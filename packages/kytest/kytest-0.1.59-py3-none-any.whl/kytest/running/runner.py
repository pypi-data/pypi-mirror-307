import shutil
import pytest

from multiprocessing import Process
from typing import Literal, Union

from kytest.running.conf import App
from kytest.utils.log import logger
from kytest.utils.config import kconfig
from kytest.running.execution_scheduler import (
    _get_case_list,
    _app_main
)


class TestMain(object):
    """
    测试框架入口
    """

    def __init__(
            self,
            title: str = None,
            path: str = None,
            host=None,
            headers: dict = None,
            pkg: str = None,
            did=None,
            ability=None,
            rule: Literal[
                "full_serial",
                "full_parallel",
                "split_serial",
                "split_parallel"] = 'full_serial',
            rerun: int = 0,
            xdist: Union[bool, int, str] = False,
            report_path: str = 'report'
    ):
        """
        @param title：报告标题
        @param path: 用例路径
        @param host: 域名，用于接口测试和web测试
            如果host为str时，默认设置base_url
            如果要设置web_host，需要用{'web': 'https://www.qizhidao.com'}的方式传值
            如果接口和web都要使用，则设置{'api': '', 'web': ''}
        # @param web_host：web域名，用于web测试和接口测试并存时区分
        @param headers: 请求头，用于接口测试和web测试
        @param pkg:
            安卓包名，通过adb shell pm list packages | grep 'xxx'获取
            IOS包名，通过tidevice applist | grep 'xxx'获取
            鸿蒙包名，通过hdc shell aa dump -l 获取
        @param did:
            安卓设备id：通过adb devices获取
            IOS设备id：通过tidevice list获取
            鸿蒙设备id：通过hdc list targets获取
        @param ability: 鸿蒙应用的main name，通过如下命令获取
            $ hdc shell aa dump -l    # 运行命令前需要手动打开app
            User ID #100
              current mission lists:{
                Mission ID #139  mission name #[#com.kuaishou.hmapp:kwai:EntryAbility]  lockedState #0  mission affinity #[]
                  AbilityRecord ID #55
                    app name [com.kuaishou.hmapp]
                    main name [EntryAbility]
                    bundle name [com.kuaishou.hmapp]
                    ability type [PAGE]
                    state #FOREGROUND  start time [152523]
                    app state #FOREGROUND
                    ready #1  window attached #0  launcher #0
                    callee connections:
                    isKeepAlive: false
             }
        @param rule: 多设备执行模式
                - full_serial：每个设备都执行全部用例，串行执行
                - full_parallel：每个设备都执行全部用例，并发执行
                - split_serial：每个设备执行部分用例，串行执行
                - split_parallel：每个设备执行部分用例，并发执行
        @param rerun: 失败重试次数
        @param xdist: 是否并发执行，应该是多进程
        @param report_path: 报告路径
        """
        logger.info("kytest start.")
        kconfig['project'] = title
        # kconfig['base_url'] = host
        # kconfig['web_url'] = web_host
        if isinstance(host, str):
            kconfig['base_url'] = host
        if isinstance(host, dict):
            kconfig['base_url'] = host.get('api', None)
            kconfig['web_url'] = host.get('web', None)
        kconfig['headers'] = headers

        App.did = did
        App.pkg = pkg
        App.ability = ability

        def _serial_execute(_path):
            # 串行执行用例
            cmd_list = [
                '-sv',
                '--reruns', str(rerun),
                '--alluredir', report_path, '--clean-alluredir'
            ]

            if _path:
                cmd_list.insert(0, _path)

            if xdist:
                if xdist is True:
                    cmd_list.insert(1, '-n')
                    cmd_list.insert(2, 'auto')
                    cmd_list.insert(3, '--dist=loadscope')
                elif isinstance(xdist, int) or isinstance(xdist, str):
                    cmd_list.insert(1, '-n')
                    cmd_list.insert(2, str(xdist))
                    cmd_list.insert(3, '--dist=loadscope')

            logger.info(cmd_list)
            pytest.main(cmd_list)

        def _parallel_execute(_params):
            # 并发执行用例
            if 'parallel' in rule:
                if _params:
                    for param in _params:
                        pr = Process(target=_app_main, args=param)
                        pr.start()
            elif 'serial' in rule:
                if _params:
                    for param in _params:
                        _app_main(*param)

        def _collect_case_and_split(device_id, _path):
            # 用例采集
            _path_list = [{item: []} for item in device_id]
            test_cases = _get_case_list(_path)
            print(test_cases)
            # 把用例均分成设备数量的份数
            n = len(device_id)
            _lists = [[] for _ in range(n)]
            for _i, item in enumerate(test_cases):
                index = _i % n  # 计算元素应该分配给哪个列表
                _lists[index].append(item)
            return _lists

        # 多设备执行策略
        if isinstance(did, list):
            params = []
            if not did:
                _serial_execute(path)
            elif len(did) == 1:
                App.did = did[0]
                _serial_execute(path)
            else:
                # 清空上次执行的目录
                shutil.rmtree(report_path, ignore_errors=True)
                if 'full' in rule:
                    for device in did:
                        params.append((path, device, pkg, report_path, True))
                else:
                    lists = _collect_case_and_split(did, path)

                    for i in range(len(did)):
                        _path = lists[i][0] if len(lists[1]) < 2 else ','.join(lists[i])
                        params.append((_path, did[i], pkg))

                # 多进程执行
                _parallel_execute(params)

        else:
            # 串行执行
            _serial_execute(path)

        # 公共参数重置
        kconfig.reset()
        # App参数重置
        App.did = None
        App.pkg = None


main = TestMain

if __name__ == '__main__':
    main()
