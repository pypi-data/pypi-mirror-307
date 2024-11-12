from .html import ColorHtml
from .styles import STYLES
from ..core import create_static_style_meta


class StaticColorHtml(metaclass=create_static_style_meta(ColorHtml, STYLES)):
    pass