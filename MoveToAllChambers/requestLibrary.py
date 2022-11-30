import requests
import json
import icecubeAPI
import time
import urllib3
from datetime import datetime
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

    def deleteRequest(self, requestFunc):
        api = requestFunc
        r = requests.delete(self.url + api, headers=self.requestHeader, verify=False)
        print(f"Request Status Code: {r.status_code}")
        if r.status_code == 401:
            self.renewToken()
            r = requests.delete(self.url + api, headers=self.requestHeader, verify=False)
            print(f"Request Status Code: {r.status_code}")
        return json.loads(r.text), r.status_code

    def putRequest(self, requestFunc):
        # If put request with body
        if type(requestFunc) == tuple:
            api = requestFunc[0]
            payload = requestFunc[1]
            r = requests.put(self.url + api, data=json.dumps(payload), headers=self.requestHeader, verify=False)
        else:
            api = requestFunc
            r = requests.put(self.url + api, headers=self.requestHeader, verify=False)
        print(f"Request Status Code: {r.status_code}")
        if r.status_code == 401:
            self.renewToken()
            if type(requestFunc) == tuple:
                r = requests.put(self.url + api, data=json.dumps(payload), headers=self.requestHeader, verify=False)
            else:
                r = requests.put(self.url + api, headers=self.requestHeader, verify=False)
            print(f"Request Status Code: {r.status_code}")
        return json.loads(r.text), r.status_code

    def getRequestDownload(self, requestFunc):
        api = requestFunc
        r = requests.get(self.url + api, headers=self.requestHeader, verify=False)
        print(f"Request Status Code: {r.status_code}")
        if r.status_code == 401:
            self.renewToken()
            r = requests.get(self.url + api, headers=self.requestHeader, verify=False)
            print(f"Request Status Code: {r.status_code}")
        with open(f"Logs_{datetime.now().strftime('%Y-%m-%dT%H_%M_%S')}.tar.gz", 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

    def postRequestUpload(self, requestFunc):
        api = requestFunc[0]
        payload = requestFunc[1]
        r = requests.post(self.url + api, data=json.dumps(payload), headers=self.requestHeader, verify=False)
        pass


def main():

    ip_address = "10.10.11.156"
    icb_14 = requestObject(ip_address)
    currentPackage = icb_14.getRequest(icecubeAPI.getCurrentPackage())
    print(currentPackage)
    print("")
    frus = icb_14.getRequest(icecubeAPI.getFruAllMetaData())
    print(frus)


if __name__ == "__main__":
    main()