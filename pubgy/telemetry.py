def generate_telemetry(tel_data):
    dataToReturn = {"data": {}}
    for item in tel_data:
        if dataToReturn["data"].get(item["_T"]) is None:
            dataToReturn["data"][item["_T"]] = []
        dataToReturn["data"][item["_T"]].append(item)
    return dataToReturn
