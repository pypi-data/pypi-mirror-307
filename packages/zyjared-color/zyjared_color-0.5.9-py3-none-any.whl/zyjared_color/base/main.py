from .color import Color
from .styles import STYLES
import re

__all__ = ["Color", "color"]

_STYLES_MAP = {}

for k, v in STYLES.items():
    if isinstance(v, dict):
        for _, v1 in v.items():
            _STYLES_MAP[f'{v1}'] = k
    else:
        _STYLES_MAP[f'{v}'] = k


def _parse(text: str):
    array: list[dict] = []
    sep_reg = r'(.*)(\033\[[\d;]+m)(.*)'
    for v in text.split('\033[0m'):
        if not v:
            continue

        groups = re.findall(sep_reg, v)

        # 无样式文本

        if not groups:
            if v:
                array.append({"text": v})
            continue

        if groups[0][0]:
            array.append({"text": groups[0][0]})

        # 样式与文本

        if groups[0][2]:
            styles_str: str = groups[0][1][2:-1]
            styles = {_STYLES_MAP[v]: v for v in styles_str.split(
                ';') if v in _STYLES_MAP}
            array.append({"text": groups[0][2], "style": styles})

    return array


def color(content: str | Color):
    '''
    将字符串转换为 Color 对象

    Example:

    ```python
    # 链式调用
    c1 = color('Hello World!').red().bold()

    # 不用顾及参数是否为 Color 类型
    c2 = color(c1)

    # 保留原始样式，或选择改变
    c3 = color('\\033[33mHello World!\\033[0m test').bold()

    # 拼接
    c4 = c1 + 'test'
    c4.bold() # 拼接后为 Color 对象，可以继续调用

    # format
    c5 = color(f'{c1:<15}test')
    ```
    '''
    if isinstance(content, Color):
        return content

    array = _parse(content)
    if len(array) > 1:
        return Color(
            _children=[
                Color(
                    v['text'],
                    v.get('style', {})
                ) for v in array
            ])
    else:
        return Color(content, array[0].get('style', {}))
