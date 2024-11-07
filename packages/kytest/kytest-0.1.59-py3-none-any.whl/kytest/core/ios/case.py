"""
@Author: kang.yang
@Date: 2023/10/26 09:48
"""
import time
import allure

from .driver import Driver
from .elem import Elem

from kytest.core.api.request import HttpReq
from kytest.running.conf import App
from kytest.utils.log import logger
from kytest.utils.config import kconfig


class TestCase(HttpReq):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    dr: Driver = None
    launch: bool = True

    # ---------------------初始化-------------------------------
    def start_class(self):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    def end_class(self):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        try:
            cls().start_class()
        except BaseException as e:
            logger.error(f"start_class Exception: {e}")

    @classmethod
    def teardown_class(cls):
        try:
            cls().end_class()
        except BaseException as e:
            logger.error(f"end_class Exception: {e}")

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    # def config(self):
    #     """
    #     目前就是用来设置是否自动启动应用
    #     @return:
    #     """
    #     pass

    def setup_method(self):
        # # 设置调整
        # self.config()

        # 设置用例默认feature
        project_name = kconfig['project']
        if project_name:
            allure.dynamic.feature(project_name)

        # 驱动初始化
        self.dr = Driver(App.did)

        # # 启动应用
        # if self.launch is True:
        #     self.dr.util.start_app(App.pkg)

        self.start()

    def teardown_method(self):
        self.end()

    # 公共方法
    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.info(f"暂停: {n}s")
        time.sleep(n)

    def shot(self, name: str, delay=0):
        """截图"""
        if delay:
            self.sleep(delay)
        self.dr.shot(name)

    # UI方法
    def elem(self,
             xpath=None,
             name=None,
             label=None,
             value=None,
             text=None,
             className=None,
             index=None):
        _kwargs = {}
        if name is not None:
            _kwargs["name"] = name
        if label is not None:
            _kwargs["label"] = label
        if value is not None:
            _kwargs["value"] = value
        if text is not None:
            _kwargs["text"] = text
        if className is not None:
            _kwargs["className"] = className
        if index is not None:
            _kwargs["index"] = index
        if xpath is not None:
            _kwargs["xpath"] = xpath

        return Elem(driver=self.dr, **_kwargs)

    def uninstall_app(self):
        """
        卸载应用
        @return:
        """
        self.dr.util.uninstall_app(App.pkg)

    def install_app(self, apk_url):
        """
        安装应用
        @return:
        """
        self.dr.util.install_app(apk_url)

    def start_app(self):
        """
        启动应用
        @return:
        """
        self.dr.util.start_app(App.pkg)

    def stop_app(self):
        """
        停止应用
        @return:
        """
        self.dr.util.stop_app(App.pkg)
