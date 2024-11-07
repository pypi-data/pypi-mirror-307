import logging
import os
from importlib import import_module
from inspect import isclass
from pathlib import Path
from sys import path
import re

from cdktf import App, TerraformStack, StringMap
from subprocess import Popen, PIPE

# adjust path for library loading:
# prefer cdktf get over prebuild imports
path.append(f"{Path(__file__).parent.parent.parent}/imports")
# include terrajinja sbp.* packages
path.append(f"{Path(__file__).parent.parent.parent}/terrajinja")
# include terrajinja prebuild imports
path.append(f"{Path(__file__).parent.parent.parent}/terrajinja/imports")

logger = logging.getLogger(__name__)


class TaskMissingError(Exception):
    """Task is missing in resource"""


class ModuleMissingError(Exception):
    """Module is missing in resource"""


class InvalidLookupKey(Exception):
    """Invalid data was provided for lookup key in string."""


class LookupKeyNotFound(Exception):
    """The provided lookup key was not found."""


class NoProvidersInDeployment(Exception):
    """There is no provider specified in the deployment"""


class NoResourcesInDeployment(Exception):
    """There is no resource specified in the deployment"""


def pascal_case(s):
    """Convert snake_case string in to PascalCase."""
    return "".join(word.title() for word in s.split("_"))


class TerraformDeployment(TerraformStack):
    def __init__(self, name: str, **kwargs):
        self.results: dict = {}
        self.app = App(**kwargs)
        super().__init__(self.app, name)

    @staticmethod
    def import_module(module: str) -> callable:
        """Try multiple names to import a provided module
            these can be either via import (e.g. vcd.network_routed_v2)
            or via pip (e.g. cdktf_cdktf_provider_vcd.network_routed_v2)
            we choose to try the pip one first, and if it fails, use the search path

        Args:
            module (str): name of the module we try to import

        Returns:
            object: imported module
        """
        try:
            return import_module(f"cdktf_cdktf_provider_{module}")
        except ModuleNotFoundError:
            pass

        # return import_module(module, package='.imports')
        return import_module(module)

    @staticmethod
    def class_name(module: str) -> str:
        """Create the class name based on module name

        Args:
            module (str): name of the module in format of import path

        Returns:
            str: class name of the module
        """
        provider = module.split(".")[0]
        # change data type resource to match class names
        # vcd.data_vcd_my_provider -> data_vcd_my_provider
        # vcd.my_provider -> vcd_my_provider
        if module.startswith(f"{provider}.data_{provider}"):
            module = ".".join(module.split(".")[1:])
        return pascal_case(module.replace(".", "_"))

    def getattr_module_and_class(self, module: str) -> callable:
        """Get attr of module and class based on module_name

        Args:
            module (str): name of the module in format of import path

        Returns:
            object: class to call of the imported module
        """
        # import module
        imported_module = self.import_module(module)
        # get class_name
        class_name = self.class_name(module)
        try:
            return getattr(imported_module, class_name)
        except AttributeError:
            # if including the provider name fails, try without
            class_name = self.class_name(module.split('.')[-1])
            return getattr(imported_module, class_name)

    def get_variable_by_path(self, item: any, search: str) -> str:
        """
        Replace a given key value ($something) with a matching value in the item.

        Args:
            item: item to search in
            search: key to search

        Returns:
            the value found in the cache

        Raises:
            InvalidLookupKey: if provided lookup key does not match the expected format
            LookupKeyNotFound: the provided lookup key was not found in the cache

        """
        key = search.split('.')
        more = '.'.join(key[1:])
        if isinstance(item, dict):
            keyed_item = item.get(key[0])
            if not keyed_item:
                raise LookupKeyNotFound(f"did not find '{key}' in '{item.keys()}")
            if more:
                return self.get_variable_by_path(keyed_item, more)
            return keyed_item
        if isinstance(item, str):
            raise LookupKeyNotFound(f"reached a str/int {item} but want to search deeper '{'.'.join(key)}'")
        if isinstance(item, StringMap):
            return item.lookup(key[0])
        if isclass(type(item)):
            try:
                result = getattr(item, key[0])
            except AttributeError:
                raise LookupKeyNotFound(f"did not find '{key}' in class '{type(item)}")

            if more:
                return self.get_variable_by_path(result, more)
            return result

    def replace_lookup_variables_recursive(self, parameters: dict) -> any:
        """
        Searches recursively in a dict to replace any variables starting with a $ sign.

        It performs a lookup of these value to see if they resolve to an earlier executed stack.

        Args:
            parameters: the parameters items of the module

        Returns:
            dict with search values resolved

        """
        if isinstance(parameters, dict):
            for k in parameters.keys():
                parameters[k] = self.replace_lookup_variables_recursive(parameters[k])
            return parameters

        if isinstance(parameters, list):
            return [self.replace_lookup_variables_recursive(item) for item in parameters]

        if isinstance(parameters, str):
            matches = re.findall(r'\$[a-zA-Z0-9_.-]+', parameters)
            for match in matches:
                try:
                    replacement_value = self.get_variable_by_path(self.results, match[1:])
                except LookupKeyNotFound as e:
                    print(f"  WARN: lookup key not found, this may be expected: {e}")
                    continue

                if isinstance(replacement_value, str):
                    parameters = parameters.replace(match, replacement_value)
                else:
                    parameters = replacement_value
                    break
            return parameters
        return parameters

    def create_resource(self, name: str, module: str, resource: dict) -> object:
        """Create a terraform resource and add it to App

        Args:
            name (str): name of the resource to create
            module (str): name of the module to load
            resource (dict): dict which defines a resource (expects: task, module and (optionally) parameters)

        Raises:
            ModuleMissingError: module has not been declared as part of resource

        Returns:
            object: results of the created resource
        """
        parameters = resource.get('parameters')
        if isclass(parameters) is list:
            raise TypeError(f"parameter provided to {name} is list, expected dict: {parameters}")
        if parameters:
            print(f"task: {name} params: {list(resource['parameters'].keys())}")
        class_ = self.getattr_module_and_class(module)
        try:
            return class_(self, name, **self.replace_lookup_variables_recursive(resource.get("parameters", {})))
        except TypeError as e:
            raise TypeError(
                f"error {e} calling {class_} with {self.replace_lookup_variables_recursive(resource['parameters'])}")

    def compile(self, providers: list[dict], resources: list[dict]) -> App:
        """Create and register all providers and resources called in order

        Args:
            providers (list[dict]): providers to load
            resources (list[dict]): resources to load

        Raises:
            TaskMissingError: task has not been declared as part of resource

        Returns:
            App: terraform App
        """
        if not providers:
            raise NoProvidersInDeployment("no provided added in deployment")
        if not resources:
            raise NoResourcesInDeployment("no resource added in deployment")
        for resource in providers + resources:
            task_name = resource.get("task")
            if not task_name:
                raise TaskMissingError(f"resource '{resource}' has no 'task' name declared.")
            module = resource.get("module")
            if not module:
                raise ModuleMissingError(f"resource '{task_name}' has no 'module' declared")
            self.results.update({task_name: self.create_resource(task_name, module, resource)})
            # print(f"results: {self.results}")
        return self.app

    @staticmethod
    def run(command: list):
        procExe = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        while procExe.poll() is None:
            line = procExe.stdout.readline()
            yield line

    def action(self, action):
        self.app.synth()
        if action == 'plan':
            print('executing cdktf plan:')
            for output in self.run(['cdktf', 'plan']):
                print(output, end="")
        if action == 'apply':
            print('executing cdktf apply:')
            for output in self.run(['cdktf', 'apply', '--auto-approve', '--skip-synth']):
                print(output, end="")
        if action == 'destroy':
            allow_delete = os.getenv('TJCLI_ALLOW_DESTROY')
            if not allow_delete:
                print("to delete your stack, please set the environment variable 'TJCLI_ALLOW_DESTROY' first.")
                exit(1)
            print('executing cdktf delete:')
            for output in self.run(['cdktf', 'destroy', '--auto-approve', '--skip-synth']):
                print(output, end="")
