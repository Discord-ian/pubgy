def order_by_time(telemetry):
    """

    :param telemetry: Telemetry Object
    :return:
    """
    full_list = []
    for event in telemetry["data"]:
        for item in telemetry["data"][event]:
            full_list.append(item)
    return full_list.sort(key=lambda x: x["_D"])
