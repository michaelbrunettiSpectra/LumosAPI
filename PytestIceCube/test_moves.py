import icecubeAPI
import requestLibrary
import lumosHelperFuncs
import libraryInfo

# Setup
library = requestLibrary.requestObject(libraryInfo.libraryIp)

def test_slotToSlotMove():
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    src = lumosHelperFuncs.fullElement(inventoryRequestBefore[0], "SLOT")
    dest = lumosHelperFuncs.emptyElement(inventoryRequestBefore[0], "SLOT")
    moveRequest = library.postRequest(icecubeAPI.postMove(src, dest))
    assert moveRequest[1] == 202
    taskPolling = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(moveRequest[0]['taskID'])))
    assert taskPolling is True
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest[0]['taskID']))
    assert moveStatus[0]['state'] == 'SUCCEEDED'
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore[0], inventoryRequestAfter[0], src, dest)
    assert inventoryVerification is True

def test_slotToDriveMove():
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    src = lumosHelperFuncs.fullElement(inventoryRequestBefore[0], "SLOT")
    dest = lumosHelperFuncs.emptyElement(inventoryRequestBefore[0], "DRIVE")
    moveRequest = library.postRequest(icecubeAPI.postMove(src, dest))
    assert moveRequest[1] == 202
    taskPolling = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(moveRequest[0]['taskID'])))
    assert taskPolling is True
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest[0]['taskID']))
    assert moveStatus[0]['state'] == 'SUCCEEDED'
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore[0], inventoryRequestAfter[0], src, dest)
    assert inventoryVerification is True

def test_driveToSlotMove():
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    src = lumosHelperFuncs.fullElement(inventoryRequestBefore[0], "DRIVE")
    dest = lumosHelperFuncs.emptyElement(inventoryRequestBefore[0], "SLOT")
    moveRequest = library.postRequest(icecubeAPI.postMove(src, dest))
    assert moveRequest[1] == 202
    taskPolling = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(moveRequest[0]['taskID'])))
    assert taskPolling is True
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest[0]['taskID']))
    assert moveStatus[0]['state'] == 'SUCCEEDED'
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore[0], inventoryRequestAfter[0],src, dest)
    assert inventoryVerification is True

def test_deleteMove():
    # slot to drive
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    src = lumosHelperFuncs.fullElement(inventoryRequestBefore[0], "SLOT")
    dest = lumosHelperFuncs.emptyElement(inventoryRequestBefore[0], "DRIVE")
    moveRequest = library.postRequest(icecubeAPI.postMove(src, dest))
    assert moveRequest[1] == 202

    # drive to slot move, delete move in queue- post move, but swap dest and src
    moveRequest2 = library.postRequest(icecubeAPI.postMove(dest, src))
    deleteRequest = library.putRequest(icecubeAPI.putAbortMove(moveRequest2[0]['taskID']))
    assert deleteRequest[1] == 202
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest2[0]['taskID']))
    assert moveStatus[0]['state'] == 'ABORTED'

    # Poll original move
    taskPolling = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(moveRequest[0]['taskID'])))
    assert taskPolling is True
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest[0]['taskID']))
    assert moveStatus[0]['state'] == 'SUCCEEDED'
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore[0], inventoryRequestAfter[0], src, dest)
    assert inventoryVerification is True

    # Issue same drive to slot move that was deleted
    inventoryRequestBefore = library.getRequest(icecubeAPI.getInventory())
    moveRequest3 = library.postRequest(icecubeAPI.postMove(dest, src))
    assert moveRequest3[1] == 202
    taskPolling = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(moveRequest3[0]['taskID'])))
    assert taskPolling is True
    moveStatus = library.getRequest(icecubeAPI.getSpecificMove(moveRequest3[0]['taskID']))
    assert moveStatus[0]['state'] == 'SUCCEEDED'
    inventoryRequestAfter = library.getRequest((icecubeAPI.getInventory()))
    inventoryVerification = lumosHelperFuncs.inventoryComparison(inventoryRequestBefore[0], inventoryRequestAfter[0], dest, src)
    assert inventoryVerification is True
