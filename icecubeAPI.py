

# Inventory
def getInventory(partition=None, containerType=None, mediaType=None, mediaBarcode=None, offset=None, limit=None):
    parameterList = []
    if partition is not None:
        parameterList.append(f"partition={partition}")
    if containerType is not None:
        parameterList.append(f"containerType={containerType}")
    if mediaType is not None:
        parameterList.append(f"mediaType={mediaType}")
    if mediaBarcode is not None:
        parameterList.append(f"mediaBarcode={mediaBarcode}")
    if offset is not None:
        parameterList.append(f"offset={offset}")
    if limit is not None:
        parameterList.append(f"limit={limit}")
    if not parameterList:
        return "/inventory"
    else:
        if len(parameterList) == 1:
            return f"/inventory?{parameterList[0]}"
        else:
            api = "/inventory?"
            for parameter in parameterList:
                api += parameter + "&"
            return api.rstrip("&")

def getSpecificInventory(address, partition=None):
    if partition is None:
        return f"/inventory/{address}"
    else:
        return f"/inventory/{address}?partition={partition}"
# action = RESET,
def postInventoryAction(action):
    return f"/inventory/actions/{action}"

# Magazines
def getMagazines(magazineBarcode=None):
    if magazineBarcode is None:
        return "/magazines"
    else:
        return f"/magazines/{magazineBarcode}"


# Moves
def postMove(sourceAddress, destinationAddress):
    api = "/moves"
    body = {
        "destAddress": destinationAddress,
        "sourceAddress": sourceAddress,
        "type": "MEDIA",
        "partition": "Auto Partition"
    }
    return api, body


# Library
def getLibrary():
    return "/library"

def getLibraryStatus():
    return "/library/status"
# action = POWER_OFF,
def postLibraryAction(action):
    return f"/library/actions/{action}"

# Library - Diagnostics
def postSelfTest():
    return "/library/diagnostics/SELF_TEST"

def getSelfTestStatus(taskID):
    return f"/library/diagnostics/SELF_TEST/{taskID}"

# Partitions
def getPartitions(offset=None, limit=None):
    parameterList = []
    if offset is not None:
        parameterList.append(f"offset={offset}")
    if limit is not None:
        parameterList.append(f"limit={limit}")
    if not parameterList:
        return f"/partitions"
    else:
        if len(parameterList) == 1:
            return f"/partitions?{parameterList[0]}"
        else:
            api = "partitions?"
            for parameter in parameterList:
                api += parameter + "&"
            return api.rstrip("&")

def getSpecificPartition(partition):
    return f"/partitions/{partition}"

def deletePartition():
    return "/partitions"

