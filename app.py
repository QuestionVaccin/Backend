from flask import Flask, request
from utils.SpreadSheet import DoctorSheet
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import logging
from sentry_sdk.integrations.logging import LoggingIntegration
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

app = Flask(__name__)

@app.route('/close_ticket')
def hello_world():
    dSheet = DoctorSheet()
    dSheet.close_ticket(request.args.get('ticket_uuid'))
    return """"<script>
    window.open(document.URL,'_self','resizable=no,top=-245,width=250,height=250,scrollbars=no');
    window.close();
    </script>"""


if __name__ == '__main__':
    app.run()
