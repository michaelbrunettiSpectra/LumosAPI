

class restApi:
    def __init__(self, ip_address):
        self.url = f"https://{ip_address}:443/api"
        self.token = "Old_Token"
        self.requestHeader = self.token

    def printInfo(self):
        print(self.token)
        print(self.requestHeader)

    def updateToken(self):
        self.token = "New_Token"

def main():
    x = restApi("10.10.11.156")
    x.printInfo()
    x.updateToken()
    x.printInfo()

if __name__ == "__main__":
    main()