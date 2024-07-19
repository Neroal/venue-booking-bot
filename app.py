from flask import Flask, request, render_template, redirect, url_for
import webbrowser
from threading import Timer, Thread
from sdk import Sdk

app = Flask(__name__)

@app.route('/')
def index():
    account = request.args.get('account', '')
    password = request.args.get('password', '')
    time_slot = request.args.get('time_slot', '')

    return render_template('index.html', account=account, password=password, time_slot=time_slot)

@app.route('/submit', methods=['POST'])
def submit():
    account = request.form['account']
    password = request.form['password']
    time_slot = request.form['timeSlot']

    Thread(target=execute, args=(account, password, time_slot)).start()

    return redirect(url_for('index', account=account, password=password, time_slot=time_slot))

def execute(account, password, time_slot):
    bot_sdk = Sdk()
    bot_sdk.open_login_page()
    bot_sdk.close_entry_button()
    bot_sdk.login(account, password)
    bot_sdk.booking(time_slot)

def open():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == "__main__":
    Timer(1, open).start()

    app.run()
