import os
from typing import Type
from urllib.parse import ParseResult, urlparse

from injector import Injector
from pytest import FixtureRequest
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.remote.webdriver import WebDriver

from transstellar.framework.loggable import Loggable

from .main_config import MainConfig
from .module import Module
from .router import Router


# pylint: disable-next=R0902
class Application(Loggable):
    container: Injector
    testrun_uid: str
    request: FixtureRequest
    driver: WebDriver
    options: any
    e2e_enabled: bool = False
    closed: bool = False
    current_user = None

    def __init__(self, params: dict):
        super().__init__()

        self.logger.info("Creating application")

        options = params.get("options")
        self.request = params.get("request")
        self.driver = params.get("driver")
        self.testrun_uid = params.get("testrun_uid")
        self.container = Injector()
        self.router = Router(self)
        self.main_config = self.get(MainConfig)

        routes = params.get("routes")

        if options:
            self.options = options
        else:
            self.options = {}

        self.__configure_log__()
        self.__remove_existing_screenshots__()
        self.register_routes(routes)

    def init_e2e(self):
        if self.e2e_enabled:
            return

        self.e2e_enabled = True

        self.driver = self.__init_driver__()

        self.closed = False

    def is_e2e_enabled(self):
        return self.e2e_enabled

    def get(self, key: any):
        return self.container.get(key)

    def register_module(self, module_class: Type[Module]):
        module = module_class(self)
        self.container.binder.bind(module_class, module)

    def register_routes(self, routes: dict):
        self.router.register_routes(routes)

    def get_page(self, route_key: str):
        self.guard_e2e()

        return self.router.get_page(route_key)

    def build_page(self, page_class):
        return self.router.build_page(page_class)

    def go_to_url(self, url: str):
        self.router.go_to_url(url)

    def go_to(self, route_key: str, path_params: dict = None):
        self.guard_e2e()

        return self.router.go_to(route_key, path_params)

    def guard_e2e(self):
        if not self.e2e_enabled:
            raise AttributeError("e2e is not enabled")

    def close(self):
        if self.closed:
            return

        self.logger.info("Closing application")

        if self.is_e2e_enabled():
            self.driver.quit()
            self.logger.info("Driver closed")

        self.e2e_enabled = False
        self.closed = True

        self.logger.info("Application closed")

    def set_current_user(self, user):
        if not self.is_e2e_enabled():
            raise RuntimeError("Only E2E test supports setting current user")

        self.current_user = user

    def get_current_user(self):
        return self.current_user

    def is_logged_in(self):
        return self.current_user is not None

    def get_current_url(self) -> ParseResult:
        return urlparse(self.driver.current_url)

    def __configure_log__(self):
        worker_id = os.environ.get("PYTEST_XDIST_WORKER")
        if worker_id is not None:
            with open(file=f"logs/pytest_{worker_id}.log", mode="w", encoding="utf-8"):
                pass

            self.logger.configure(
                file_format=self.request.config.getini("log_file_format"),
                filename=f"logs/pytest_{worker_id}.log",
                level=self.request.config.getini("log_file_level"),
            )

    def __remove_existing_screenshots__(self):
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")

        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        else:
            for file_name in os.listdir(screenshots_dir):
                file_path = os.path.join(screenshots_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    def __init_driver__(self) -> WebDriver:
        self.logger.info("Initializing driver")
        selenium_cmd_executor = os.environ.get(
            "SELENIUM_CMD_EXECUTOR", "http://selenium:4444/wd/hub"
        )
        implicitly_wait_time = self.options.get("implicitly_wait_time", 10)
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = Remote(command_executor=selenium_cmd_executor, options=options)
        driver.implicitly_wait(implicitly_wait_time)
        self.logger.info("Driver initialized")

        return driver
