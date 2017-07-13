import os
from flask import Flask, request
from twilio.jwt.access_token import AccessToken, VoiceGrant
from twilio.rest import Client
import twilio.twiml

ACCOUNT_SID = 'ACad4dc3b3ee78bebe28ff14c9aab76924'
API_KEY = 'SK455717a4b500be5de60aff4545ecfd80'
API_KEY_SECRET = '9YLtI2VtY4ORCl18IyWHyGSJrULqQb1F'
PUSH_CREDENTIAL_SID = 'CR0fb82f909db067e5bc5e5ee9ab3b8c0a'
APP_SID = 'AP03e968e9ae3d0fd3ecdd9539cc219125'

app = Flask(__name__)

@app.route('/accessToken/<myId>')
def token(myId):
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)
  push_credential_sid = os.environ.get("PUSH_CREDENTIAL_SID", PUSH_CREDENTIAL_SID)
  app_sid = os.environ.get("APP_SID", APP_SID)
  grant = VoiceGrant(
    push_credential_sid=push_credential_sid,
    outgoing_application_sid=app_sid
  )
  token = AccessToken(account_sid, api_key, api_key_secret, myId)
  token.add_grant(grant)
  return str(token)

@app.route('/outgoing', methods=['GET', 'POST'])
def outgoing():
  resp = twilio.twiml.Response()
  resp.say("Welcome!")
  with resp.dial(callerId='test1') as r:
    r.client(request.values.get('target'))
  return str(resp)
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
