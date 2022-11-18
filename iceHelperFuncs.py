import random
import time

# Returns the address of a full slot, containerType = "DRIVE" or "SLOT"
def fullSlot(inventory, containerType):
    fullSlots = [storageElement for storageElement in inventory["value"] if "mediaBarcode" in storageElement and storageElement["containerType"] == containerType]
    # No full elements in the list
    if not fullSlots:
        return None
    else:
        return random.choice(fullSlots)["address"]

# Returns the address of an empty slot, containerType = "DRIVE" or "SLOT"
def emptySlot(inventory, containerType):
    emptySlots = [storageElement for storageElement in inventory["value"] if "mediaBarcode" not in storageElement and storageElement["containerType"] == containerType]
    if not emptySlots:
        return None
    else:
        return random.choice(emptySlots)["address"]

# Gets the mediaBarcode at a specific address if it exists
def mediaBarcodeInfo(inventory, storageAddress):
    for storageElement in inventory["value"]:
        if storageElement["address"] == storageAddress:
            try:
                return storageElement["mediaBarcode"]
            except KeyError:
                pass

# Verifies inventory after a move
def inventoryComparison(beforeInventory, afterInventory, srcAddress, destAddress):
    inventoryVerification = 0
    mediaBarcode = mediaBarcodeInfo(beforeInventory, srcAddress)
    for storageElement in afterInventory["value"]:
        # This should no longer have a mediaBarcode
        if storageElement["address"] == srcAddress:
            if "mediaBarcode" not in storageElement:
                inventoryVerification += 1
        # This should have a mediaBarcode and mediaBarcode should match match the srcAddress barcode pre-move
        if storageElement["address"] == destAddress:
            if "mediaBarcode" in storageElement and storageElement["mediaBarcode"] == mediaBarcode:
                inventoryVerification += 1
    if inventoryVerification == 2:
        return True

# requestFunc = lambda + getSpecificTask request
#ex. lambda: icb_14.getRequest(icecubeAPI.getSpecificTask(logGather[0]["taskID"]))
def poller(requestFunc):
    print("Polling started")
    while True:
        status = requestFunc()
        if status[0]["state"] == "RUNNING":
            time.sleep(10)
            print("Polling in progress")
        else:
            print("Polling completed")
            break