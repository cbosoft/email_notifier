import os.path
from typing import List, Union
import json
from datetime import datetime
import traceback
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailNotifier:

    def __init__(self,
                 message, *,
                 error_message='Something went wrong!',
                 subject=None,
                 config_path=None,
                 is_html=None,
                 smtp_server=None, sender_email=None, password=None, recipient_email=None, port=None):
        config = self.get_config(config_path)
        specified_config = dict(
            smtp_server=smtp_server, sender_email=sender_email,
            recipient_email=recipient_email, port=port, password=password)
        for k, v in specified_config.items():
            if v is not None:
                config[k] = v
        self.config = config
        self.message = message
        self.error_message = error_message

        if subject is None:
            subject = '{kind} alert ' + datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        self.subject = subject
        self.is_html = '<' in message if is_html is None else is_html

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if any([exc_type, exc_val, exc_tb]):
            error_message = self.error_message + '<br><p>{}</p>'.format(
                ''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
            self.send_message(error_message, self.subject.format(kind='Error'), self.is_html, **self.config)
        else:
            self.send_message(self.message, self.subject.format(kind='Notification'), True, **self.config)

    @staticmethod
    def get_config(config_path: str = None) -> dict:
        if config_path is None:
            config_path = os.path.join(os.getenv('HOME'), '.email_notifier.json')
        if os.path.isfile(config_path):
            with open(config_path) as f:
                return json.load(f)
        print(f'Warning: config_path ("{config_path}") does not exist or is not a valid file.')
        return {}

    @staticmethod
    def send_message(message_text, subject: str, is_html: bool, *,
                     smtp_server: str, port: int, sender_email: str, password: str,
                     recipient_email: Union[str, List[str]]):

        email_message = MIMEMultipart()
        email_message['To'] = recipient_email
        email_message['From'] = sender_email
        email_message['Subject'] = subject
        email_message.attach(MIMEText(message_text, 'html' if is_html else 'plain'))

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        server = smtplib.SMTP(smtp_server, port)

        try:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, email_message.as_string())
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()
