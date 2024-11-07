import kytest
from kytest import kconfig


if __name__ == '__main__':

    kconfig['browser'] = 'firefox'
    kytest.main(
        path="tests/test_web.py",
        host="https://www-test.qizhidao.com/",
    )
