"""
@Author: kang.yang
@Date: 2023/9/20 11:21
"""
import time

from urllib import parse

from kytest.utils.config import kconfig
from kytest.utils.log import logger


class Page(object):
    """页面基类，用于pom模式封装"""

    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str = None):
        if getattr(self, 'url', None) is None:
            if url is None:
                raise Exception('url不能为空')
        else:
            url = getattr(self, 'url')

        if not url.startswith('http'):
            web_host = kconfig["web_url"]
            if web_host:
                host = web_host
            else:
                host = kconfig["base_url"]
            if host is not None:
                url = parse.urljoin(host, url)
            else:
                raise Exception('host不能为空')

        self.driver.open(url)

    @staticmethod
    def sleep(n):
        logger.info(f"等待: {n}s")
        time.sleep(n)





