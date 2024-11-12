# zyjared-color

## 安装

```sh
pip install zyjared-color
```

## 使用

```py
from zyjared_color import color, blue, red

# 基本使用
content = color('Hello World!').red() + ' - test'
print(content.bold()) # content 可以继续调用

# 自由转换
text = f'{color("Hello World!").blue():<15} - test'
content = color(text).yellow()
print(content)

# 使用别名
print(blue('Hello World!'))
print(red('Hello World!').bold())
```

### 拓展

#### `zprint`

需要使用 `print` 打印列表或者字典时可以使用。

```py
from zyjared_color import zprint

zprint([
    'Hello',
    'World!',
])

zprint({
    '1': 'Hello World!',
    '2': ['Hello World!'],
    '3': {
        '3-1!': 'Hello World!'
    }
})
```

## HTML / CSS

```python
from zyjared_color.html import ColorHtml, StaticColorHtml
from zyjared_color.html import blue, red, bold, italic, underline, through

text = ColorHtml('Hello World!').red().bold()
print(text)

# custom styles
text = ColorHtml("Hello World!", {"opacity": 0.5, "font-weight": "bold"})
print(text)
```

**example:** Display `ColorHtml` in Jupyter Notebook

```python
from zyjared_color.html import ColorHtml as Color, StaticColorHtml as StaticColor
from zyjared_color.html import blue, red, bold, italic, underline, through
from IPython.display import display, HTML

text = Color('Hello World!').red().bold()

# f'{text}' or str(text)
display(HTML(f'{text}'))
```
