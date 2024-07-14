import time
import argparse
from datetime import datetime, timedelta
from DrissionPage import ChromiumPage

class Sdk:
    def __init__(self):
        self.page = ChromiumPage()
        self.page.set.auto_handle_alert()

    def open_login_page(self):
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

    def try_booking(self, date):
        self.page.get('https://scr.cyc.org.tw/tp01.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D=' + date + '&D2=1')
        
        venue_types = ['A', 'B', 'C', 'D']
        time_range = '06:00~07:00'

        try:
            conditions = " || ".join([f'onclickText.includes("羽 {vt}") && onclickText.includes("{time_range}")' for vt in venue_types])
            script = f"""
                var success = false;
                var buttons = document.getElementsByName('PlaceBtn');
                for (var i = 0; i < buttons.length; i++) {{
                    var onclickText = buttons[i].getAttribute('onclick');
                    if (onclickText && ({conditions})) {{
                        buttons[i].click();
                        success = true;
                    }}
                }}
                return success ? 'Button clicked' : 'Button not found';
            """
            result = self.page.run_js(script)
            print(result)
            if 'Button clicked' in result:
                return True
        except Exception as e:
            print(f'Error clicking button: {e}')
        return False

    def keep_trying_booking(self, date, interval=0.2, max_attempts=10):
        attempts = 0
        while attempts < max_attempts:
            success = self.try_booking(date)
            if success:
                print('Successfully booked the venue.')
                break
            attempts += 1
            print(f'Retrying in {interval} seconds... (Attempt {attempts}/{max_attempts})')
            time.sleep(interval)
        if attempts == max_attempts:
            print('Reached maximum attempts. Exiting.')

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
    sdk.open_login_page()
    sdk.close_entry_button()
    sdk.login(args.account, args.password)
    
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    wait_time = (midnight - now).total_seconds()
    print(f'Waiting for {wait_time} seconds until midnight')
    time.sleep(10)
    
    sdk.keep_trying_booking(args.date)
    
    sdk.close()
