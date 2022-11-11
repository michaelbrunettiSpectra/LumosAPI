import requests
import json

import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class requestObject:
    def __init__(self, ip_address):
        self.url = f"https://{ip_address}:443/api"
        self.token = self.postToken()
        self.requestHeader = {'Authorization': 'Bearer {}'.format(self.token)}

    def postToken(self):
        api = "/tokens"
        payload = {"username": "su",
                   "password": "spectra",
                   "domain": "NATIVE"}
        header = {"accept": "application/json", "Content-Type": "application/json"}
        auth_token = requests.post(self.url+api, data=json.dumps(payload), headers=header, verify=False)
        print(f"Post Token Status Code: {auth_token.status_code}")
        return json.loads(auth_token.text)['token']

    def renewToken(self):
        print("Renewing Token, Retry Command")
        self.token = self.postToken()
        self.requestHeader = {'Authorization': 'Bearer {}'.format(self.token)}

    def getRequest(self, requestFunc):
        api = requestFunc
        r = requests.get(self.url + api, headers=self.requestHeader, verify=False)
        print(f"Request Status Code: {r.status_code}")
        if r.status_code == 401:
            self.renewToken()
            r = requests.get(self.url + api, headers=self.requestHeader, verify=False)
            print(f"Request Status Code: {r.status_code}")
        return json.loads(r.text), r.status_code

    def postRequest(self, requestFunc):
        # If post request with body
        if type(requestFunc) == tuple:
            api = requestFunc[0]
            payload = requestFunc[1]
            r = requests.post(self.url + api, data=json.dumps(payload), headers=self.requestHeader, verify=False)
        else:
            api = requestFunc
            r = requests.post(self.url + api, headers=self.requestHeader, verify=False)
        print(f"Request Status Code: {r.status_code}")
        if r.status_code == 401:
            self.renewToken()
            if type(requestFunc) == tuple:
                r = requests.post(self.url + api, data=json.dumps(payload), headers=self.requestHeader, verify=False)
            else:
                r = requests.post(self.url + api, headers=self.requestHeader, verify=False)
            print(f"Request Status Code: {r.status_code}")
        return json.loads(r.text), r.status_code



def get_magazines(magazineBarcode=None):
    if magazineBarcode is None:
        api = "/magazines"
    else:
        api = f"/magazines/{magazineBarcode}"
    return api

def postMove(sourceAddress, destinationAddress):
    api = "/moves"
    body = {
        "destAddress": destinationAddress,
        "sourceAddress": sourceAddress,
        "type": "MEDIA",
        "partition": "Auto Partition"
    }
    return api, body

def postSelfTest():
    return "/library/diagnostics/SELF_TEST"

def main():
    ip_address = "10.10.11.8"
    icb_14 = requestObject(ip_address)


if __name__ == "__main__":
    main()