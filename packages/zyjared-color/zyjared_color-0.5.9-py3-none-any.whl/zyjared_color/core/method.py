from typing import Dict, Any, TypeVar
from .style import Style

__all = [
    "create_style_method_meta"
]

_S = TypeVar("_S", bound="Style")


def _create_method(key: str, value: Any):
    def handler(self: _S):
        self.style[key] = value
        return self
    return handler


def create_style_method_meta(styles: Dict[str, Any]):
    class StyleMethodMeta(type):
        def __new__(cls, name, bases, attrs):
            for k, v in styles.items():
                if isinstance(v, dict):
                    for k1, v1 in v.items():
                        attrs[k1] = _create_method(k, v1)
                else:
                    attrs[k] = _create_method(k, v)
            return super().__new__(cls, name, bases, attrs)

    return StyleMethodMeta
