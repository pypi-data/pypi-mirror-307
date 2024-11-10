from typing import Any

__all__ = [
    'Arg',
    'validate_kwargs',
]


class Arg:
    def __init__(self,
                 arg_name: str,
                 arg_type: type = object,
                 required: bool = False,
                 default_value: Any = None):

        # init vars
        self._arg_name = 'default'
        self._arg_type = object
        self._required = False
        self._default_value = None

        self.set_arg_name(arg_name)
        self.set_arg_type(arg_type)
        self.set_required(required)
        self.set_default_value(default_value)

    def get_arg_name(self) -> str:
        return self._arg_name

    def get_arg_type(self) -> type:
        return self._arg_type

    def get_required(self) -> bool:
        return self._required

    def get_default_value(self) -> Any:
        return self._default_value

    def set_arg_name(self, arg_name: str):
        if not isinstance(arg_name, str):
            raise TypeError('arguments "arg_name" must be an instance of str')
        if not arg_name:
            raise ValueError('arguments "arg_name" must be a non-empty str')

        self._arg_name = arg_name
        return self

    def set_arg_type(self, arg_type: type):
        if not isinstance(arg_type, type):
            raise TypeError('arguments "arg_type" must be one of built-in types')

        self._arg_type = arg_type
        return self

    def set_required(self, required: bool):
        if not isinstance(required, bool):
            raise TypeError('arguments "required" must in [True, False]')

        self._required = required
        return self

    def set_default_value(self, default_value=None):
        self._default_value = default_value
        return self


def validate_kwargs(expected: list[Arg], actual: dict) -> None:
    """
    Validate "actual" kwargs against "expected", and set default values if necessary.

    :param expected: expected arguments
    :param actual: actual arguments
    """
    for arg in expected:
        if not isinstance(arg, Arg):
            raise TypeError(f'element of "expected" must be an instance of "Arg"')

        arg_name = arg.get_arg_name()
        arg_type = arg.get_arg_type()

        # arg found in actual
        if arg_name in actual:
            if not isinstance(actual[arg_name], arg_type):
                raise TypeError(f'{arg_name} must be an instance of {arg_type}')
        # arg not found in actual
        else:
            if arg.get_required():
                raise ValueError(f'{arg_name} is required')
            else:
                actual[arg_name] = arg.get_default_value()
