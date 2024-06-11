import pyotp
import qrcode
from PIL import Image


def convertImageToPng(username):
# Read the secret from the file
  with open(f'/etc/openvpn/otp/{username}.google_authenticator', 'r') as f:
      secret = f.readline().strip()

  # Create the OTP URI
  otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=f"{username}@dc-test.net", issuer_name="OpenVPN")

  # Generate the QR code
  qr = qrcode.make(otp_uri)
  qr_filename = f'{username}_qr.png'
  qr.save(qr_filename)

  # Open and display the QR code
  Image.open(qr_filename).show()