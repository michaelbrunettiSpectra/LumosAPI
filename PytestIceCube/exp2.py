import icecubeAPI
import requestLibrary
import libraryInfo
import lumosHelperFuncs


def main():
    library = requestLibrary.requestObject(libraryInfo.libraryIp)
    magazinesRequest = library.getRequest(icecubeAPI.getMagazines())
    print(magazinesRequest[0]['value'][0]['barcode'])
if __name__ == "__main__":
    main()