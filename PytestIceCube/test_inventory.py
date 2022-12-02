import icecubeAPI
import requestLibrary
import lumosHelperFuncs
import libraryInfo

# Setup
library = requestLibrary.requestObject(libraryInfo.libraryIp)

def test_inventory():
    inventoryRequest = library.getRequest(icecubeAPI.getInventory())
    assert inventoryRequest[1] == 200

def test_inventoryOffset():
    inventoryRequest = library.getRequest(icecubeAPI.getInventory())
    assert inventoryRequest[1] == 200
    offset = inventoryRequest[0]['count'] - 1
    inventoryRequest = library.getRequest((icecubeAPI.getInventory(offset=offset)))
    assert inventoryRequest[1] == 200
    assert len(inventoryRequest[0]['value']) == 1

def test_inventoryLimit():
    inventoryRequest = library.getRequest(icecubeAPI.getInventory(limit=1))
    assert inventoryRequest[1] == 200
    assert len(inventoryRequest[0]['value']) == 1

def test_inventoryContainerType():
    inventoryRequest = library.getRequest(icecubeAPI.getInventory(containerType="SLOT"))
    assert inventoryRequest[1] == 200
    for element in inventoryRequest[0]['value']:
        assert element["address"] >= 4096
    inventoryRequest = library.getRequest(icecubeAPI.getInventory(containerType="DRIVE"))
    assert inventoryRequest[1] == 200
    for element in inventoryRequest[0]['value']:
        assert 256 <= element["address"] <= 271

def test_inventoryMediaType():
    inventoryRequest = library.getRequest(icecubeAPI.getInventory(mediaType="LTO"))
    assert inventoryRequest[1] == 200
    inventoryRequest = library.getRequest(icecubeAPI.getInventory(mediaType="LTO_CLEAN"))
    assert inventoryRequest[1] == 200

def test_inventoryPartition():
    inventoryRequest = library.getRequest(icecubeAPI.getInventory(partition="Auto Partition"))
    assert inventoryRequest[1] == 200
    inventoryRequest = library.getRequest(icecubeAPI.getInventory(partition="Auto Cleaning Partition"))
    assert inventoryRequest[1] == 200

def test_inventoryMediaBarcode():
    inventoryRequest = library.getRequest(icecubeAPI.getInventory())
    assert inventoryRequest[1] == 200
    fullSlot = lumosHelperFuncs.fullSlot(inventoryRequest[0], "SLOT")
    mediaBarcode = lumosHelperFuncs.mediaBarcodeInfo(inventoryRequest[0], fullSlot)
    inventoryRequest = library.getRequest(icecubeAPI.getInventory(mediaBarcode=mediaBarcode))
    assert inventoryRequest[1] == 200
    assert inventoryRequest[0]['count'] == 1
    assert inventoryRequest[0]['value'][0]['mediaBarcode'] == mediaBarcode


