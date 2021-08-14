import logging

import gspread
from .credentials import CREDS


class DoctorSheet(object):
    def __init__(self):
        gc = gspread.service_account_from_dict(CREDS)
        self.tickets = gc.open(u'Liste specialistes Bot').get_worksheet(2)

    def close_ticket(self, ticket_id):
        cell = self.tickets.find(ticket_id)
        try:
            self.tickets.update_cell(cell.row, 6, "TRUE")
        except Exception as e:
            logging.exception("An exception has been raised for ticket " + ticket_id + ", exception: " + str(e))
