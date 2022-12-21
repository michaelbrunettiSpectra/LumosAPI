import icecubeAPI
import requestLibrary
import lumosHelperFuncs
import libraryInfo

# Setup
library = requestLibrary.requestObject(libraryInfo.libraryIp)
log_paths = ["/version.json", "/can/canA.log", "/can/canC.log", "/dip-e/dip-e.log", "/loglib/loglib.log", "/lumos/lumos.log", "/lumos/security.log", "/lumos/web.log", "/lumos/config.csv", "/lumos/messages.json", "/motion/DbConfig.prop", "/motion/event.db.bz2", "/motion/hydra.db.bz2", "/motion/LoggingConfig_V1.prop", "/motion/LoggingConfig_V2.prop", "/motion/motion.log", "/motion/pools.db", "/motion/SystemConfig.prop", "/mysql/", "/os/system.log"]

def test_logTypes():
    logTypesRequest = library.getRequest(icecubeAPI.getLogType())
    assert logTypesRequest[1] == 200
    assert 'can' in logTypesRequest[0]
    assert 'dip-e' in logTypesRequest[0]
    assert 'loglib' in logTypesRequest[0]
    assert 'lumos' in logTypesRequest[0]
    assert 'motion' in logTypesRequest[0]
    assert 'mysql' in logTypesRequest[0]
    assert 'os' in logTypesRequest[0]

def test_gatherLog():
    gatherLogRequest = library.postRequest(icecubeAPI.postLogGather())
    assert gatherLogRequest[1] == 202
    taskPolling = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(gatherLogRequest[0]['taskID'])))
    assert taskPolling is True
    gatherStatusRequest = library.getRequest(icecubeAPI.getLogGatherStatus(gatherLogRequest[0]['taskID']))
    assert gatherStatusRequest[1] == 200
    assert gatherStatusRequest[0]['state'] == 'SUCCEEDED'
    downloadLogRequest = library.getRequestDownload(icecubeAPI.getLog(gatherLogRequest[0]['taskID']))
    assert downloadLogRequest[1] == 200
    global logName
    logName = downloadLogRequest[0]

def test_getAllGatheredLogs():
    gatheredLogsRequest = library.getRequest(icecubeAPI.getGatheredLogs())
    assert gatheredLogsRequest[1] == 200
    assert gatheredLogsRequest[0]['count'] >= 1

def test_logContents():
    lumosHelperFuncs.unzipLogs(logName)
    logVerification = lumosHelperFuncs.logPathVerification(log_paths)
    assert logVerification is True

