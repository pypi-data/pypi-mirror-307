from ..framework import Element


class Input(Element):
    XPATH_CURRENT = "//input"

    def is_enabled(self):
        return not self.get_attribute("disabled") == "true"
