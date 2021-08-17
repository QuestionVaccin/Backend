import logging

import gspread
import tweepy
from .credentials import CREDS
from .credentials import VACCIN_CONSUMER_API_KEY, VACCIN_CONSUMER_API_SECRET, VACCIN_ACCESS_API_SECRET, VACCIN_ACCESS_API_KEY


class DoctorSheet(object):
    def __init__(self):
        gc = gspread.service_account_from_dict(CREDS)
        auth = tweepy.OAuthHandler(VACCIN_CONSUMER_API_KEY, VACCIN_CONSUMER_API_SECRET)
        auth.set_access_token(VACCIN_ACCESS_API_KEY, VACCIN_ACCESS_API_SECRET)
        self.api = tweepy.API(auth)
        self.tickets = gc.open(u'Liste specialistes Bot').get_worksheet(2)

    def close_ticket(self, ticket_id):
        cell = self.tickets.find(ticket_id)
        row = self.tickets.row_values(cell.row)
        user_id = row[1]
        closed = row[6]
        if closed == "FALSE":
            self.api.send_direct_message(recipient_id=user_id, text="""
            Nous espérons avoir répondu à toutes vos questions. N'hésitez pas à partager votre expérience en mentionnant @QuestionVaccin !
            """)

        try:
            self.tickets.update_cell(cell.row, 7, "TRUE")
        except Exception as e:
            logging.exception("An exception has been raised for ticket " + ticket_id + ", exception: " + str(e))
