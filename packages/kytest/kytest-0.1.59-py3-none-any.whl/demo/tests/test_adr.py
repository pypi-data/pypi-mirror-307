import kytest
from kytest.adr import TC

from page.adr_page import AdrPage


@kytest.story('测试demo')
class TestAdrDemo(TC):
    def start(self):
        self.start_app()
        self.adr = AdrPage(self.dr)

    @kytest.title('进入设置页')
    def test_go_setting(self):
        if self.adr.adBtn.exists():
            self.adr.adBtn.click()
        self.adr.myTab.click()
        self.adr.setBtn.click()
        self.adr.page_title.assert_text_eq('设置')





