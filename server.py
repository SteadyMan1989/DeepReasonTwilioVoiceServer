import os
from flask import Flask, request
from twilio.jwt.access_token import AccessToken, VoiceGrant, IpMessagingGrant
import twilio.twiml

ACCOUNT_SID = 'ACad4dc3b3ee78bebe28ff14c9aab76924'
API_KEY = 'SK455717a4b500be5de60aff4545ecfd80'
API_KEY_SECRET = '9YLtI2VtY4ORCl18IyWHyGSJrULqQb1F'
PUSH_CREDENTIAL_SID = 'CR0fb82f909db067e5bc5e5ee9ab3b8c0a'
APP_SID = 'AP03e968e9ae3d0fd3ecdd9539cc219125'
IPM_SERVICE_SID = 'IS814c74082fd0415a918badc16f341069'

app = Flask(__name__)

@app.route('/accessToken', methods=['GET', 'POST'])
def token():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)
  ipm_service_sid = os.environ.get("IPM_SERVICE_SID", IPM_SERVICE_SID)
  push_credential_sid = os.environ.get("PUSH_CREDENTIAL_SID", PUSH_CREDENTIAL_SID)
  app_sid = os.environ.get("APP_SID", APP_SID)

  device_id = request.values.get('device')
  identity = request.values.get('identity')

  voiceGrant = VoiceGrant(
    push_credential_sid=push_credential_sid,
    outgoing_application_sid=app_sid
  )
  chatGrant = IpMessagingGrant(
    service_sid=ipm_service_sid,
    endpoint_id="DeepReason:{0}:{1}".format(device_id, identity)
  )

  token = AccessToken(account_sid, api_key, api_key_secret, identity)
  token.add_grant(voiceGrant)
  token.add_grant(chatGrant)
  return str(token)

@app.route('/outgoing', methods=['GET', 'POST'])
def outgoing():
  resp = twilio.twiml.Response()
  with resp.dial(callerId='test1') as r:
    r.client(request.values.get('target'))
  return str(resp)
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
