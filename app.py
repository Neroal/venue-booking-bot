from flask import Flask, request, render_template, redirect, url_for
import webbrowser
from threading import Thread, Timer
from sdk import Sdk

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    account = request.form['account']
    password = request.form['password']
    time_slot = request.form['timeSlot']

    execute(account, password, time_slot)

    return redirect(url_for('index'))

def open():
    webbrowser.open_new('http://127.0.0.1:5000')

def execute(account, password, time_slot):
    # A: 83, B: 84, C: 1074, D: 1075
    venue_ids = [83, 84, 1074, 1075]

    threads = []
    for venue_id in venue_ids:
        thread = Thread(target=run_sdk, args=(account, password, venue_id, time_slot))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def run_sdk(account, password, venue_id, time_slot):
    bot_sdk = Sdk()
    bot_sdk.open_login_page()
    bot_sdk.close_entry_button()
    bot_sdk.login(account, password)
    bot_sdk.booking(venue_id, time_slot)

if __name__ == "__main__":
    Timer(1, open).start()

    app.run()
