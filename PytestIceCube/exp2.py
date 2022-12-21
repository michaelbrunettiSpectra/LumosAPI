import icecubeAPI
import requestLibrary
import libraryInfo
import lumosHelperFuncs

def main():
    library = requestLibrary.requestObject(libraryInfo.libraryIp)

    # Perform slot to slot move
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    src = lumosHelperFuncs.fullElement(inventoryRequestBefore[0], "SLOT")
    dest = lumosHelperFuncs.emptyElement(inventoryRequestBefore[0], "SLOT")
    moveRequest = library.postRequest(icecubeAPI.postMove(src, dest))
    print(moveRequest)
    pollingMove = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(moveRequest[0]['taskID'])))
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest[0]['taskID']))
    print(moveStatus)
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore[0], inventoryRequestAfter[0], src, dest)
    print(inventoryVerification)

    # Perform slot to drive move
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    src = lumosHelperFuncs.fullElement(inventoryRequestBefore[0], "SLOT")
    dest = lumosHelperFuncs.emptyElement(inventoryRequestBefore[0], "DRIVE")
    moveRequest = library.postRequest(icecubeAPI.postMove(src, dest))
    print(moveRequest)
    pollingMove = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(moveRequest[0]['taskID'])))
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest[0]['taskID']))
    print(moveStatus)
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore[0], inventoryRequestAfter[0], src, dest)
    print(inventoryVerification)


    # Perform drive to slot move
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    src = lumosHelperFuncs.fullElement(inventoryRequestBefore[0], "DRIVE")
    dest = lumosHelperFuncs.emptyElement(inventoryRequestBefore[0], "SLOT")
    moveRequest = library.postRequest(icecubeAPI.postMove(src, dest))
    print(moveRequest)
    pollingMove = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(moveRequest[0]['taskID'])))
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest[0]['taskID']))
    print(moveStatus)
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore[0], inventoryRequestAfter[0], src, dest)
    print(inventoryVerification)
    
    # Queue up slot to drive, drive to slot, cancel drive to slot -> then reissue drive to slot
    # slot to drive
    print("____Move #1: Slot to Drive____")
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    src = lumosHelperFuncs.fullElement(inventoryRequestBefore[0], "SLOT")
    dest = lumosHelperFuncs.emptyElement(inventoryRequestBefore[0], "DRIVE")
    moveRequest = library.postRequest(icecubeAPI.postMove(src, dest))
    print(moveRequest)

    # drive to slot queue - post move, but swap dest and src
    print("____Move #2: Drive to Slot Deleted____")
    moveRequestQueue = library.postRequest(icecubeAPI.postMove(dest, src))
    # delete move
    deleteRequest = library.putRequest(icecubeAPI.putAbortMove(moveRequestQueue[0]['taskID']))
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequestQueue[0]['taskID']))
    print(deleteRequest)
    print(moveStatus)

    # Poll original move
    print("____Move #1: Polling original move____")
    pollingMove = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(moveRequest[0]['taskID'])))
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest[0]['taskID']))
    print(moveStatus)
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore[0], inventoryRequestAfter[0], src, dest)
    print(f"Inventory Verification: {inventoryVerification}")

    # Issue same drive to slot move
    print("____Move #3: Reissue original move____")
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    sameMoveRequest = library.postRequest(icecubeAPI.postMove(dest, src))
    pollingMove = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(sameMoveRequest[0]['taskID'])))
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(sameMoveRequest[0]['taskID']))
    print(moveStatus)
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore[0], inventoryRequestAfter[0], dest, src)
    print(f"Inventory Verification: {inventoryVerification}")

if __name__ == "__main__":
    main()