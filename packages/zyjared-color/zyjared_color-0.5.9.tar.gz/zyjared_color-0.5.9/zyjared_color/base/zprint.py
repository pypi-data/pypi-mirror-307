from .color import Color
from .main import color
import sys

__all__ = [
    'zprint',
]

LIST_PREFIX = Color('·').bold()
DICT_SEP = ' '

# 字典的 key 与 列表的 LIST_PREFIX 颜色
COLORS = [
    'green',
    'cyan',
    'magenta',
    'yellow'
]


def _color(text: Color | str, *, i, force=False):
    '''
    支持 text 携带样式代码
    - skip:
      - `true`: 如果包含颜色代码，则不转换
      - `false`: 统一颜色
    '''
    if not force and ((isinstance(text, str) and '\033[' in text) or (isinstance(text, Color))):
        return text
    return getattr(color(text), COLORS[i])()


def _color_idx(i):
    return i % len(COLORS)


def _blank(n):
    return ' ' * n


def _list_prefix(blank, *, _c_idx=0):
    return f'{_blank(blank)}{_color(LIST_PREFIX, i=_c_idx, force=True)}'


def _put(text, end='\n'):
    if text:
        sys.stdout.write(f'{text}{end}')
    else:
        sys.stdout.write(f'{text!r}{end}')


def _put_list(ls: list, *, blank: int = 2, _c_idx=0):
    if len(ls) == 0:
        sys.stdout.write('[ ]')

    for i in range(len(ls)):
        if isinstance(ls[i], dict):
            sys.stdout.write(f'{_list_prefix(blank, _c_idx=_c_idx)}\n')
            _put_dict(ls[i], blank=blank + 2, _c_idx=_color_idx(_c_idx + 1))
        elif isinstance(ls[i], list):
            _put_list(ls[i], blank=blank + 2, _c_idx=_color_idx(i + 1))
        else:
            sys.stdout.write(f'{_list_prefix(blank, _c_idx=_c_idx)} ')
            _put(f'{ls[i]}')


def _put_dict(dic: dict, *, blank: int = 0, force_color_key=False, sep=DICT_SEP, _c_idx=0):
    if len(dic) == 0:
        sys.stdout.write('{ }')

    max_key_len = max([len(k) for k in dic.keys()])
    for k, v in dic.items():
        sys.stdout.write(
            f'{' ' * blank}{_color(
                k,
                i=_c_idx,
                force=force_color_key
            ):<{max_key_len}}{sep}'
        )
        if isinstance(v, list):
            sys.stdout.write('\n')
            _put_list(v, blank=blank + 2)
        elif isinstance(v, dict):
            sys.stdout.write('\n')
            _put_dict(v,
                      blank=blank + 2,
                      _c_idx=_color_idx(_c_idx + 1),
                      )
        else:
            _put(v)


def print_list(ls: list, *, blank: int = 0):
    '''
    打印列表
    - blank: 空格数
    '''
    _put_list(ls, blank=blank)
    sys.stdout.flush()


def print_dict(dic: dict, *, blank: int = 0, force_color_key=False, sep=DICT_SEP):
    '''
    打印字典
    - sep: key 与 value 的分隔符
    - blank: 空格数
    - force_color: 如果 key 包含颜色代码，是否继续转换
    '''
    _put_dict(dic, blank=blank, force_color_key=force_color_key, sep=sep)
    sys.stdout.flush()


def zprint(content: str | Color | list | dict, *, blank=0, sep=DICT_SEP, force_color=False):
    '''
    按照一定格式打印，通常打印列表、字典，会做一定的美化。

    若无必要，请使用 `print` 或者 `pprint`。

    :param content: 需要打印的内容
    :param blank: `dict` | `list` 空格数
    :param sep: `dict` key 与 value 的分隔符
    :param force_color: `dict` 如果 key 包含颜色代码，是否继续转换
    '''
    if isinstance(content,  dict):
        print_dict(content,
                   blank=blank,
                   sep=sep,
                   force_color_key=force_color)
    elif isinstance(content, list):
        print_list(content, blank=blank)
    else:
        print(content)
