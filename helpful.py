""""..."""
""" BOOLEANS """


def is_function(obj: object) -> bool:
    return callable(obj)


def is_snake_case(name: str) -> bool:
    return '_' in name


""" OTHERS """


def snake_to_camel(name: str) -> str:
    if is_snake_case(name):
        first, *others = name.split('_')
        return ''.join([first.lower(), *[word.title() for word in others]])
    return name
