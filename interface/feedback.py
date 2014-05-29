__author__ = 'Bijan'

from flask import render_template
from flask_mail import Message

from interface import mail
from interface import app
from modules.basic_modules.decorators import async


@async
def send_async_email(msg):
    """
        sends the email, however beacuase of the @async function, sends it withing a separate thread.
    """
    with app.app_context():
        mail.send(msg)



def send_email(subject, sender, recipients, text_body, html_body):
    """
        sends the email to the recipient(s)
        this function uses a thread to send the email in order to return immediately to the user
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    send_async_email(msg)


def request_error_correction(document, person_list, message_type, comment, user):
    """

    """
    my_email = "bij.ranjbar@gmail.com"
    bhic_email = "bij.ranjbar@gmail.com"

    if message_type == "to_bhic":
        send_email("[MiSS] Data Correction Request, document %s!" % document['id'],
        my_email, [my_email, bhic_email],
        render_template("feedback_email.txt",
            document=document, person_list=person_list, commnet=comment, user=user),
        render_template("feedback_email.html",
            document=document, person_list=person_list, comment=comment, user=user))
    else:
        send_email("[MiSS] Website Problem!",
                   my_email, [my_email],
                   comment, "<h3> There is has been a problem with the MiSS website:</h3> <br>" + comment)

