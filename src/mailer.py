import sendgrid
from sendgrid.helpers.mail import *

class Mailer:
    '''Simplifies the process of sending emails with sendgrid.'''

    def __init__(self, apikey):
        '''
        `apikey` - sendgrid api key
        '''
        self.sg = sendgrid.SendGridAPIClient(apikey=apikey)

    def send(self, to_email, subject, body):
        '''
        `to_email` - email address to send the email to (string)
        `subject` - subject of the email (string)
        `body` - body of the email (string)
        '''
        from_email = Email("evg-notify@mongodb.com")
        to_email = Email(to_email)
        content = Content("text/plain", body)
        mail = Mail(from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        response.status_code
        response.body
        response.headers
