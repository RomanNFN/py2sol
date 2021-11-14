import typing

from config import VARIABLE_TEMPLATE, FUNCTION_TEMPLATE
from config.enums import AccessMode


class Variable:
    TEMPLATE = VARIABLE_TEMPLATE

    def __init__(self, name: str, default_value: typing.Any, var_type: typing.Any):
        self.name = name
        self.default_value = default_value
        self.type = var_type
        # self.is_public
        # self.is_static

    def to_sol(self) -> str:
        return self.TEMPLATE.render(type=self.type, name=self.name, default_value=self.default_value)


class Function:
    TEMPLATE = FUNCTION_TEMPLATE

    def __init__(self, name: str, arguments: list[tuple], return_types: list[typing.Type], access: AccessMode,
                 code: list[str]):
        self.name = name
        self.arguments = arguments
        self.return_types = return_types
        self.access = access
        self.code = code

    def to_sol(self) -> str:
        return self.TEMPLATE.render(function_name=self.name,
                                    function_args=self.arguments,
                                    access=self.access.value,
                                    return_types=self.return_types,
                                    code=self.code)
