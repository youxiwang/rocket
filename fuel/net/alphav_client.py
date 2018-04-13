'''
Created on Apr 12, 2018

@author: youxiwang

'''
from collections import OrderedDict
from pprint import pprint
from requests import codes
from requests import get

BASE_URL = "https://www.alphavantage.co/query"

class AlphavClient():
    """AlphaVClient"""

    def __init__(self, api_key="6WOFTO637JF2AEY1"):
        self._api_key = api_key
    
    def __Query(self, params):
        full_params = params.copy()
        full_params.update({"apikey": self._api_key})

        try:
            response = get(BASE_URL, params=full_params)
            response_j = response.json()
        except ValueError as err:
            print("Fail to parse response: {0}".format(err))
            raise err
        else:
            if response.status_code != codes.ok:
                error_msg = "unknown" 
                if ("Error Message") in response_j:
                    error_msg = response_j["Error Message"]
                raise Exception("Request failed: {0}".format(error_msg))
            
            return response_j
                
    def TimeSeriesDailyAdjusted(self, symbol, outputsize="compact", 
                                datatype="json"):
        params = {"function": "TIME_SERIES_DAILY_ADJUSTED",
                  "symbol": symbol,
                  "outputsize": outputsize,
                  "datatype": datatype}
        
        return self.__Query(params)          

class TimeSeries():
    def __init__(self, response):
        self.meta_data = response["Meta Data"]
        # assume 2nd key is the time series
        time_series_key = list(response.keys())[1]
        self.series = OrderedDict(response[time_series_key])

if __name__ == "__main__":
    alphavClient = AlphavClient()
    result_j = alphavClient.TimeSeriesDailyAdjusted("goog")
    time_series = TimeSeries(result_j)
    pprint(time_series.series)
    