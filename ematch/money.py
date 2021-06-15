"""
from rave_python import Rave, RaveExceptions, Misc
rave = Rave("FLWPUBK-a84b67198d340a7fdf94426256026503-X", "FLWSECK-cf767206dec44c4b415e4278c6a3f4a9-X", usingEnv=False, production=True)
id = "00152431"
txRef = Misc.generateTransactionReference(id)
payload = {
    "amount": "5",
    "email": "phaisalsey6@gmail.com",
    "phonenumber": "0249141809",
    "network": "MTN",
    "txRef": f"{txRef}",
    "IP": "",
    "redirect_url": "http://127.0.0.1:8000/"
}
tx = payload["txRef"]

try:

    res = rave.GhMobile.charge(payload)
    print(res)

except RaveExceptions.TransactionChargeError as e:
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])
"""


"""
headers = {
    # Request headers
    'Authorization': "FLWSECK-e7a67a8c1fb0abf221e02f635941331f-X"
}
body = {
  "otp": "123456",
  "flw_ref": "man",
  "type": "account"

}
url = 'https://api.flutterwave.com/v3/validate-charge'
x = requests.post(url, data=body, headers=headers)
print(x.text)
import uuid, http.client, urllib.parse, base64, uuid,json
import bfa
reference_id = str(uuid.uuid4())
print(reference_id)

try:
    conn = http.client.HTTPSConnection('https://api.flutterwave.com/v3/charges?type=mobile_money_ghana')
    conn.request("POST", "/v1_0/answer?%s" % params, body, headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '20a3c5ea56814e6eb70cb8eeffee72ce'
}
params = urllib.parse.urlencode({
})
body = json.dumps({
  "providerCallbackHost": "https://webhook.site/89bc3e13-9123-48ae-a004-387d0365b508" })
try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
    conn.request("GET", f"/v1_0/apiuser/{reference_id}%s" % params, body, headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read().decode("utf-8")
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '20a3c5ea56814e6eb70cb8eeffee72ce'
}
params = urllib.parse.urlencode({
})
body = json.dumps({
  "providerCallbackHost": "https://webhook.site/89bc3e13-9123-48ae-a004-387d0365b508" })
try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
    conn.request("POST", f"/v1_0/apiuser/{reference_id}/apikey?%s" % params, body, headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read().decode("utf-8")
    print(data)
    name = json.loads(data)
    key = name.get('apiKey')
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))



api_user = reference_id
api_key = key
api_user_and_key = (api_user+':'+api_key).encode()
encoded = base64.b64encode(api_user_and_key).decode()
headers = {
    # Request headers
    'Authorization': 'Basic ' + encoded,
    'Ocp-Apim-Subscription-Key': '20a3c5ea56814e6eb70cb8eeffee72ce',
}
params = urllib.parse.urlencode({})
try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
    conn.request("POST", "/collection/token/?%s" % params, "{body}", headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read().decode('utf-8')
    token = json.loads(data)
    access_token = token.get('access_token')
    print(data)
    print(access_token)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))


token = access_token
reference_id = str(uuid.uuid4())
headers = {
    # Request headersi
    'Authorization': 'Bearer '+ token,
    'X-Reference-Id': reference_id,
    'X-Target-Environment': 'sandbox',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '20a3c5ea56814e6eb70cb8eeffee72ce',
}
params = urllib.parse.urlencode({})
body = json.dumps({
  "amount": "5",
  "currency": "EUR",
  "externalId": "12345",
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "0561400170"
  },
  "payerMessage": "test message",
  "payeeNote": "test note"
})
try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
    conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, body, headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

token = access_token
headers = {
    # Request headersi
    'Authorization': 'Bearer '+ token,
    'X-Reference-Id': reference_id,
    'X-Target-Environment': 'sandbox',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '20a3c5ea56814e6eb70cb8eeffee72ce',
}
params = urllib.parse.urlencode({})
body = json.dumps({
  "amount": "5",
  "currency": "EUR",
  "externalId": "12345",
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "0561400170"
  },
  "payerMessage": "test message",
  "payeeNote": "test note"
})
try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
    conn.request("GET", f"/collection/v1_0/requesttopay/{reference_id}?%s" % params, body, headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))


token = access_token
headers = {
    # Request headersi
    'Authorization': 'Bearer '+ token,
    'X-Target-Environment': 'sandbox',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '20a3c5ea56814e6eb70cb8eeffee72ce',
}
params = urllib.parse.urlencode({})

try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
    conn.request("GET", "/collection//v1_0/account/balance?%s" % params, "{body}", headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))


headers = {
    # Request headers
    'Authorization': 'Bearer' + token,
    'X-Target-Environment': 'sandbox',
    'Ocp-Apim-Subscription-Key': '20a3c5ea56814e6eb70cb8eeffee72ce',
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
    conn.request("GET", "/collection/v1_0/accountholder/msisdn/0561400170/active?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))    
    
    
"""
import numpy as np


A = np.array([[1, 0, 0, 1, 0, 0, 0], [1, -1, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, -1, 0], [472963.52, 0, 0, 2695540, 0, 0, -2221630],
              [472963.52, -450688.68, 0, 2236090, -2687460, 0, 0], [0, 450688.68, -406139, 0, 2264370, -2670810, 0]])

B = np.array([-5.07e10, 1842246504, 0, 4536])

C = np.array([[-1763126.48, -2687460, 0, -450688.68], [0, 2264370, -2670810, 450688.68], [1, -1, 0, -1], [0, 0, -1, 1]])

print(np.linalg.solve(C, B))




















