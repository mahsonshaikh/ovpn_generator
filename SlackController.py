import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import requests


load_dotenv()
slack_token = os.getenv('SLACK_BOT_TOKEN')

# Initialize the Slack client
client = WebClient(token=slack_token)

class SlackController:
    def __init__(self):
        pass
    
    def upload_file(self, username, user_id):
      ovpn_file_path = './general.ovpn'
      ovpn_crt_file_path = './ca.crt'
      qr_file_path = f'./{username}_qr.png'

      print("This is the Member:" + user_id)
      response = client.conversations_open(users=[user_id])
      # Channel to send the file to
      CHANNEL_ID = response['channel']['id']
      # channel_id = 'YOUR_CHANNEL_ID'
      # print(user_id)

      try:
  
        with open(ovpn_file_path, 'r') as file_raw:
            file_content = file_raw.read()
            response = client.files_upload_v2(
                channel=CHANNEL_ID,
                filename=ovpn_file_path,
                title='File Upload',
                initial_comment='OVPN FILE',
                content=str(file_content)
            )   

        with open(qr_file_path, 'rb') as file_raw:
          file_content = file_raw.read()
          response = client.files_upload_v2(
              channel=CHANNEL_ID,
              filename=qr_file_path,
              title='File Upload',
              initial_comment='QR CODE',
              content=file_content
          )  

          
        print(f"File uploaded successfully: {response['file']['permalink']}")
      except FileNotFoundError:
          print("Error: The file path does not exist.")
      except SlackApiError as e:
          print(f"Error uploading file: {e.response['error']}")
      except Exception as e:
          print(f"An unexpected error occurred: {e}")
