from functools import update_wrapper

from browser import webcomponent

CACHE_DECORATORS = {}


def defineElement(name):
    def decorator(cls):
        if webcomponent.get(name) is None:
            webcomponent.define(name, cls)
        return cls

    return decorator


def append_decorators(func, value):
    class_name = func.__qualname__.split(".")[-2]
    update_wrapper(value, func)
    CACHE_DECORATORS.setdefault(class_name, []).append(value)


def bind(target, evt):
    def decorator(func):
        append_decorators(
            func,
            lambda self: [
                _.bind(evt, getattr(self, func.__name__))
                for _ in self.render_root.select(target)
            ],
        )
        return func

    return decorator


def react(target):
    def decorator(func):
        append_decorators(
            func,
            lambda self: getattr(self, func.__name__)(self.render_root.select(target)),
        )
        return func

    return decorator
