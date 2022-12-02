import icecubeAPI
import requestLibrary
import libraryInfo

# Setup
library = requestLibrary.requestObject(libraryInfo.libraryIp)

def test_apiSpec():
    apiSpecDoc = library.getRequest(icecubeAPI.getAPIDoc())
    assert apiSpecDoc[1] == 200