import icecubeAPI
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():

    libraryIp = "10.10.11.156"
    libraryObject = icecubeAPI.restApi(libraryIp)
    magazineInfo = libraryObject.getMagazines("LUDZO5X")
    print(magazineInfo)


if __name__ == "__main__":
    main()