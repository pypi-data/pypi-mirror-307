import re


def str_has_style(text: str):
    '''
    检查字符串是否包含 ANSI 转义序列
    '''
    return bool(re.search(r'\033\[\d+', text))
