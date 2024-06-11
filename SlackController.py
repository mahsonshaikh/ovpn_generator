import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv


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

      # Channel to send the file to
      # channel_id = 'YOUR_CHANNEL_ID'

      try:
          # Upload the file
          response_ovpn_file = client.files_upload_v2(
              channels=user_id,
              file=ovpn_file_path,
              title="OVPN FILE"
          )

          response_crt_file = client.files_upload_v2(
              channels=user_id,
              file=ovpn_crt_file_path,
              title="CA CRT FILE"
          )

          response_qr = client.files_upload_v2(
            channels=user_id,
            file=qr_file_path,
            title="CA CRT FILE"
        )
          assert response_ovpn_file["file"]  # Verify the file upload was successful
          print(f"File uploaded successfully: {response_ovpn_file['file']['permalink']}")

          assert ovpn_crt_file_path["file"]  # Verify the file upload was successful
          print(f"File uploaded successfully: {ovpn_crt_file_path['file']['permalink']}")

          assert response_qr["file"]  # Verify the file upload was successful
          print(f"File uploaded successfully: {response_qr['file']['permalink']}")

      except SlackApiError as e:
          print(f"Error uploading file: {e.response['error']}")