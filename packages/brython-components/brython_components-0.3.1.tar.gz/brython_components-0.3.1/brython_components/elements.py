from browser import DOMNode, html

from .decorators import CACHE_DECORATORS


class customElement(DOMNode):
    use_shadow: bool = True
    shadow_options: dict = {"mode": "open"}

    def __init__(self, use_shadow: bool = True, shadow_options: dict = {}):
        if use_shadow and self.use_shadow:
            self.attachShadow(shadow_options or self.shadow_options)

        self.render_root = getattr(self, "shadowRoot", self)

    def connectedCallback(self):
        for decorated in CACHE_DECORATORS.get(self.__class__.__name__, []):
            decorated(self)

    def disconnectedCallback(self):
        pass

    def adoptedCallback(self):
        pass
