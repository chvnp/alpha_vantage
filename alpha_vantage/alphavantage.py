try:
    # Python 3 import
    from urllib.request import urlopen
except ImportError:
    # Python 2.* import
    from urllib2 import urlopen

from simplejson import loads


class AlphaVantage:
    """
        This class is in charge of creating a python interface between the Alpha
        Vantage restful API and your python application
    """
    _ALPHA_VANTAGE_API_URL = "http://www.alphavantage.co/query?"

    def __init__(self, key=None):
        if key is None:
            raise ValueError('Get a free key from the alphavantage website')
        self.key = key

    def _data_request(self, url):
        """ Request data from the given url and return it as a json
        object. It raises URLError

        Keyword arguments:
        url -- The url of the service
        """
        response = urlopen(url)
        url_response = response.read()
        json_response = loads(url_response)
        return json_response

    def get_intraday(self, symbol, interval='15min', outputsize='compact'):
        """ Return intraday time series in two json objects as data and
        meta_data. It raises ValueError when problem arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min'
        (default '15min')
        outputsize -- The size of the call, supported values are
        'compact' and 'full; the first returns the last 100 points in the
        data series, and 'full' returns the full-length intraday times
        series, commonly above 1MB (default 'compact')
        """
        _FUNCTION_KEY = "TIME_SERIES_INTRADAY"
        url = "{}function={}&symbol={}&interval={}&outputsize={}&apikey={}\
        ".format(AlphaVantage._ALPHA_VANTAGE_API_URL, _FUNCTION_KEY,  symbol,
                 interval, outputsize, self.key)
        json_response = self._data_request(url)
        if 'Error Message' in json_response:
            raise ValueError('ERROR getting data form api',
                             json_response['Error Message'])
        data = json_response['Time Series ({})'.format(interval)]
        meta_data = json_response['Meta Data']
        return data, meta_data


    def get_daily(self, symbol, outputsize='compact'):
        """ Return daily time series in two json objects as data and
        meta_data. It raises ValueError when problem arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        outputsize -- The size of the call, supported values are
        'compact' and 'full; the first returns the last 100 points in the
        data series, and 'full' returns the full-length intraday times
        series, commonly above 1MB (default 'compact')
        """
        _FUNCTION_KEY = "TIME_SERIES_DAILY"
        url = "{}function={}&symbol={}&outputsize={}&apikey={}".format(
        AlphaVantage._ALPHA_VANTAGE_API_URL, _FUNCTION_KEY,  symbol, outputsize,
        self.key)
        json_response = self._data_request(url)
        if 'Error Message' in json_response:
            raise ValueError('ERROR getting data form api',
                             json_response['Error Message'])
        data = json_response['Time Series (Daily)']
        meta_data = json_response['Meta Data']
        return data, meta_data

    def get_weekly(self, symbol):
        """ Return weekly time series in two json objects as data and
        meta_data. It raises ValueError when problem arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data

        """
        _FUNCTION_KEY = "TIME_SERIES_WEEKLY"
        url = "{}function={}&symbol={}&apikey={}".format(
        AlphaVantage._ALPHA_VANTAGE_API_URL, _FUNCTION_KEY, symbol, self.key)
        json_response = self._data_request(url)
        if 'Error Message' in json_response:
            raise ValueError('ERROR getting data form api',
                             json_response['Error Message'])
        data = json_response['Weekly Time Series']
        meta_data = json_response['Meta Data']
        return data, meta_data

    def get_monthly(self, symbol):
        """ Return monthly time series in two json objects as data and
        meta_data. It raises ValueError when problem arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data

        """
        _FUNCTION_KEY = "TIME_SERIES_MONTHLY"
        url = "{}function={}&symbol={}&apikey={}".format(
        AlphaVantage._ALPHA_VANTAGE_API_URL, _FUNCTION_KEY, symbol, self.key)
        json_response = self._data_request(url)
        if 'Error Message' in json_response:
            raise ValueError('ERROR getting data form api',
                             json_response['Error Message'])
        data = json_response['Monthly Time Series']
        meta_data = json_response['Meta Data']
        return data, meta_data

    def get_sma(self, symbol, interval='60min', time_period=20, series_type='close'):
        """ Return simple moving average time series in two json objects as data and
        meta_data. It raises ValueError when problem arise

        Keyword arguments:
        symbol -- the symbol for the equity we want to get its data
        interval -- time interval between two conscutive values,
        supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
        'weekly', 'monthly' (default '60min')
        time_period -- How many data points to average (default 20)
        series_type -- The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        """
        _FUNCTION_KEY = "SMA"
        url = "{}function={}&symbol={}&interval={}&time_period={}"\
        "&series_type={}&apikey={}".format(AlphaVantage._ALPHA_VANTAGE_API_URL,
        _FUNCTION_KEY, symbol, interval, time_period, series_type, self.key)
        json_response = self._data_request(url)
        if 'Error Message' in json_response or not json_response:
            if json_response:
                raise ValueError('ERROR getting data form api',
                             json_response['Error Message'])
            else:
                raise ValueError('Error getting data from api, no return'\
                 ' message from the api url (possibly wrong symbol/param)')
        print(json_response)
        data = json_response['Technical Analysis: SMA']
        meta_data = json_response['Meta Data']
        return data, meta_data

if __name__ == '__main__':
    av = AlphaVantage(key='486U')
    data, meta_data = av.get_sma('GOOGLX')
    print(data)
