import time
import argparse

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
    
    def login(self, account, password):
        self.page('#ContentPlaceHolder1_loginid').input(account)
        self.page('#loginpw').input(password)

        time.sleep(1)
        self.page('#login_but').click()

        print('login')
        
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SDK script with parameters.')
    parser.add_argument('--account', type=str, required=True, help='account to the browser')
    parser.add_argument('--password', type=str, required=True, help='password to the browser')

    args = parser.parse_args()

    sdk = Sdk()
    sdk.open()
    sdk.close_entry_button()
    sdk.login(args.account, args.password)
    
    time.sleep(60)  # 保持浏览器打开60秒
    
    sdk.close()
