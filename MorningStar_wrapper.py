import json
import requests
from bs4 import BeautifulSoup

class Wrapper:
    """
        Wrapper to return a ticker, based on ISIN input.
        Data from Morningstar.com
    """

    # If True prints some basic feedback from the Wrapper
    debug = False

    def __init__(self, ISIN=''):
        self.ISIN = ISIN.upper()

        if self.ISIN:
            # Opens search URL and returns a Requests-object
            r = self.startConnection()

            # Creates soup and finds the correct result data based on a request-object
            self.makeSoup(r)

    def setISIN(self, ISIN):
        """ Sets the value of ISIN, it's required to set this, either in the __init__ or with this function """
        self.ISIN = ISIN.upper()

    def startConnection(self):
        """ Stars the connection to the search URL and returns a request-object if succeeded """
        PREFIX = 'http://www.morningstar.com/search.html?q='
        search_url = f'{PREFIX}+{self.ISIN}'
        if self.debug:
            print(search_url)
        r = requests.get(search_url)
        if r.status_code == 200:
            return r
        else:
            return None

    def makeSoup(self, request):
        """ Creates a BS object and filters the data we need """
        soup = BeautifulSoup(request.text, 'html.parser')

        for div in soup.find_all('div'):

            # Limit our search to the search results
            if div.get('class') == ['search-list-content']:

                # Check if we  found correct result, containing our ISIN
                if div.get('data-key').strip() == self.ISIN:

                    self.data = div.get('data-initialdata')
                    break

    def getTicker(self):
        """ Returns a ticker based on the filtered data, which is collected in makeSoup() """
        if self.debug:
            print('DATA: ' + self.data)

        myJSON = json.loads(self.data)

        if self.debug:
            print('JSON: ' + str(myJSON))
            print('Result part: ' + str(myJSON['result']))

        new_dict = myJSON['m']

        if self.debug:
            print('NEW DICT: ', end='')
            print(list(new_dict))

        # The ticker is part of a large string, followed by the OS001-tag.
        pos_tag = str(new_dict).find('OS001')
        pos_comma = str(new_dict)[pos_tag:].find(',')

        ticker = str(new_dict)[pos_tag + 9:pos_tag + pos_comma - 1]
        return ticker