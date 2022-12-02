import icecubeAPI
import requestLibrary
import lumosHelperFuncs
import libraryInfo
import time

# Setup
library = requestLibrary.requestObject(libraryInfo.libraryIp)

def test_partitionDelete():
    partitionDelete = library.deleteRequest(icecubeAPI.deletePartition())
    assert partitionDelete[1] == 202
    taskDelete = library.getRequest(icecubeAPI.getSpecificTask(partitionDelete[0]['taskID']))
    assert taskDelete[1] == 200
    assert taskDelete[0]['state'] == "RUNNING"
    taskPolling = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(partitionDelete[0]['taskID'])))
    assert taskPolling is True
    taskDelete = library.getRequest(icecubeAPI.getSpecificTask(partitionDelete[0]['taskID']))
    assert taskDelete[1] == 200
    assert taskDelete[0]['state'] == "SUCCEEDED"
    time.sleep(30)
    statusPolling = lumosHelperFuncs.statusPoller(lambda: library.getRequest(icecubeAPI.getLibraryStatus()))
    assert statusPolling is True

