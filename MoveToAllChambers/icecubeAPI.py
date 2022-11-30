

# ____API DOCUMENT REQUESTS____
def getAPIDoc():
    return "/spec"

# ____FRUS REQUESTS____
# types = DRIVE, ROBOT
def getFruAllMetaData(offset=None, limit=None, types=None):
    parameterList = []
    if offset is not None:
        parameterList.append(f"offset={offset}")
    if limit is not None:
        parameterList.append(f"limit={limit}")
    if types is not None:
        parameterList.append(f"types={types}")
    if not parameterList:
        return "/frus"
    else:
        if len(parameterList) == 1:
            return f"/frus?{parameterList[0]}"
        else:
            api = "/frus?"
            for parameter in parameterList:
                api += parameter + "&"
            return api.rstrip("&")

# typePath ex. Drive:1:3:1
def getFruSingleMetaData(typePath):
    return f"/frus/{typePath}"

# typePath ex. Drive:1:3:1
def getFruStatus(typePath):
    return f"/frus/{typePath}/status"

# typePath ex. Drive:1:3:1, action = RESET
def postFruAction(typePath, action):
    return f"/frus/{typePath}/actions/{action}"

# ____INVENTORY REQUESTS____
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

# ____LOGS REQUESTS____
def getLogType():
    return "/logs/types"

def getGatheredLogs(offset=None, limit=None):
    parameterList = []
    if offset is not None:
        parameterList.append(f"offset={offset}")
    if limit is not None:
        parameterList.append(f"limit={limit}")
    if not parameterList:
        return "/logs"
    else:
        if len(parameterList) == 1:
            return f"/logs?{parameterList[0]}"
        else:
            api = "/logs?"
            for parameter in parameterList:
                api += parameter + "&"
            return api.rstrip("&")

def postLogGather():
    return "/logs"

def getLogGatherStatus(taskID):
    return f"/logs/{taskID}"
# This for log gather download
def getLog(taskID):
    return f"/logs/{taskID}/download"

# ____MAGAZINES REQUESTS____
def getMagazines(magazineBarcode=None):
    if magazineBarcode is None:
        return "/magazines"
    else:
        return f"/magazines/{magazineBarcode}"


# ____MOVES REQUESTS____
def postMove(sourceAddress, destinationAddress):
    api = "/moves"
    body = {
        "destAddress": destinationAddress,
        "sourceAddress": sourceAddress,
        "type": "MEDIA",
        "partition": "Auto Partition"
    }
    return api, body

def getMoves(offset=None, limit=None, partition=None):
    parameterList = []
    if offset is not None:
        parameterList.append(f"offset={offset}")
    if limit is not None:
        parameterList.append(f"limit={limit}")
    if partition is not None:
        parameterList.append(f"partition={partition}")
    if not parameterList:
        return "/moves"
    else:
        if len(parameterList) == 1:
            return f"/moves?{parameterList[0]}"
        else:
            api = "/moves?"
            for parameter in parameterList:
                api += parameter + "&"
            return api.rstrip("&")

def getSpecificMove(taskID):
    return f"/moves/{taskID}"

def putAbortMove(taskID):
    return f"/moves/{taskID}/abort"

# ____LIBRARY REQUESTS____
def getLibrary():
    return "/library"

def getLibraryStatus():
    return "/library/status"
# action = POWER_OFF,
def postLibraryAction(action):
    return f"/library/actions/{action}"

# ____LIBRARY DIAGNOSTICS REQUESTS____
def postSelfTest():
    return "/library/diagnostics/SELF_TEST"

def getSelfTestStatus(taskID):
    return f"/library/diagnostics/SELF_TEST/{taskID}"

def postMoveToAllChambers():
    return "/library/diagnostics/MOVE_TO_CHAMBERS"

# ____MESSAGES REQUESTS____
def getMessages(offset=None, limit=None, id=None, lang=None, startTime=None, endTime=None):
    parameterList = []
    if offset is not None:
        parameterList.append(f"offset={offset}")
    if limit is not None:
        parameterList.append(f"limit={limit}")
    if id is not None:
        parameterList.append(f"id={id}")
    if lang is not None:
        parameterList.append(f"lang={lang}")
    if startTime is not None:
        parameterList.append(f"startTime={startTime}")
    if endTime is not None:
        parameterList.append(f"endTime={endTime}")
    if not parameterList:
        return "/messages"
    else:
        if len(parameterList) == 1:
            return f"/messages?{parameterList[0]}"
        else:
            api = "/messages?"
            for parameter in parameterList:
                api += parameter + "&"
            return api.rstrip("&")


# ____PACKAGE REQUESTS____
def getCurrentPackage():
    return "/packages/active"

# This will start update
def putPackage(packageName):
    api = "/packages/active"
    body = {
        "name": packageName
    }
    return api, body

def getAllPackages(offset=None, limit=None):
    parameterList = []
    if offset is not None:
        parameterList.append(f"offset={offset}")
    if limit is not None:
        parameterList.append(f"limit={limit}")
    if not parameterList:
        return "/packages"
    else:
        if len(parameterList) == 1:
            return f"/packages?{parameterList[0]}"
        else:
            api = "/packages?"
            for parameter in parameterList:
                api += parameter + "&"
            return api.rstrip("&")

def getPackageState():
    return "/packages/state"

# Uploads package to library
def postPackage(packageName, pubkeyName):
    api = "/packages/upload"
    return api, packageName, pubkeyName

def getSpecificPackage(packageName):
    return f"/packages/{packageName}"

def deleteSpecificPackage(packageName):
    return f"/packages/{packageName}"


# ____PARTITIONS REQUESTS____
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

# ____TASKS REQUESTS____
def getTasks(limit=None, state=None, taskType=None, tag=None, startTime=None, endTime=None):
    parameterList = []
    if limit is not None:
        parameterList.append(f"limit={limit}")
    if state is not None:
        parameterList.append((f"state={state}"))
    if taskType is not None:
        parameterList.append((f"taskType={taskType}"))
    if tag is not None:
        parameterList.append(f"tag={tag}")
    if startTime is not None:
        parameterList.append(f"startTime={startTime}")
    if endTime is not None:
        parameterList.append(f"endTime={endTime}")
    if not parameterList:
        return "/tasks"
    else:
        if len(parameterList) == 1:
            return f"/partitions?{parameterList[0]}"
        else:
            api = "partitions?"
            for parameter in parameterList:
                api += parameter + "&"
            return api.rstrip("&")

def getSpecificTask(taskID):
    return f"/tasks/{taskID}"


