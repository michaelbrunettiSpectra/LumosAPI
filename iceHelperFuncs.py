

def fullSlots(inventory):
    return [storageElement for storageElement in inventory[0]["value"] if "mediaBarcode" in storageElement]

def emptySlots(inventory):
    return [storageElement for storageElement in inventory[0]["value"] if "mediaBarcode" not in storageElement]

