import random
import time
import paramiko

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

# Gets the mediaBarcode at a specific address if it exists. Used in function inventoryComparison
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
#ex. lambda: icb_14.getRequest(icecubeAPI.getSpecificTask(logGather[0]["taskID"])) - function object
def taskPoller(requestFunc):
    print("Polling started")
    while True:
        status = requestFunc()
        if status[0]["state"] == "RUNNING":
            time.sleep(10)
            print("Polling in progress")
        else:
            print("Polling completed")
            return True

# requestFunc = lambda + getLibraryStatus request
#ex. lambda: icb_14.getRequest(icecubeAPI.getLibraryStatus()) - function object
def statusPoller(requestFunc):
    print("Polling started")
    while True:
        status = requestFunc()
        if status[0]["ready"] == "Library degraded":
            print("Library degraded")
            return False
        elif status[0]["ready"] is True:
            print("Initialization finished")
            return True
        else:
            print("Initializing")
            time.sleep(10)

# Uses the function getCurrentPackage() request in {libraryType}API.py module to get firmware versions per application.
# This converts applications into their associated component type and creates a tuple of component type and version.
# This is used with function firmwareCheck which compares FRU reported FWs to Application FWs.
def convertedApplicationToFirmwareVersions(firmwareList):
    componentList = []
    for component in firmwareList["firmware"]:
        if component["name"] == "dip-e":
            componentList.append(('DRIVE', component['version']))
        if component["name"] == "motion":
            componentList.append(('ROBOT', component['version']))
        if component["name"] == "esw":
            componentList.append(('NETWORK_SWITCH', component['version']))
        if component["name"] == "pmm":
            componentList.append(('PMM', component['version']))
            componentList.append(('POWER_SUPPLY', component['version']))
        if component["name"] == "lumos":
            componentList.append(('LS', component['version']))
    return componentList

# Uses the function getFruAllMetaData() request in {libraryType}API.py module to get firmware versions from FRUs.
# This returns a list of tuples of FRU type and firmware version.
# This is used with function firmwareCheck which compares FRU reported FWs to Application FWs.
def firmwareFruList(fruList):
    return [(fru["type"], formatter(fru["fruFirmware"])) for fru in fruList["value"]]

def availableFruList(fruList):
    return [fru["type"] for fru in fruList["value"]]

# This takes the output of function firmwareFruList and formats it to match the output of function convertedApplicationToFirmwareVersions
def formatter(firmwareVersion):
    charString = ""
    charGroup = ""
    count = 1
    for char in firmwareVersion:
        # a group consists of chars ending with ".", unless it is the last group in the firmware version
        if char == ".":
            charGroup += char
            # This is a group of chars that leads with a 0, exclude leading 0 from firmware string
            if len(charGroup) > 2 and charGroup[0] == "0":
                charString += charGroup[1:]
            # No leading 0 OR 0 is the only character in the group
            else:
                charString += charGroup
            charGroup = ""
            count += 1
        # This is the last character in the firmware string
        elif count == len(firmwareVersion):
            charGroup += char
            # This is a group of chars that leads with a 0, exclude leading 0 from firmware string
            if len(charGroup) >= 2 and charGroup[0] == "0":
                charString += charGroup[1:]
            # No leading 0 OR 0 is the only character in the group
            else:
                charString += charGroup
        # Keep adding chars to a group unless one of the above conditions is met
        else:
            charGroup += char
            count += 1
    return charString

# This compares the application reported firmware to the firmware being reported on FRUs
def firmwareCheck(fruFirmware, actualFirmware):
    mismatchedFirmware = []
    for fruFw in fruFirmware:
        match = False
        for actualFw in actualFirmware:
            if fruFw == actualFw:
                match = True
                break
        if match is False:
            mismatchedFirmware.append(fruFw)
    if not mismatchedFirmware:
        return True
    else:
        return mismatchedFirmware

# This returns whether an application - "motion", "loglib", "lumos", "dip-e", "mysqld" is active or not.
def systemCtlStatus(host, username, password, application):
    host = "10.10.11.156"
    username = "root"
    password = ""
    command = f"systemctl status {application}"
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    stdin, stdout, stderr = client.exec_command(command)
    response = str(stdout.read())
    client.close()
    if "active (running)" in response:
        return True

