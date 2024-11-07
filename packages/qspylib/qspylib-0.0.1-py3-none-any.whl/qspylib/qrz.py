# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import requests
import html
import xmltodict
from qspylib.logbook import Logbook

class QRZInvalidSession(Exception):
    def __init__(self, message="Got no session key back. This session is invalid."):
        self.message=message
        super().__init__(self, message)



class QRZLogbookAPI:
    """
    API wrapper for a QRZ Logbook. At present, only handles fetching QSOs.
    Fetching returns a Logbook object that must be assigned to something.
    """

    def __init__(self, key: str):
        self.key = key
        self.base_url = "https://logbook.qrz.com/api"
        self.headers = {
            'User-Agent': 'pyQSP/0.0.1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

    def fetch_logbook(self):
        params = {
            'KEY': self.key,
            'ACTION': 'FETCH',
            'OPTION': ''
        }
        # filter down to only used params
        params = {k: v for k, v in params.items() if v is not None}
        
        response = requests.get(self.base_url, params=params, headers=self.headers)
        if response.status_code == 200:
            return QRZLogbookAPI.__stringify(self, response.text)
        else:
            response.raise_for_status()

    def insert_record(self, adif, option=None):
        raise NotImplementedError
    
    def delete_record(self, list_logids: list):
        raise NotImplementedError
    
    def check_status(self, list_logids: list):
        raise NotImplementedError
    

    
    ### Helpers

    def __stringify(self, adi_log):
        qrz_output = html.unescape(adi_log)
        start_of_log, end_of_log = qrz_output.index('ADIF=') + 5, qrz_output.rindex('<eor>\n\n') + 4
        log_adi = "<EOH>" + qrz_output[start_of_log:end_of_log] #adif_io expects a header, so we're giving it an end of header
        return Logbook(self.key, log_adi)
    
class QRZXMLInterface:
    """
    A wrapper for the QRZ XML interface.
    This functionality requires being logged in and maintaining a session.
    """

    def __init__(self, username:str=None, password:str=None):
        self.username = username,
        self.password = password,
        self.agent = 'pyQSP/0.0.1'
        self.session_key = None
        self.base_url = "https://xmldata.qrz.com/xml/1.34/"
        self.headers = {
            'User-Agent': self.agent,
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

        self.__initiate_session()

    def __initiate_session(self):
        """Helper -- Grab us a session key so we're not throwing around passwords"""
        params = {'username': self.username,
                  'password': self.password,
                  'agent': self.agent}

        response = requests.get(self.base_url, params=params, headers=self.headers)
        xml_dict = xmltodict.parse(response.text)
        key = xml_dict["QRZDatabase"]["Session"].get("Key")
        if not key:
            raise QRZInvalidSession()
        else:
            self.session_key = key

    def __verify_session(self):
        """ Helper -- Verify our session key is still valid."""
        params = {'agent': self.agent,
                  's': self.session_key}

        response = requests.get(self.base_url, params=params, headers=self.headers)
        if not xmltodict.parse(response.text)["QRZDatabase"]["Session"].get("Key"):
            raise QRZInvalidSession()


