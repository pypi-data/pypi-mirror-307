from typing import Dict, Union, Any, TypeVar, List, Optional, Type

_S = TypeVar("_S", bound="Style")


def convert_to_style_list(cls: Type[_S], arr: List[str]):
    children = []
    for item in arr:
        if isinstance(item, Style):
            if item.children:
                children.extend(convert_to_style_list(cls, item.children))
            else:
                children.append(cls(
                    item.text, item._cp_style()))
        else:
            children.append(cls(item))
    return children


class Style:

    text: str | None
    style: dict
    children: list[_S]

    def __init__(self, text: Optional[Union[str | _S]] = None, _style: Optional[Dict[_S, Any]] = None, _children: Optional[List[Union[_S, str]]] = None):
        """
        参数:
            - `text`:
                - `Style`: 拷贝其属性, `_style` 和 `_children` 将作为扩展。
                - `str`: 直接赋值。
        """
        if isinstance(text, Style):
            self.text = text.text if text.text else None
            self.style = text._cp_style()
            if _style:
                self.style = {**self.style, **_style}
            self.children = text._cp_children(True) if text.children else []
            if _children:
                self.children.extend(
                    convert_to_style_list(self.__class__, _children))
        else:
            self.text = text
            self.style = _style if _style else {}
            self.children = convert_to_style_list(
                self.__class__, _children) if _children else []

    def _compose_style(self) -> str:
        """
        self.text 和 self.style 合并的结果

        子类应该会重写
        """
        return self.text

    def __fcompose_style(self) -> str:
        if self.style:
            return self._compose_style()
        else:
            return self.text or ''

    def _propagate_style(self) -> None:
        """
        传递 style 到 children
        """
        for k, v in self.style.items():
            for s in self.children:
                s.style[k] = v

    def _compose_children(self) -> str:
        """
        style 和 self.children 合并的结果

        如果不需要在最外层嵌套，则可以不用重写
        """
        return ''.join([c.__fcompose_style() for c in self.children])

    def propagate(self):
        """
        如果 `children` 不为空, 则将 `style` 传递给 `children`
        """
        if not self.children:
            return self

        self._propagate_style()
        return self

    def _cp_style(self):
        return {**self.style}

    def _cp_children(self, propagate=False):
        """
        参数:
            - `propagate`: 是否将 `style` 传递给 `children`
        """
        if propagate:
            self.propagate()
        return [self.__class__(child.text, child._cp_style()) for child in self.children]

    def copy(self, propagate=False):
        """
        返回一个拷贝

        参数:
            - `propagate`: 是否将 `style` 传递给 `children`
        """
        return self.__class__(self.text, self._cp_style(), self._cp_children(propagate))

    def extend(self, color: _S):
        if not self.text:
            self.text = color.text
        self.style = {**self.style, **color.style}
        self.children.extend(color._cp_children(True))
        return self

    def _to_str(self, propagate=True):
        if self.children:
            if propagate:
                self.propagate()
            return self._compose_children()
        else:
            return self.__fcompose_style()

    def __add__(self, other: Union[str, _S]):
        return self.__class__(_children=[self, other])

    def __radd__(self, other: Union[str, _S]):
        return self.__class__(_children=[other, self])

    def __repr__(self):
        result = {
            "text": self.text,
            "style": self.style,
            "children": [
                {'text': i.text, 'style': i.style} for i in self.children
            ]
        }
        return str(result)

    def __str__(self):
        return self._to_str()

    def __format__(self, format_spec: str):
        return f'{self._to_str():{format_spec}}'

    def __len__(self):
        if self.children:
            return sum([len(c) for c in self.children])
        return len(self.text)
