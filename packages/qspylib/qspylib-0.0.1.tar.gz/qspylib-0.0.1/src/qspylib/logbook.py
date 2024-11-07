# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import adif_io

class QSO:
    """
    A hambaseio QSO obj. Contains simple info on a QSO.
    """
    def __init__(self, their_call, band, mode, qso_date, time_on, qsl_rcvd='N'): 
        self.their_call = their_call
        self.band = band
        self.mode = mode
        self.qso_date = qso_date
        self.time_on = time_on
        self.qsl_rcvd = qsl_rcvd

    def __str__(self):
        return f"CALL: {self.their_call} BAND: {self.band} MODE: {self.mode} DATE: {self.qso_date} TIME: {self.time_on} QSL: {self.qsl_rcvd}\n"
        # to-do: make this return as an actual adif formattede string

class Logbook:
    """
    A Logbook has both an adi field, holding all fields parsed from an .adi log per QSO, and a simplified log field, holding a simplified set of fields per QSO.
    Interacting with the log field can provide one field to check for if a QSO is confirmed on one or more of: LoTW, eQSL, QRZ, or ClubLog. 
    """

    def __init__(self, callsign: str, unparsed_log: str):
        self.callsign = callsign
        self.adi, self.header = adif_io.read_from_string(unparsed_log)
        self.log = set()
        for contact in self.adi:
            # whether this qsl has been confirmed; lotw & clublog use qsl_rcvd, eqsl uses eqsl_qsl_rcvd, qrz most simply gives a qsl date
            qsl_rcvd, qrz_qsl_dte, eqsl_qsl_rcvd = contact.get('QSL_RCVD'), contact.get('app_qrzlog_qsldate'), contact.get('eqsl_qsl_rcvd')
            qso_confirmed = 'Y' if qsl_rcvd == 'Y' or qrz_qsl_dte or eqsl_qsl_rcvd == 'Y' else 'N'
            # create a QSO for this contact
            self.log.add(QSO(contact['CALL'], contact['BAND'], contact['MODE'], contact['QSO_DATE'], contact['TIME_ON'], qso_confirmed))

    def __str__(self):
        log_str = ""
        for qso in self.log:
            log_str += str(qso)
        return log_str

    def write_qso(self, contact: QSO):
        self.log.add(contact)

    def discard_qso(self, contact: QSO):
        self.log.discard(contact)
        # to-do: discrad from adi?