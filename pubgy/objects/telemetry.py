import time


class Telemetry:
    # would love to use a dataclass, but need to remain backwards compat with 3.5 (for now)
    # todo: add method to match requests to enable automatic retrieval of telemetry data
    def __init__(self, url, data=None):
        """

        :param url:
        :param data:
        """
        self._url = url
        self._data = data
        self._events = []

    def calculate_events(self):
        """

        :return:
        """
        for item in self._data["data"]:
            if self._data["events"].get(item["_T"]) is None:
                self._data["events"][item["_T"]] = []
            self._data["events"][item["_T"]].append(item)
        return self._data["events"]

    @property
    def url(self):
        return self._url

    def set_data(self, data):
        self._data = {"events": {}, "data": data, "sorted": False}

    @property
    def events(self):
        """

        :return:
        """
        return self._check_if_exist("events")


    def _check_if_exist(self, info):
        """

        :return:
        """
        if info.lower() == "events":
            if self._data.get(info) is {}:
                return self._data[info]
            else:
                return self.calculate_events()
        if self._data["sorted"]:
            return self._data[info]
        elif self._data["sorted"] is False:
            self.calculate_events()

