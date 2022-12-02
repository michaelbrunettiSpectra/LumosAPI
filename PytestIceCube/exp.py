import icecubeAPI
import requestLibrary
import lumosHelperFuncs
import libraryInfo
import time

def main():

    library = requestLibrary.requestObject(libraryInfo.libraryIp)
    partitionDelete = library.deleteRequest(icecubeAPI.deletePartition())
    print(f"Delete Status Code: {partitionDelete[1]}")
    taskDelete = library.getRequest(icecubeAPI.getSpecificTask(partitionDelete[0]['taskID']))
    print(f"Task Status Code: {taskDelete[1]}")
    print(f"Task Delete State: {taskDelete[0]['state']}")
    taskPolling = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(partitionDelete[0]['taskID'])))
    print(f"Task Polling: {taskPolling}")
    taskDelete = library.getRequest(icecubeAPI.getSpecificTask(partitionDelete[0]['taskID']))
    print(f"Task Delete State: {taskDelete[0]['state']}")
    time.sleep(30)
    statusPolling = lumosHelperFuncs.statusPoller(lambda: library.getRequest(icecubeAPI.getLibraryStatus()))
    print(f"Status Polling: {statusPolling}")



if __name__ == "__main__":
    main()