import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class restApi:
    def __init__(self, ip_address):
        self.url = f"https://{ip_address}:443/api"
        self.token = self.post_token()

    def post_token(self):
        api = "/tokens"
        payload = {"username": "su",
                   "password": "spectra",
                   "domain": "NATIVE"}
        header = {"accept": "application/json", "Content-Type": "application/json"}
        auth_token = requests.post(self.url+api, data=json.dumps(payload), headers=header, verify=False)
        print(f"Post Token Status Code: {auth_token.status_code}")
        return json.loads(auth_token.text)['token']

    def post_security_audit(self):
        api = "/library/diagnostics/SECURITY_AUDIT"
        header = {'Authorization': 'Bearer {}'.format(self.token)}
        security_audit = requests.post(self.url+api, headers=header, verify=False)
        print(f"Security Audit Status Code: {security_audit.status_code}")
        if security_audit.status_code == 401:
            print("Renewing Token, Retry Command")
            self.token = self.post_token()
            return False
        return json.loads(security_audit.text)['taskID']

    def get_tasks(self, task_id):
        api = f"/tasks/{task_id}"
        header = {'Authorization': 'Bearer {}'.format(self.token)}
        tasks = requests.get(self.url+api, headers=header, verify=False)
        print(f"Tasks Status Code: {tasks.status_code}")
        if tasks.status_code == 401:
            print("Renewing Token, Retry Command")
            self.token = self.post_token()
            return False
        return json.loads(tasks.text)

    def get_magazines(self):
        api = "/magazines"
        header = {'Authorization': 'Bearer {}'.format(self.token)}
        magazines = requests.get(self.url+api, headers=header, verify=False)
        print(f"Magazines Status Code: {magazines.status_code}")
        if magazines.status_code == 401:
            print("Renewing Token, Retry Command")
            self.token = self.post_token()
            return False
        return json.loads(magazines.text)["count"]