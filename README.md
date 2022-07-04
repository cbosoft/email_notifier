# `email_notifier`

Get email notification when a long-running function ends.

# Installation

```bash
git clone https://github.com/cbosoft/email_notifier
cd email_notifier
pip install .
```

# Usage

```python
from email_notifier import EmailNotifier

with EmailNotifier(message='Task complete.'):
    do_something()
```

All going well, you will recieve an email the message "Task complete.". If an error were to arise, you would recieve the formatted exception and traceback via email.