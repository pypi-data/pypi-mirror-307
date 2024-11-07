"""
@Author: kang.yang
@Date: 2023/10/26 09:48
"""
import time
import allure
import requests

from kytest.core.api.request import HttpReq
from kytest.utils.log import logger
from kytest.utils.config import kconfig
from kytest.utils.allure_util import AllureData


class TestCase(HttpReq):
    """
    测试用例基类，所有测试用例需要继承该类
    """
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
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        cls().end_class()

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

    def setup_method(self):
        project_name = kconfig['project']
        if project_name:
            allure.dynamic.feature(project_name)

        self.start()

    def teardown_method(self):
        self.end()

    # 公共方法
    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.info(f"暂停: {n}s")
        time.sleep(n)

    @staticmethod
    def check_coverage_data(backend_url, project_name):
        """
        检查接口平台已覆盖的接口在脚本中是否都已覆盖
        @param backend_url: tms平台后端服务域名，如: http://localhost:8001
        @param project_name: tms平台已导入接口项目名，如：kz-bff-patent
        @return:
        """
        apis_covered = AllureData().get_api_list()
        url = f"{backend_url}/api/api_test/api/check_test_result"
        body = {
            "project_name": project_name,
            "apis_covered": apis_covered
        }
        res = requests.post(url, json=body)

        if res.json()['data']['status'] == 'pass':
            print("都已真实覆盖。")
        else:
            miss_list = res.json()['data']['error_list']
            print(f"还有{len(miss_list)}个接口漏掉了，如下：")
            for api in miss_list:
                print(api)

