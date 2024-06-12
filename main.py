from flask import Flask, request, jsonify
from ConvertImageToPNG import convertImageToPng
import os
import json
import requests
import subprocess
from SlackController import SlackController
import time
import threading

app = Flask(__name__)
slack_controller = SlackController()


@app.route('/testapp')
def test_data():
    return "APP is working"



@app.route('/slack/events', methods=["POST"])
def slack_events():
    # Running a simple command, e.g., 'ls'
    data = request.form

    if data.get("command") == "/testapp":
        trigger_id = data.get("trigger_id")
        username = data.get("user_name")
        user_id = data.get('user_id')
        print(f"{username} now running subprocess")
        command = f'google-authenticator --time-based --disallow-reuse --force --rate-limit=3 --rate-time=30 --window-size=3 -l "{username}@dc-test.net" -s /etc/openvpn/otp/{username}.google_authenticator --quiet'
        time.sleep(5)
        
        result = subprocess.run(command, shell=True, check=True)
        print(f"{username} has now run subprocess")
        convertImageToPng(username=username)
        slack_thread = threading.Thread(target=slack_controller.upload_file, args=(username, user_id))
        slack_thread.start()
        # Printing the output and the return code
        print(result.stdout)
        print("Return code:", result.returncode)
        return "Files are uploaded"




        # username_full = helper.format_username(username)
        # result = open_modal(trigger_id, username_full)
        return '', 200
    return "Command if found!"
    # payload = json.loads(request.form["payload"])
    # username = payload['user']['username']
    # user_id = payload['user']['user_id']
    
    


@app.route('/slack/interactivity', methods=['POST'])
def interactivity():
    
    return jsonify({"response_action": "clear"})
# print(temporary_data)


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)