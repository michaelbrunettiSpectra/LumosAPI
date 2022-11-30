import icecubeAPI
import requestLibrary
import lumosHelperFuncs
import libraryInfo


# Setup
library = requestLibrary.requestObject(libraryInfo.libraryIp)

def test_partitionDelete():
    partitionDelete = library.deleteRequest(icecubeAPI.deletePartition())
    assert partitionDelete[1] == 201
    statusPolling = lumosHelperFuncs.statusPoller(lambda: library.getRequest(icecubeAPI.getLibraryStatus()))
    assert statusPolling is True
    taskDelete = library.getRequest(icecubeAPI.getSpecificTask(partitionDelete[0]['taskID']))
    assert taskDelete[1] == 200
    assert taskDelete[0]["state"] == "SUCCESSFUL"
