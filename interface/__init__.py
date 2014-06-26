__author__ = 'Bijan'

from flask import Flask
from flask_mail import Mail
import base64

app = Flask(__name__)
try:
    f = open('/Users/Bijan/linkspy.cnf', 'r')

    app.config.update(dict(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='bij.ranjbar@gmail.com',
        MAIL_PASSWORD=base64.b64decode(f.read()),
        DEFAULT_MAIL_SENDER='bij.ranjbar@gmail.com'
    ))

except:
    pass
mail = Mail(app)
