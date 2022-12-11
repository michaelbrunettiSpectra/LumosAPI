import icecubeAPI
import requestLibrary
import lumosHelperFuncs

def logger(statement):
    with open('MoveToAllChamberResults.txt', 'a+') as f:
        f.write(statement)
        f.write("\n")


def log_results(task_results):
    for line in task_results:
        logger(line)


def main():
    ipaddress = input("Input IP Address: ")
    loopCount = int(input("Input loop count: "))
    library = requestLibrary.requestObject(ipaddress)
    count = 1
    passedCount = 0
    failedCount = 0
    while loopCount >= count:
        moveToAllChambers = library.postRequest(icecubeAPI.postMoveToAllChambers())
        pollingFunc = lumosHelperFuncs.taskPoller(lambda: library.getRequest(icecubeAPI.getSpecificTask(moveToAllChambers[0]['taskID'])))
        taskResults = library.getRequest(icecubeAPI.getSpecificTask(moveToAllChambers[0]['taskID']))
        logger(f"Test Results #{count}")
        log_results(taskResults[0]["taskLog"])
        for line in taskResults[0]['taskLog']:
            if "Total chambers: " in line:
                if "Failed chambers: 0" in line:
                    passedCount += 1
                    logger(f"Diagnostic Result for Test #{count}: PASSED")
                else:
                    failedCount += 1
                    logger(f"Diagnostic Result for Test #{count}: FAILED")
        logger(f"Loop Count: {count}")
        logger(f"Diagnostic Passed Count: {passedCount}")
        logger(f"Diagnostic Failed Count: {failedCount}")
        print(f"Loop Count {count}")
        count += 1
    if failedCount != 0:
        logger("At least 1 diagnostic had a failed chamber or chambers")
        print("At least 1 diagnostic had a failed chamber or chambers")
    else:
        logger("All diagnostic tests passed with no failed chambers")
        print("All diagnostic tests passed with no failed chambers")
    logger("Script Finished")
    print("Script Finished")


if __name__ == "__main__":
    main()
