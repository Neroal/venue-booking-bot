from flask import Flask, request, render_template, redirect, url_for
import webbrowser
import threading
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
    bot_sdk = Sdk()
    bot_sdk.open_login_page()
    bot_sdk.close_entry_button()
    bot_sdk.login(account, password)
    bot_sdk.keep_trying_booking(time_slot)
    bot_sdk.close()

if __name__ == "__main__":
    threading.Timer(1, open).start()

    app.run()
