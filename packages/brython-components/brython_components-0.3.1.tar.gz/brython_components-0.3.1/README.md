# Brython-components

Brython-components is an easy implementation of brython's webcomonent.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install brip
brip install brython-components
```

## Usage

### file.html
```html
<popup-info>
    <span slot="data-text">Popup info data</span>
</popup-info>
```

### file.py
```python
from browser import html

from brython_components import bind, customElement, defineElement, react

html.maketag("SLOT")

@defineElement("popup-info")
class PopupInfo(customElement):
    def __init__(self):
        super().__init__()

        self.render_root <= html.STYLE('''
        .wrapper {
            position: relative;
        }
        .info {
            font-size: 0.8rem;
            width: 200px;
            display: inline-block;
            border: 1px solid black;
            padding: 10px;
            background: white;
            border-radius: 10px;
            opacity: 0;
            transition: 0.6s all;
            position: absolute;
            top: 20px;
            left: 10px;
            z-index: 3;
        }
        .icon:hover + .info, .icon:focus + .info {
            opacity: 1;
        }
        ''')

        wrapper = html.SPAN(Class="wrapper")

        icon = html.SPAN(Class="icon", tabindex="0")
        wrapper <= icon

        info = html.SPAN(Class="info")
        info <= html.SLOT(name="data-text")
        wrapper <= info

        self.render_root <= wrapper
        
    @bind(".icon", "click")
    def deactivate(self, event):
        info = self.render_root.select_one(".info")
        icon = event.target
        if not info.style.opacity:
            info.style["opacity"] = 1
            icon.style["text-decoration"] = "line-through"
        else:
            info.style["opacity"] = ""
            icon.style["text-decoration"] = ""
            
    @react(".icon")
    def completed(self, targets):
        targets[0].text = ":) hover me"
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
