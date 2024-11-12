from ..core import Style, create_style_method_meta
from .styles import STYLES
import re
from typing import TypeVar

_C = TypeVar("_C", bound="Color")


class Color(Style, metaclass=create_style_method_meta(STYLES)):
    '''
    如果文本已有 ANSI 的样式，请使用 `color(content)` 函数, `color(content)` 更加通用。

    Example:

    >>> from zyjared_color import Color
    >>> Color('hello world').red().bold()
    '''

    children: list[_C]

    def _compose_style(self):
        return f'\033[{';'.join([str(i) for i in self.style.values()])}m{self.text}\033[0m'

    @property
    def size(self):
        if self.children:
            return sum([c.size for c in self.children])
        else:
            if self.style:
                return len(self._compose_style())
            else:
                return len(self.text)

    def __format__(self, format_spec: str):

        # 无 format_spec
        if not format_spec:
            return super().__format__(format_spec)

        ns = re.findall(r'\d+', format_spec)

        # 无效 format_spec
        if not ns:
            return super().__format__(format_spec)

        exc_size = self.size - len(self)

        # 无样式的情况
        if exc_size <= 0:
            return super().__format__(format_spec)

        _spec = format_spec.replace(
            ns[0],
            f'{int(ns[0]) + exc_size}'
        )
        return f'{self._to_str():{_spec}}'
