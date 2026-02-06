import json

class Config():
    def __init__(self, filename='config.json'):
        self._filename = filename
        try:
            with open(self._filename, 'r') as f:
                saved = json.load(f)
        except FileNotFoundError:
            saved = {
                "displayCode": "epd7in5_V2",
                "refreshRateInSeconds": 5,
                "startDate": '07/01/2024',
                "endDate": '07/31/2024',
                "teamCode": 'min'
            }
            json.dump(saved, open(self._filename, 'w'))
        self._displayCode = saved.get("displayCode", "epd7in5_V2")
        self._refreshRateInSeconds = saved.get("refreshRateInSeconds", 5)
        self._startDate = saved.get("startDate", '07/01/2024')
        self._endDate = saved.get("endDate", '07/31/2024')
        self._teamCode = saved.get("teamCode", 'min')

    def _setConfigValue(self, key, value):
        with open(self._filename, 'r') as f:
            data = json.load(f)
        data[key] = value
        with open(self._filename, 'w') as f:
            json.dump(data, f)

    @property
    def getDisplayCode(self):
        return self._displayCode
    
    def setDisplayCode(self, code):
        self._displayCode = code
        self._setConfigValue("displayCode", code)
    
    @property
    def getRefreshRateInSeconds(self):
        return self._refreshRateInSeconds
    
    def setRefreshRateInSeconds(self, rate):
        self._refreshRateInSeconds = rate
        self._setConfigValue("refreshRateInSeconds", rate)
    
    @property
    def getStartDate(self):
        return self._startDate
    
    def setStartDate(self, date):
        self._startDate = date
        self._setConfigValue("startDate", date)
    
    @property
    def getEndDate(self):
        return self._endDate
    
    def setEndDate(self, date):
        self._endDate = date
        self._setConfigValue("endDate", date)
    
    @property
    def getTeamCode(self):
        return self._teamCode
    
    def setTeamCode(self, code):
        self._teamCode = code
        self._setConfigValue("teamCode", code)
