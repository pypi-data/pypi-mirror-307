<h1 align='center'>tingetone</h1>
<h2 align='center'>ANSI color formatting for output in terminal</h2>

<p align='center'>
    <a href="https://www.python.com">
        <img 
            alt="made with python" 
            src="https://img.shields.io/badge/Made With-python-blue"
        />
    </a>
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/Code%20Style-Black-000000.svg"/></a>
    <a href="https://pypi.org/project/tingetone">
        <img 
            alt="Downloads" 
            src="https://img.shields.io/badge/Downloads-26k-blue"
        />
    </a>
</p>

## Setup and Installation

### Using pip

```bash
pip install tingetone
```


## Example

### Foreground

```python
from tingetone import colored

print(colored("This is red text", color="red"))
```

Or

```python
from tingetone import cprint

cprint("Hello there", color="green")
```

### Foreground and Background

```python
from tingetone import colored

print(colored("Green on white", color="green", on_color="white"))
```

Or

```python
from tingetone import cprint

cprint("Red on black", color="red", on_color="black")
```

### Styling

> underline & italic are not supported on windows

```python
from tingetone import italic, underline, bold

print(italic("This is italic"))
print(underline("This is underlined"))
print(bold("This is bold"))
```

### Styling with Foreground and Background

```python
from tingetone import colored, italic, underline, bold

print(
    underline("This is red on white",
    color="red",
    on_color="white")
)

print(
    italic("This is italic",
    color="green")
)
```

### Specific Use Cases

These method prints by default & return None

```python
from tingetone import warn, error, info, success

warn("This is warning") # yellow bold text
info("This is to inform") # blue bold text
success("Success", strong=False) # green normal text
error("Error: File Missing") # red bold text
```

### Horizontal Line (width equal to terminal width)

```python
from tingetone import line

line()  # a horizontal line
line(text="Hello")  # horizontal line with text in middle
line(text="Hello", color="red") # red color line with text in middle
help(line)  # for more info
```

## Available Colors and Styles

| Foreground(color) | Background(on_color) |
| ----------------- | -------------------- |
| Black             | Grey                 |
| Red               | Red                  |
| Green             | Green                |
| Yellow            | Yellow               |
| Blue              | Blue                 |
| Magenta           | Magenta              |
| Cyan              | Cyan                 |
| White             | White                |

<br>

<br>

| Style | Bold | Italic | Underline |
| ----- | ---- | ------ | --------- |


<br>

| Function    | Parameters                  | Use for                    |
| ----------- | --------------------------- | -------------------------- |
| `colored`   | _text_, _color_, _on_color_ | Colored text               |
| `italic`    | _text_, _color_, _on_color_ | Italic colored text        |
| `underline` | _text_, _color_, _on_color_ | Underlined colored text    |
| `bold`      | _text_, _color_, _on_color_ | Bold colored text          |
| `warn`      | _text_                      | Yellow Bold Warning text   |
| `error`     | _text_                      | Red Bold Error text        |
| `info`      | _text_                      | Blue Bold Information text |
| `success`   | _text_                      | Green Bold Success text    |

