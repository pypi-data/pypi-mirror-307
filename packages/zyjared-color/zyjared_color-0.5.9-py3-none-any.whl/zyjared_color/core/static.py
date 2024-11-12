from typing import Any, Dict, TypeVar, Type
from .style import Style

__all__ = [
    "create_static_style_meta",
]

_S = TypeVar("_S", bound="Style")


def _create_static_method(custom_cls: Type[_S], attr: str):
    def handler(text: str | _S) -> _S:
        return getattr(custom_cls(text), attr, lambda: print(f'static {attr} not found'))()
    return handler


def create_static_style_meta(custom_cls: Type[_S], styles: Dict[str, Any], ):
    class StaticStyleMeta(type):
        def __new__(cls, name, bases, attrs):
            for k, v in styles.items():
                if isinstance(v, dict):
                    for k1, _ in v.items():
                        attrs[k1] = staticmethod(_create_static_method(custom_cls, k1))
                else:
                    attrs[k] = staticmethod(_create_static_method(custom_cls, k))
            return super().__new__(cls, name, bases, attrs)

    return StaticStyleMeta
