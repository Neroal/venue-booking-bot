from flask import Flask, request, render_template, redirect, url_for
import webbrowser
from threading import Timer, Thread
from sdk import Sdk
import json

app = Flask(__name__)

with open('config.json') as f:
    config = json.load(f)

@app.route('/')
def index():
    account = request.args.get('account', '')
    password = request.args.get('password', '')
    time_slot = request.args.get('time_slot', '')
    region = request.args.get('region', '')

    return render_template('index.html', regions=config['regions'], time_slots=config['time_slots'], account=account, password=password, time_slot=time_slot, region=region)

@app.route('/submit', methods=['POST'])
def submit():
    account = request.form['account']
    password = request.form['password']
    time_slot = request.form['timeSlot']
    region = request.form['region']

    selected_region_config = next((r for r in config['regions'] if r['site'] == region), None)

    Thread(target=execute, args=(account, password, time_slot, selected_region_config)).start()

    return redirect(url_for('index', account=account, password=password, time_slot=time_slot, region=region))

def execute(account, password, time_slot, region_config):
    bot_sdk = Sdk(region_config)
    bot_sdk.open_login_page()
    bot_sdk.close_entry_button()
    bot_sdk.login(account, password)
    bot_sdk.booking(time_slot)

def open():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == "__main__":
    Timer(1, open).start()

    app.run()
