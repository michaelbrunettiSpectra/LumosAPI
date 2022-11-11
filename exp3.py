
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

def main():
    request = getPartitions(limit=35)
    print(request)
if __name__ == "__main__":
    main()