import time
import argparse

from DrissionPage import ChromiumPage

class Sdk:
    def __init__(self):
        self.page = ChromiumPage()
        self.page.set.auto_handle_alert()

    def openLoginPage(self):
        self.page.get('https://scr.cyc.org.tw/tp01.aspx?module=login_page&files=login')

        print('open')

    def close_entry_button(self):
        button = self.page.ele('css:.swal2-confirm.swal2-styled')
        button.click()

        print('close_entry_button')
    
    def login(self, account, password):
        self.page('#ContentPlaceHolder1_loginid').input(account)
        self.page('#loginpw').input(password)

        time.sleep(0.5)
        self.page('#login_but').click()
        
        print('login')
    
    def booking(self, date):
        self.page.get('https://scr.cyc.org.tw/tp01.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D=' + date + '&D2=1')
        
        venue_types = ['A', 'B', 'C', 'D']
        time_range = '06:00~07:00'
        start_time = time.time()

        try:
            while time.time() - start_time < 6:
                for venue_type in venue_types:
                    script = f"""
                        var buttons = document.getElementsByName('PlaceBtn');
                        for (var i = 0; i < buttons.length; i++) {{
                            var onclickText = buttons[i].getAttribute('onclick');
                            if (onclickText && onclickText.includes('羽 {venue_type}') && onclickText.includes('{time_range}')) {{
                                buttons[i].click();
                                return 'Button clicked: 羽 {venue_type} {time_range}';
                            }}
                        }}
                        return 'Button not found for 羽 {venue_type} {time_range}';
                    """
                    result = self.page.run_js(script)
                    print(result)
                    if 'Button clicked' in result:
                        return
                time.sleep(0.1)
            print('Timeout reached, button not found')
        except Exception as e:
            print(f'Error clicking button: {e}')

        
    def close(self):
        self.page.close()

        print('close')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SDK script with parameters.')
    parser.add_argument('--account', type=str, required=True, help='account to the browser')
    parser.add_argument('--password', type=str, required=True, help='password to the browser')
    parser.add_argument('--date', type=str, required=True, help='booking date')

    args = parser.parse_args()

    sdk = Sdk()
    sdk.openLoginPage()
    sdk.close_entry_button()
    sdk.login(args.account, args.password)
    sdk.booking(args.date)
    
    time.sleep(600)  # 保持浏览器打开60秒
    
    sdk.close()
