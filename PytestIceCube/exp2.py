import icecubeAPI
import requestLibrary
import libraryInfo
import lumosHelperFuncs
import tarfile

def unzipLogs(logFileName):
    file = tarfile.open(logFileName)
    file.extractall(('./unzippedLogs'))
    file.close()

def main():
    logFileName = "Logs_2022-12-02T16_29_27.tar.gz"
    unzipLogs(logFileName)


if __name__ == "__main__":
    main()