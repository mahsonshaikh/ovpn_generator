from flask import Flask, request, jsonify
from ConvertImageToPNG import convertImageToPng
import os
import json
import requests
import subprocess
from SlackController import SlackController

app = Flask(__name__)
slack_controller = SlackController()


@app.route('/testapp/events', methods=["POST"])
def test_data():
    return "APP is working"



@app.route('/testapp/events', methods=["POST"])
def slack_events():
    # Running a simple command, e.g., 'ls'
    payload = json.loads(request.form["payload"])
    username = payload['user']['username']
    user_id = payload['user']['user_id']
    
    result = subprocess.run([f'google-authenticator --time-based --disallow-reuse --force --rate-limit=3 --rate-time=30 --window-size=3 -l "{username}@dc-test.net" -s /etc/openvpn/otp/mubasit.khan.google_authenticator'], capture_output=True, text=True)
    convertImageToPng(username=username)
    slack_controller.upload_file(username=username, user_id=user_id )
    # Printing the output and the return code
    print(result.stdout)
    print("Return code:", result.returncode)
    return "Command if found!"


@app.route('/slack/interactivity', methods=['POST'])
def interactivity():
    
    return jsonify({"response_action": "clear"})
# print(temporary_data)


if __name__ == '__main__':
    app.run(port=5000)