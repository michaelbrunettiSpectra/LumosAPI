import icecubeAPI
import requestLibrary
import libraryInfo

# Setup
library = requestLibrary.requestObject(libraryInfo.libraryIp)

def test_magazines():
    magazinesRequest = library.getRequest(icecubeAPI.getMagazines())
    assert magazinesRequest[1] == 200
    assert magazinesRequest[0]['count'] > 0
    # magazineBarcode = the first magazine barcode in the list
    singleMagazineRequest = library.getRequest(icecubeAPI.getMagazines(magazineBarcode=magazinesRequest[0]['value'][0]['barcode']))
    assert singleMagazineRequest[1] == 200

