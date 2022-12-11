import icecubeAPI
import requestLibrary
import libraryInfo
import lumosHelperFuncs

def main():
    library = requestLibrary.requestObject(libraryInfo.libraryIp)
    # Perform slot to drive move
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    src = lumosHelperFuncs.fullElement(inventoryRequestBefore[0], "SLOT")
    dest = lumosHelperFuncs.EmptyElement(inventoryRequestBefore[0], "DRIVE")
    moveRequest = library.postRequest(icecubeAPI.postMove(src, dest))
    print(moveRequest)
    pollingMove = lumosHelperFuncs.taskPoller(lambda: library.getRequestDownload(icecubeAPI.getSpecificTask(moveRequest['taskID'])))
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest['taskID']))
    print(moveStatus)
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore, inventoryRequestAfter, src, dest)
    print(inventoryVerification)


if __name__ == "__main__":
    main()