import time

from DrissionPage import ChromiumPage

class Sdk:
    def __init__(self):
        self.page = ChromiumPage()
        self.page.set.auto_handle_alert()

    def open(self):
        self.page.get('https://scr.cyc.org.tw/tp01.aspx?module=login_page&files=login')

        print('open')

    def close_entry_button(self):
        button = self.page.ele('css:.swal2-confirm.swal2-styled')
        time.sleep(1)
        button.click()

        print('close_entry_button')
        
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    sdk = Sdk()
    sdk.open()
    sdk.close_entry_button()
    
    time.sleep(60)  # 保持浏览器打开60秒
    
    sdk.close()
