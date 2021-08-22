import logging
import sentry_sdk

from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from flask import Flask, request, redirect

from utils.SpreadSheet import DoctorSheet
from utils.credentials import SENTRY_URL


app = Flask(__name__)

# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn=SENTRY_URL,
    integrations=[FlaskIntegration(), sentry_logging],
    traces_sample_rate=1.0
)

@app.route('/close_ticket')
def hello_world():
    dSheet = DoctorSheet()
    user_id = dSheet.close_ticket(request.args.get('ticket_uuid'))
    return redirect(f'https://twitter.com/messages/compose?recipient_id={user_id}')

@app.route('/fuck-afk')
def hello():
    dSheet = DoctorSheet()
    dSheet.afk()
    return "OK"

if __name__ == '__main__':
    app.run()
