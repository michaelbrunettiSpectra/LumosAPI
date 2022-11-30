import icecubeAPI
import requestLibrary
import libraryInfo

# Setup
library = requestLibrary.requestObject(libraryInfo.libraryIp)

# Check 200 response and 2 partitions present - Auto Partition and Auto Clean
def test_partition():
    partitionRequest = library.getRequest(icecubeAPI.getPartitions())
    assert partitionRequest[1] == 200
    assert partitionRequest[0]['count'] == 2

def test_autoPartition():
    partitionRequest = library.getRequest(icecubeAPI.getSpecificPartition("Auto Partition"))
    assert partitionRequest[1] == 200
    assert partitionRequest[0]['name'] == "Auto Partition"
    assert partitionRequest[0]['mediaType'] == "LTO"

def test_cleaningPartition():
    partitionRequest = library.getRequest(icecubeAPI.getSpecificPartition("Auto Cleaning Partition"))
    assert partitionRequest[1] == 200
    assert partitionRequest[0]['name'] == "Auto Cleaning Partition"
    assert partitionRequest[0]['mediaType'] == "LTO_CLEAN"
