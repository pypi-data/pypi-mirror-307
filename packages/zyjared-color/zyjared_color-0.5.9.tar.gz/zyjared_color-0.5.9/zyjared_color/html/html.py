from typing import Union, TypeVar
from ..core import Style, create_style_method_meta
from .styles import STYLES

_C = TypeVar("_C", bound="ColorHtml")


class ColorHtml(Style, metaclass=create_style_method_meta(STYLES)):

    def _compose_style(self):
        return f'<span style="{";".join([f'{k}:{v}' for k, v in self.style.items()])};">{self.text}</span>'

    def _compose_children(self) -> str:
        text = super()._compose_children()
        if not self.style:
            return text
        return f'<span style="{";".join([f'{k}:{v}' for k, v in self.style.items()])};">{text}</span>'

    def _propagate_style(self) -> None:
        for k, _ in self.style.items():
            for s in self.children:
                if k in s.style:
                    del s.style[k]

    def __add__(self, other: Union[str, _C]):
        return self.__class__(_children=[self, other])

    def __radd__(self, other: Union[str, _C]):
        return self.__class__(_children=[other, self])
