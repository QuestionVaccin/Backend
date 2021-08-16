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
        message = self.api.get_direct_message(self.tickets.row_values(cell.row)[0])
        user_id = message.message_create['sender_id']
        self.api.send_direct_message(recipient_id=user_id, text="""Merci d'avoir posé votre question, nous esperons vous avoir aidé. N'hésitez pas à donner votre avis en mentionnant le bot @QuestionVaccin
        """)

        try:
            self.tickets.update_cell(cell.row, 6, "TRUE")
        except Exception as e:
            logging.exception("An exception has been raised for ticket " + ticket_id + ", exception: " + str(e))
