import time
from datetime import datetime, timedelta
from DrissionPage import ChromiumPage, ChromiumOptions
import requests
import threading

class Sdk:
    def __init__(self, region_config):
        co = ChromiumOptions().auto_port()
        self.page = ChromiumPage(co)
        self.page.set.auto_handle_alert()
        self.cookies = {}
        self.ids = region_config['ids']
        self.base_url = f'https://scr.cyc.org.tw/{region_config["site"]}.aspx'

    def open_login_page(self):
        self.page.get(f'{self.base_url}?module=login_page&files=login')

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

        self.page.wait.url_change(f'{self.base_url}?Module=ind&files=ind', timeout=10)
        
        self.cookies = self.page.cookies()
    
    def booking(self, time_slot):
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        wait_time = (midnight - now).total_seconds()
        two_weeks_later = (midnight + timedelta(weeks=2)).strftime('%Y/%m/%d')

        # mark for fast testing
        time.sleep(wait_time)
        # two_weeks_later = "2024/08/01"

        threads = []
        for _ in range(10):
            for id in self.ids:
                url = f'{self.base_url}?module=net_booking&files=booking_place&StepFlag=25&QPid={id}&QTime={time_slot}&PT=1&D={two_weeks_later}'
                thread = threading.Thread(target=self.fetch, args=(url,))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

    def fetch(self, url):
        session = requests.Session()
        for cookie in self.cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        session.get(url)
