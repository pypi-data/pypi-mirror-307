import os
import time
from typing import Type, TypeVar

from injector import Injector
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from transstellar.framework.decorators.with_timeout import with_timeout

from .loggable import Loggable
from .utils import (
    wait_for_element_by_selector,
    wait_for_element_by_xpath,
    wait_for_element_to_click_by_xpath,
    wait_for_element_to_disappear_by_xpath,
)

T = TypeVar("T")


# pylint: disable=R0904
class Element(Loggable):
    XPATH_CURRENT = None

    label = ""
    app = None
    injector: Injector
    driver: WebDriver
    dom_element: WebElement = None

    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        self.injector = app.container
        self.driver = app.driver

    def init(self):
        pass

    def init_after_dom_element_is_set(self):
        pass

    @classmethod
    def create_element(cls, app):
        instance = cls(app)
        instance.init()

        return instance

    @classmethod
    def get_current_element_xpath(cls):
        return cls.get_xpath()

    @classmethod
    def get_xpath(cls):
        if not cls.XPATH_CURRENT:
            raise AssertionError(
                f"{cls.__name__} should set XPATH_CURRENT in order to get element"
            )

        return cls.XPATH_CURRENT

    def wait_for_ready(self):
        pass

    @with_timeout()
    def find_global_element(self, target_element_class: Type[T], timeout=0) -> T:
        self.logger.debug(
            f"finding global element for {target_element_class.__name__} with timeout: {timeout}"
        )

        target_element_xpath = target_element_class.get_current_element_xpath()
        element = self.find_global_dom_element_by_xpath(target_element_xpath)

        if element:
            return self.__create_child_element(target_element_class, element)

        raise LookupError(f"Could not find element of {target_element_class.__name__}")

    def click(self):
        self.get_current_dom_element().click()

    def refresh(self):
        self.logger.debug("refresh current element")

        xpath = self.get_current_element_xpath()
        dom_element = self.find_global_dom_element_by_xpath(xpath)

        self.set_current_dom_element(dom_element)

        return self.get_current_dom_element()

    @with_timeout()
    def find_element(self, target_element_class: Type[T], timeout=0) -> T:
        self.logger.debug(
            f"find element: {target_element_class.__name__} with timeout: {timeout}"
        )

        target_element_xpath = target_element_class.get_current_element_xpath()

        dom_element = self.find_dom_element_by_xpath(target_element_xpath)

        if dom_element:
            return self.__create_child_element(target_element_class, dom_element)

        raise LookupError(f"Could not find element of {target_element_class.__name__}")

    @with_timeout()
    def find_elements(self, target_element_class, timeout=0):
        self.logger.debug(
            f"find elements: {target_element_class.__name__} with timeout: {timeout}"
        )

        target_element_xpath = target_element_class.get_current_element_xpath()
        elements = self.find_dom_elements_by_xpath(target_element_xpath)

        if len(elements) > 0:
            return list(
                map(
                    lambda element: self.__create_child_element(
                        target_element_class, element
                    ),
                    elements,
                )
            )

        raise LookupError(f"Could not find elements of {target_element_class.__name__}")

    @with_timeout()
    def find_element_by_fuzzy_label(
        self, target_element_class: Type[T], label: str, timeout=0
    ) -> T:
        self.logger.debug(
            "find element (%s) by fuzzy label: %s with timeout: %s",
            target_element_class.__name__,
            label,
            timeout,
        )

        current_dom_element = self.get_current_dom_element()
        target_element_xpath = target_element_class.get_current_element_xpath()
        element = current_dom_element.find_element(
            By.XPATH,
            f'.{target_element_xpath}[descendant::text()[contains(normalize-space(), "{label}")]]',
        )

        if element:
            return self.__create_child_element(target_element_class, element, label)

        raise LookupError(
            f"Could not find element of {target_element_class.__name__} with label: {label}"
        )

    @with_timeout()
    def find_element_by_label(
        self, target_element_class: Type[T], label: str, timeout=0
    ) -> T:
        self.logger.debug(
            "find element (%s) by label: %s with timeout: %s",
            target_element_class.__name__,
            label,
            timeout,
        )

        current_dom_element = self.get_current_dom_element()
        target_element_xpath = target_element_class.get_current_element_xpath()
        element = current_dom_element.find_element(
            By.XPATH,
            f'.{target_element_xpath}[descendant::text()[normalize-space()="{label}"]]',
        )

        if element:
            return self.__create_child_element(target_element_class, element, label)

        raise LookupError(
            f"Could not find element of {target_element_class.__name__} with label: {label}"
        )

    def find_next_element(
        self, target_element_class: Type[T], original_element_class, timeout=0
    ) -> T:
        return self.__find_sibling_element(
            target_element_class, original_element_class, True, timeout
        )

    def find_next_element_by_xpath(
        self, target_element_class: Type[T], xpath, timeout=0
    ) -> T:
        return self.__find_sibling_element_by_xpath(
            target_element_class, xpath, True, timeout
        )

    def find_preceding_element(
        self, target_element_class: Type[T], original_element_class, timeout=0
    ) -> T:
        return self.__find_sibling_element(
            target_element_class, original_element_class, False, timeout
        )

    def find_preceding_element_by_xpath(
        self, target_element_class: Type[T], xpath, timeout=0
    ) -> T:
        return self.__find_sibling_element_by_xpath(
            target_element_class, xpath, False, timeout
        )

    @with_timeout()
    def get_next_element(self, target_element_class: Type[T], timeout=0) -> T:
        self.logger.debug(
            f"find next element of ({target_element_class.__name__}) with timeout: {timeout}"
        )

        dom_element = self.get_dom_element().find_element(
            By.XPATH, "following-sibling::*[1]"
        )

        if dom_element:
            return self.__create_child_element(target_element_class, dom_element)

        raise LookupError(
            f"Could not find next element {target_element_class.__name__}"
        )

    @with_timeout()
    def get_preceding_element(self, target_element_class: Type[T], timeout=0) -> T:
        self.logger.debug(
            f"find preceding element of ({target_element_class.__name__}) with timeout: {timeout}"
        )

        dom_element = self.get_dom_element().find_element(
            By.XPATH, "preceding-sibling::*[1]"
        )

        if dom_element:
            return self.__create_child_element(target_element_class, dom_element)

        raise LookupError(
            f"Could not find preceding element {target_element_class.__name__}"
        )

    @with_timeout()
    def find_element_by_id(
        self, target_element_class: Type[T], dom_id: str, timeout=0
    ) -> T:
        self.logger.debug(
            "find element (%s) by id: %s with timeout: %s",
            target_element_class.__name__,
            dom_id,
            timeout,
        )

        current_dom_element = self.get_current_dom_element()
        target_element_xpath = target_element_class.get_current_element_xpath()
        element = current_dom_element.find_element(
            By.XPATH, f'.{target_element_xpath}[@id="{dom_id}"]'
        )

        if element:
            return self.__create_child_element(target_element_class, element)

        raise LookupError(
            f"Could not find element of {target_element_class.__name__} with id: {dom_id}"
        )

    def is_element_present(self, target_element_class: Type[T]) -> T:
        try:
            current_dom_element = self.get_current_dom_element()
            target_element_xpath = target_element_class.get_current_element_xpath()
            current_dom_element.find_element(By.XPATH, f".{target_element_xpath}")

            return True
        except NoSuchElementException:
            return False

    def wait_for_global_element_to_disappear(self, target_element_class):
        self.logger.debug(
            f"wait for global element to dissapear: {target_element_class.__name__}"
        )

        target_element_xpath = target_element_class.get_current_element_xpath()

        return wait_for_element_to_disappear_by_xpath(
            self.driver, f".{target_element_xpath}"
        )

    def get_dom_element(self) -> WebElement:
        return self.get_current_dom_element()

    def get_current_dom_element(self) -> WebElement:
        if self.dom_element:
            return self.dom_element

        xpath = self.get_current_element_xpath()
        dom_element = self.find_global_dom_element_by_xpath(xpath)

        self.set_current_dom_element(dom_element)

        return self.dom_element

    def get_html(self):
        return self.get_current_html()

    def get_current_html(self):
        html = self.get_current_dom_element().get_attribute("outerHTML")

        self.logger.debug(f"current HTML: {html}")

        return html

    def get_text(self):
        text = self.get_dom_element().text

        self.logger.debug(f"current text: {text}")

        return text

    def find_global_dom_element_by_xpath(self, xpath: str):
        self.logger.debug(f"finding global dom element by xpath: {xpath}")

        return wait_for_element_by_xpath(self.driver, xpath)

    def find_dom_elements_by_tag_name(self, tag_name: str):
        self.logger.debug(f"finding dom element by tag name: {tag_name}")

        dom_element = self.get_current_dom_element()

        return dom_element.find_elements(By.XPATH, f".//{tag_name}")

    def find_dom_element_by_xpath(self, xpath: str):
        self.logger.debug(f"finding dom element by xpath: {xpath}")

        try:
            dom_element = self.get_current_dom_element()
            child_dom_element = dom_element.find_element(By.XPATH, f".{xpath}")
        except StaleElementReferenceException:
            dom_element = self.get_current_dom_element()
            current_xpath = self.get_xpath()

            child_dom_element = self.driver.find_element(
                By.XPATH, f"{current_xpath}{xpath}"
            )
        except NoSuchElementException:
            self.logger.debug(f"current html: {self.get_html()}")
            raise

        return child_dom_element

    def find_dom_elements_by_xpath(self, xpath: str):
        self.logger.debug(f"finding dom element by xpath: {xpath}")

        try:
            dom_element = self.get_current_dom_element()
            child_dom_elements = dom_element.find_elements(By.XPATH, f".{xpath}")

        except StaleElementReferenceException:
            self.refresh()

            dom_element = self.get_current_dom_element()
            child_dom_elements = dom_element.find_elements(By.XPATH, f".{xpath}")

        return child_dom_elements

    def wait_for_dom_element_to_disappear_by_xpath(self, xpath: str, timeout: int = 10):
        self.logger.debug(f"wait for dom element to disappear by xpath: {xpath}")

        return wait_for_element_to_disappear_by_xpath(self.driver, f".{xpath}", timeout)

    def wait_for_dom_element_to_click_by_xpath(self, xpath: str, timeout: int = 10):
        self.logger.debug(f"wait for dom element to click by xpath: {xpath}")

        return wait_for_element_to_click_by_xpath(self.driver, f".{xpath}", timeout)

    def wait_for_dom_element_by_selector(self, css_selector, timeout: int = 10):
        self.logger.debug(f"wait for dom element by CSS selector: {css_selector}")

        return wait_for_element_by_selector(self.driver, css_selector, timeout)

    def screenshot(self, file_name):
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")

        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        screenshot_path = os.path.join(os.getcwd(), f"screenshots/{file_name}")

        self.driver.save_screenshot(screenshot_path)

        self.logger.info(f"{file_name} saved")

    def sleep(self, seconds: float):
        self.logger.debug(f"sleep: {seconds} seconds")

        time.sleep(seconds)

    def set_current_dom_element(self, element):
        self.dom_element = element

        self.init_after_dom_element_is_set()

    def scroll_to_view(self):
        self.app.driver.execute_script(
            "arguments[0].scrollIntoView(false);", self.dom_element
        )

    def get_classes(self):
        return self.get_attribute("class")

    def get_attribute(self, name: str):
        return self.get_current_dom_element().get_attribute(name)

    def is_displayed(self) -> bool:
        return self.get_current_dom_element().is_displayed()

    def highlight(self, color_code: str):
        """
        Testing purpose
        """

        dom_element = self.get_current_dom_element()
        new_style = f"border: 2px solid {color_code};"
        current_style = dom_element.get_attribute("style")
        combined_style = current_style + new_style

        self.driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            dom_element,
            combined_style,
        )

    def __create_child_element(
        self, child_element_class: Type[T], child_dom_element, label: str = ""
    ) -> T:
        child_element = child_element_class(self.app)
        child_element.set_current_dom_element(child_dom_element)
        child_element.init()

        if label:
            child_element.label = label

        return child_element

    @with_timeout()
    def __find_sibling_element(
        self,
        target_element_class: Type[T],
        original_element_class,
        is_next: bool = True,
        timeout=0,
    ) -> T:
        original_element_xpath = original_element_class.get_current_element_xpath()

        return self.__find_sibling_element_by_xpath(
            target_element_class, original_element_xpath, is_next, timeout
        )

    @with_timeout()
    def __find_sibling_element_by_xpath(
        self,
        target_element_class: Type[T],
        xpath: str,
        is_next: bool = True,
        timeout=0,
    ) -> T:
        method = "following-sibling" if is_next else "preceding-sibling"

        self.logger.debug(
            "find %s element (%s) of element xpath: %s with timeout: %d",
            method,
            target_element_class.__name__,
            xpath,
            timeout,
        )

        current_dom_element = self.get_current_dom_element()
        target_element_xpath = target_element_class.get_current_element_xpath()[2:]

        element = current_dom_element.find_element(
            By.XPATH,
            f".{xpath}/{method}::{target_element_xpath}",
        )

        if element:
            return self.__create_child_element(target_element_class, element)

        raise LookupError(
            f"Could not find {method} element {target_element_class.__name__} of xpath: {xpath}"
        )
