import icecubeAPI
import requestLibrary
import lumosHelperFuncs
import libraryInfo

def main():

    library = requestLibrary.requestObject(libraryInfo.libraryIp)
    partitionDelete = library.deleteRequest(icecubeAPI.deletePartition())
    print(f"Delete Status Code: {partitionDelete[1]}")
    statusPolling = lumosHelperFuncs.statusPoller(lambda: library.getRequest(icecubeAPI.getLibraryStatus()))
    print(f"Status Polling: {statusPolling}")
    taskDelete = library.getRequest(icecubeAPI.getSpecificTask(partitionDelete[0]['taskID']))
    print(f"Task Status Code: {taskDelete[1]}")
    print(f"Task Delete Status code: {taskDelete[0]['state']}")


if __name__ == "__main__":
    main()