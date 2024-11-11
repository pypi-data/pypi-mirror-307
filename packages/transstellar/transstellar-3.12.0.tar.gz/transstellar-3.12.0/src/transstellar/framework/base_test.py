import time

import pytest

from .application import Application
from .logger import Logger


class BaseTest:
    app: Application
    logger: Logger

    @pytest.fixture(autouse=True)
    def setup_method_base_test(self, app: Application):
        self.app = app
        self.logger = Logger(self.__class__.__name__)

    def sleep(self, seconds: float):
        self.logger.debug(f"sleep: {seconds} seconds")

        time.sleep(seconds)
