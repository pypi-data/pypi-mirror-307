from .color import Color
from .main import color
# from .styles import get_style_names


def _alias(attr: str):
    def alias(content: str | Color) -> Color:
        return getattr(color(content), attr)()
    return alias


# attributes = get_style_names()
# globals().update({
#     name: _alias(name)
#     for name in attributes
# })


bold = _alias('bold')
dim = _alias('dim')
italic = _alias('italic')
underline = _alias('underline')
blink = _alias('blink')
blink_fast = _alias('blink_fast')
reverse = _alias('reverse')
hidden = _alias('hidden')
through = _alias('through')

# fg

black = _alias('black')
red = _alias('red')
green = _alias('green')
yellow = _alias('yellow')
blue = _alias('blue')
magenta = _alias('magenta')
cyan = _alias('cyan')
white = _alias('white')
bright_black = _alias('bright_black')
bright_red = _alias('bright_red')
bright_green = _alias('bright_green')
bright_yellow = _alias('bright_yellow')
bright_blue = _alias('bright_blue')
bright_magenta = _alias('bright_magenta')
bright_cyan = _alias('bright_cyan')
bright_white = _alias('bright_white')

# bg

bg_black = _alias('bg_black')
bg_red = _alias('bg_red')
bg_green = _alias('bg_green')
bg_yellow = _alias('bg_yellow')
bg_blue = _alias('bg_blue')
bg_magenta = _alias('bg_magenta')
bg_cyan = _alias('bg_cyan')
bg_white = _alias('bg_white')
bg_bright_black = _alias('bg_bright_black')
bg_bright_red = _alias('bg_bright_red')
bg_bright_green = _alias('bg_bright_green')
bg_bright_yellow = _alias('bg_bright_yellow')
bg_bright_blue = _alias('bg_bright_blue')
bg_bright_magenta = _alias('bg_bright_magenta')
bg_bright_cyan = _alias('bg_bright_cyan')
bg_bright_white = _alias('bg_bright_white')
