# sdk.py
import time
from datetime import datetime, timedelta
from DrissionPage import ChromiumPage, ChromiumOptions

class Sdk:
    def __init__(self):
        co  = ChromiumOptions().auto_port()
        self.page = ChromiumPage(co)
        self.page.set.auto_handle_alert()

    def open_login_page(self):
        self.page.get('https://scr.cyc.org.tw/tp01.aspx?module=login_page&files=login')

    def close_entry_button(self):  
        button = self.page.ele('css:.swal2-confirm.swal2-styled')
        if button:
            button.click()

    def login(self, account, password):
        # TODO: Better way to check cloudflare success event
        time.sleep(3)

        self.page('#ContentPlaceHolder1_loginid').input(account)
        self.page('#loginpw').input(password)
        self.page('#login_but').click()

        self.page.wait.url_change('https://scr.cyc.org.tw/tp01.aspx?Module=ind&files=ind', timeout=10)

    def booking(self, venue_id, time_slot):
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        wait_time = (midnight - now).total_seconds()
        two_weeks_later = (midnight + timedelta(weeks=2)).strftime('%Y/%m/%d')

        time.sleep(wait_time)

        self.page.get(f'https://scr.cyc.org.tw/tp01.aspx?module=net_booking&files=booking_place&StepFlag=25&QPid={venue_id}&QTime={time_slot}&PT=1&D={two_weeks_later}') 