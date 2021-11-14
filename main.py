from abc import ABC
import typing
import inspect

from config import CONTRACT_TEMPLATE, OUTPUT_FILE
from config.enums import AccessMode
from helpful import is_function, snake_to_camel
from models import Variable, Function


class ContractBase(ABC):
    pass


class Foo(ContractBase):
    a: int = 1
    b: str

    def return_int(self, some_int: int) -> int:
        return some_int


def generate(contract: typing.Type[ContractBase]):
    contract_template = CONTRACT_TEMPLATE
    variables = parse_variables(contract)
    functions = parse_functions(contract)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(contract_template.render(contract_name=contract.__name__,
                                         variables=variables,
                                         functions=functions))


def parse_variables(contract: typing.Type[ContractBase]) -> typing.List[str]:
    variables = []
    for annotation in contract.__annotations__.items():
        default_value = None
        items = contract.__dict__
        if annotation[0] in items:
            default_value = items[annotation[0]]
        variable = Variable(annotation[0], default_value, annotation[1].__name__)
        variables.append(variable.to_sol())
    return variables


def parse_functions(contract: typing.Type[ContractBase]) -> list[str]:
    functions = []
    for obj_name, obj in contract.__dict__.items():
        if is_function(obj):
            code = parse_function_code(obj)
            func = Function(
                name=snake_to_camel(obj_name),
                arguments=parse_function_arguments(obj),
                # TODO split return types
                return_types=[obj.__annotations__['return'].__name__],
                access=AccessMode.PRIVATE,
                code=code
            )
            functions.append(func.to_sol())
    return functions


def parse_function_arguments(function) -> list[tuple]:
    arguments = []
    for annotation_name, annotation in function.__annotations__.items():
        if annotation_name not in ('return',):
            # TODO get argument solidity type
            arguments.append(tuple([annotation_name, annotation.__name__]))
    return arguments


def parse_function_code(function) -> list[str]:
    function_raws = []
    for raw in inspect.getsource(function).split('\n')[1:]:
        # TODO converts
        if raw:
            function_raws.append(f"{raw};")
    return function_raws


if __name__ == '__main__':
    generate(Foo)
