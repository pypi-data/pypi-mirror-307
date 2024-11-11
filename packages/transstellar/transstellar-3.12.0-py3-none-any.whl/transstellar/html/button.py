from ..framework import Element


class Button(Element):
    XPATH_CURRENT = "//button"

    def is_enabled(self):
        return not self.get_attribute("disabled") == "true"
