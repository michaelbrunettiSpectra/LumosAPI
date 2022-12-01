import icecubeAPI
import requestLibrary
import lumosHelperFuncs
import libraryInfo

# Setup
library = requestLibrary.requestObject(libraryInfo.libraryIp)

def test_FruAvailability():
    frusRequest = library.getRequest(icecubeAPI.getFruAllMetaData())
    assert frusRequest[1] == 200
    fruAvailable = lumosHelperFuncs.availableFruList(frusRequest[0])
    assert 'DRIVE' in fruAvailable
    assert 'NETWORK_SWITCH' in fruAvailable
    assert 'PMM' in fruAvailable
    assert 'POWER_SUPPLY' in fruAvailable
    assert 'ROBOT' in fruAvailable
    assert 'LS' in fruAvailable

def test_FruFirmwareVersion():
    frusRequest = library.getRequest(icecubeAPI.getFruAllMetaData())
    assert frusRequest[1] == 200
    appVersionRequest = library.getRequest(icecubeAPI.getCurrentPackage())
    assert appVersionRequest[1] == 200
    fruFirmwareList = lumosHelperFuncs.firmwareFruList(frusRequest[0])
    appFirmwareList = lumosHelperFuncs.convertedApplicationToFirmwareVersions(appVersionRequest[0])
    fruFirmwareCheck = lumosHelperFuncs.firmwareCheck(fruFirmwareList, appFirmwareList)
    assert fruFirmwareCheck is True
