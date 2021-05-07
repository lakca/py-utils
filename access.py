from decorators import overload
from typing import Sequence, Any, overload as overloadType

# func@set_index #

# declare methods of overload.


def _set_index_of_list(ls: list, index: int, value):
    '''Set list value based on index, return the value'''
    missing = index + 1 - len(ls)
    while missing > 0:
        ls.append(None)
        missing -= 1
    ls[index] = value
    return value


def _set_index_of_dict(dc: dict, attr: str, value):
    '''Set dict value based on attribute, return the value'''
    dc[attr] = value
    return value


# declare types of overload.

@overloadType
def set_index(target: list, index: int, value) -> Any:
    '''Set list value based on index, return the value'''
    pass


@overloadType
def set_index(target: dict, attr: str, value) -> Any:
    '''Set dict value based on attribute, return the value'''
    pass

# expose of overload


@overload(_set_index_of_list, _set_index_of_dict)
def set_index(*args, **kwargs):
    '''Set value based on index, return the value. Extending `list` if out of range with `None`.'''
    pass


# func@index_of #

# declare methods of overload.


def _index_of_sequence(target: Sequence, index: int, default=None):
    '''Get sequence value based on index'''
    return target[index] if -len(target) <= index < len(target) else default


def _index_of_dict(target: dict, attr: str, default=None):
    '''Get dict value based on attribute'''
    return target[attr] if attr in target else default


# declare types of overload.

@overloadType
def index_of(target: Sequence, index: int, default=None) -> Any:
    '''Get sequence value based on index'''
    pass


@overloadType
def index_of(target: dict, attr: str, default=None) -> Any:
    '''Get dict value based on attribute'''
    pass


# expose of overload

@overload(_index_of_sequence, _index_of_dict)
def index_of(*args, **kwargs):
    '''Get value based on index, silence out of range.'''
    pass
