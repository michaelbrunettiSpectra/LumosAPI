import lumosHelperFuncs
import libraryInfo

# Setup
libraryIp = libraryInfo.libraryIp
username = libraryInfo.username
password = libraryInfo.password

def test_motion():
    assert lumosHelperFuncs.systemCtlStatus(libraryIp, username, password, "motion") is True

def test_loglib():
    assert lumosHelperFuncs.systemCtlStatus(libraryIp, username, password, "loglib") is True

def test_lumos():
    assert lumosHelperFuncs.systemCtlStatus(libraryIp, username, password, "lumos") is True

def test_dipE():
    assert lumosHelperFuncs.systemCtlStatus(libraryIp, username, password, "dip-e") is True

def test_mysqld():
    assert lumosHelperFuncs.systemCtlStatus(libraryIp, username, password, "mysqld") is True

