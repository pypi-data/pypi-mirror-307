from typing import *


def isshape(obj: Any, shape: Any) -> bool:
    """
    Check if an object matches a given generic type expression.

    :param obj: The object to be checked.
    :type obj: Any
    :param shape: The generic type expression to match against.
    :type shape: Any
    :return: True if the object matches the type expression, False otherwise.
    :rtype: bool
    """
    if isinstance(obj, Tuple) and isinstance(shape, Tuple):
        for _obj, _type in zip(obj, shape):
            if not isinstance(_obj, _type):
                return False

    origin = get_origin(shape)

    if origin == list:
        if not isinstance(obj, origin):
            return False
        element_type = get_args(shape)[0]
        return all(isshape(item, element_type) for item in obj)

    elif origin in (dict, map):
        if not isinstance(obj, origin):
            return False
        key_type, value_type = get_args(shape)
        return all(isshape(key, key_type) and isshape(value, value_type) for key, value in obj.items())

    elif origin == Union:
        return any(isshape(obj, t) for t in get_args(shape))

    elif origin == None:
        return isinstance(obj, shape)

    else:
        if not isinstance(obj, origin):
            return False
        element_type = get_args(shape)[0]
        return all(isshape(item, element_type) for item in obj)
