# 介绍

[Gitee](https://gitee.com/bluepang2021/kytest_project)

Android/IOS/Web/API automation testing framework based on pytest.

> 基于pytest的安卓/IOS/Web/API平台自动化测试框架。

## 特点

* 提供丰富的断言
* 支持生成随机测试数据
* 支持设置用例依赖
* 提供强大的`数据驱动`，支持json、yaml
* 集成`allure`, 支持HTML格式的测试报告
* 集成`requests`/`playwright`/`facebook-wda`/`uiautomator2`



## 三方依赖

* [测试报告：Allure](https://github.com/allure-framework/allure2)
    * 依赖：java8及以上版本
    * 安装方式：
        * macos：brew install allure
        * windows（powershell）：scoop install allure
        * 其它方式：下载zip包解压到本地，然后配置环境变量即可
* [拾取元素：uiauto.dev](https://uiauto.dev/)
    * 安装方式：安装kytest后自动安装
* [查看安卓设备id：adb](https://formulae.brew.sh/cask/android-platform-tools)
    * 安装方式：
        * macos：brew install android-platform-tools
        * windows（powershell）：scoop install android-platform-tools
        * 其它方式：下载zip包解压到本地，然后配置环境变量即可
* [查看IOS设备id：tidevice](https://github.com/alibaba/tidevice)
    * 安装方式：安装kytest时自动安装
* [IOS端代理：WebDriverAgent](https://github.com/appium/WebDriverAgent)
    * 安装方式：使用xcode编译后安装至手机

## Install

```shell
> pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ktest
```

## 🔬 Demo

[demo](/demo) 提供了丰富实例，帮你快速了解ktest的用法。

## 接口脚本生成
```
from kytest import generate_case


if __name__ == '__main__':
    # 需要启动一个tms服务，并导入对应project的swagger文档
    host = "http://localhost:8001"
    generate_case(host=host,
                  project="qzd-bff-enterprise",
                  controller="企业详情",
                  base_path="tests")
```

## 项目脚手架
### 搭建简单项目结构，方便快速开始编写脚本
```
Usage: kytest create [OPTIONS]

  创建新项目 @param platform: 平台，如api、android、ios、web @return:

Options:
  -p, --platform TEXT  Specify the platform.
  --help               Show this message and exit.
```

## web录制并生成脚本
### 敬请期待
