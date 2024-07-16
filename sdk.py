# sdk.py
import time
from datetime import datetime, timedelta
from DrissionPage import ChromiumPage

class Sdk:
    def __init__(self):
        self.page = ChromiumPage()
        self.page.set.auto_handle_alert()

    def open_login_page(self):
        self.page.get('https://scr.cyc.org.tw/tp01.aspx?module=login_page&files=login')

    def close_entry_button(self):  
        button = self.page.ele('css:.swal2-confirm.swal2-styled')
        if button:
            button.click()

    def login(self, account, password):
        time.sleep(3)

        self.page('#ContentPlaceHolder1_loginid').input(account)
        self.page('#loginpw').input(password)
        self.page('#login_but').click()

        while True:
            if self.page.url == "https://scr.cyc.org.tw/tp01.aspx?Module=ind&files=ind":
                break
            time.sleep(0.5)

    def try_booking(self, date, time_slot, d2):
        self.page.get(f'https://scr.cyc.org.tw/tp01.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D={date}&D2={d2}', timeout=2)

        venue_types = ['A', 'B', 'C', 'D']

        try:
            conditions = " || ".join([f'onclickText.includes("羽 {vt}") && onclickText.includes("{time_slot}")' for vt in venue_types])
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

            if 'Button clicked' in result:
                return True
        except Exception as e:
            print(f'Error clicking button: {e}')
        return False

    def keep_trying_booking(self, time_slot, interval=0.2, max_attempts=5):
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        wait_time = (midnight - now).total_seconds()
        two_weeks_later = (midnight + timedelta(weeks=2)).strftime('%Y/%m/%d')

        start_time = time_slot.split("~")[0]
        d2 = 1
        if "06:00" <= start_time < "11:00":
            d2 = 1
        elif "11:00" <= start_time < "17:00":
            d2 = 2
        elif "17:00" <= start_time < "22:00":
            d2 = 3

        attempts = 0
        while attempts < max_attempts:
            success = self.try_booking(two_weeks_later, time_slot, d2)
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
