# `email_notifier`

Get email notification when a long-running function ends.

# Installation

```bash
git clone https://github.com/cbosoft/email_notifier
cd email_notifier
pip install .
```

# Usage

To send email, you need to configure email server settings. This is, by default, in a json file in your home dir: `$HOME/.email_notifier.json`

```json
{
  "smtp_server": "smtp.example.com",
  "sender_email": "notifications@bar.com",
  "password": "notVerySecureAtAll",
  "recipient_email": "foo@bar.com",
  "port": 587
}
```

It is recommended to use a single-purpose address for this: one set up to only send notifications. There is little security here and the password is stored plaintext. With email configured, we can get notifications in only a few lines:

```python
from email_notifier import EmailNotifier

with EmailNotifier(message='Task complete.'):
    do_something()
```

All going well, you will recieve an email the message "Task complete.". If an error were to arise, you would recieve the formatted exception and traceback via email.

Email configuration settings can be overriden case-by-case when constructing the notifier:
```python
from email_notifier import EmailNotifier

with EmailNotifier(
        message='Task complete.',
        smtp_server='smtp.another.server.com',
        sender_email='notifications@another.server.com',
        password='guest1234',
        recipient_email='person@another.server.com',
        port=587):
    do_something()
```