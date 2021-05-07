from inspect import signature, Parameter
from functools import wraps
from time import time
from threading import Timer


def throttle(delay: float):
    '''限流：调用函数的时间间隔至少为 `delay` 秒，才会执行该函数。'''
    last = time()

    def wrapped(fn):
        @wraps(fn)
        def _fn(*args, **kwargs):
            now = time()
            nonlocal last
            if now - last >= delay:
                last = now
                return fn(*args, **kwargs)
        return _fn
    return wrapped


def debounce(idle: float):
    '''防抖：调用函数 `idle` 秒后，才会执行该函数，若在这 `idle` 秒内又调用此动作则将重新计算执行时间。
    '''

    def wrapped(fn):
        timer = None
        cache_args = ()
        cache_kwargs = {}

        def call():
            nonlocal timer
            timer = None
            fn(*cache_args, **cache_kwargs)

        @wraps(fn)
        def _fn(*args, **kwargs):
            nonlocal timer, cache_args, cache_kwargs
            cache_args, cache_kwargs = args, kwargs
            if timer is not None and timer.is_alive():
                timer.cancel()
            timer = Timer(idle, call)
            timer.start()
        return _fn
    return wrapped


def chainable(fn):
    '''链式调用，使类方法返回实例本身 (`self`)'''
    @wraps(fn)
    def wrapped(*args, **kwargs):
        fn(*args, **kwargs)
        return args[0]
    return wrapped


# def objectable(fn):
#     pass


def overload(*overloadings):
    '''An alternative to overload，for neat code structure. (More examples to see ./access.py)

        # Example

        ```
        def demoStr(a: str): return 'str'
        def demoInt(a: int): return 'int'
        def demoIntOpts(a: int, **kwargs): return 'int opts'

        @overload(demoStr, demoInt, demoIntOpts)
        def demo(*args, **kwargs): pass
        ```
    '''
    overloadingsOrderedParameters = list(map(lambda overloading: list(signature(
        overloading).parameters.values()), overloadings))

    def wrapped(fn):
        @wraps(fn)
        def _fn(*args, **kwargs):
            droppedSigIndexes = []
            sigParameterCursors = [0 for _ in range(
                len(overloadingsOrderedParameters))]

            def param(sigIndex, sigParameters):
                if sigParameterCursors[sigIndex] >= len(sigParameters):
                    droppedSigIndexes.append(sigIndex)
                    return None
                # current argument description of every signature
                return sigParameters[sigParameterCursors[sigIndex]]

            # parameter.kind:
            # 'POSITIONAL_ONLY':  followed by /
            # 'KEYWORD_ONLY':  following *
            # 'POSITIONAL_OR_KEYWORD':
            # 'VAR_POSITIONAL':  *args
            # 'VAR_KEYWORD':  **kwargs

            for arg in args:
                # iter every signature
                for sigIndex, sigParameters in enumerate(overloadingsOrderedParameters):
                    if sigIndex in droppedSigIndexes:
                        continue
                    # exclude signature expecting less arguments.
                    if sigParameterCursors[sigIndex] >= len(sigParameters):
                        droppedSigIndexes.append(sigIndex)
                        continue

                    # current argument description of every signature
                    parameter = sigParameters[sigParameterCursors[sigIndex]]

                    # exclude signature that requires the parameter must be keyword.
                    if parameter.kind in [Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD]:
                        droppedSigIndexes.append(sigIndex)
                        continue
                    # check type, exclude signature that mismatches argument type
                    if parameter.annotation is not Parameter.empty and not isinstance(arg, parameter.annotation):
                        droppedSigIndexes.append(sigIndex)
                        continue

                    # move to next if is not VAR_POSITIONAL (like *args)
                    if parameter.kind != Parameter.VAR_POSITIONAL:
                        sigParameterCursors[sigIndex] += 1

            for argName, argValue in kwargs.items():
                # iter every signature
                for sigIndex, sigParameters in enumerate(overloadingsOrderedParameters):
                    if sigIndex in droppedSigIndexes:
                        continue
                    # exclude signature expecting less arguments.
                    if sigParameterCursors[sigIndex] >= len(sigParameters):
                        droppedSigIndexes.append(sigIndex)
                        continue
                    # current argument description of every signature
                    parameter = sigParameters[sigParameterCursors[sigIndex]]
                    # ! if parameter is *args, move to next
                    if parameter.kind is Parameter.VAR_POSITIONAL:
                        sigParameterCursors[sigIndex] += 1
                        # exclude signature expecting less arguments.
                        if sigParameterCursors[sigIndex] >= len(sigParameters):
                            droppedSigIndexes.append(sigIndex)
                            continue
                        # current argument description of every signature
                        parameter = sigParameters[sigParameterCursors[sigIndex]]

                    # exclude signature that requires the parameter must be positional.
                    if parameter.kind is Parameter.POSITIONAL_ONLY:
                        droppedSigIndexes.append(sigIndex)
                        continue
                    # check name, exclude signature that mismatches argument name
                    if parameter.kind in [Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY] and argName != parameter.name:
                        droppedSigIndexes.append(sigIndex)
                        continue
                    # check type, exclude signature that mismatches argument type
                    if parameter.annotation is not Parameter.empty and not isinstance(argValue, parameter.annotation):
                        droppedSigIndexes.append(sigIndex)
                        continue

                    # move to next if is not VAR_KEYWORD (like **kwargs)
                    if parameter.kind != Parameter.VAR_KEYWORD:
                        sigParameterCursors[sigIndex] += 1

            # print([overloadings[index].__name__ for index in droppedSigIndexes],
            #       [(overloadings[index].__name__, cursor) for index, cursor in enumerate(sigParameterCursors)])
            # signatures having more parameters
            for sigIndex, sigParameters in enumerate(overloadingsOrderedParameters):
                if sigIndex not in droppedSigIndexes:
                    for parameter in sigParameters[sigParameterCursors[sigIndex]:]:
                        # not *args or **kwargs, and parameter.default is empty (required)
                        if parameter.kind not in [Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD] and isinstance(parameter.default, Parameter.empty):
                            break
                    # return first match.
                    # print('Selected: ',
                    #       overloadings[sigIndex].__name__, args, kwargs)
                    return overloadings[sigIndex](*args, **kwargs)
            # fallback
            return fn(*args, **kwargs)
        return _fn
    return wrapped
