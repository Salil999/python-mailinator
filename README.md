# python-mailinator
A simple Python3 wrapper to the amazing [Mailinator](https://www.mailinator.com) service!

## Installation
Install using pip3
```
pip3 install python-mailinator
```

## Instructions
Make sure you have an API key! You may request one at the Mailinator [website](https://www.mailinator.com/manyauth/teamsettings.jsp).
```
from python-mailinator.mailinator import MailinatorInbox
API_KEY = <your_api_key>
inbox = MailinatorInbox(token=API_KEY, default_mailbox='test', is_private_domain=False) # 2nd and 3rd params optional
messages = inbox.get_messages() # consumes an API call
for message in messages:
    email = inbox.read_email(message['id']) # consumes an API call
    print(email.get_sender())
    print(email.get_receiver())
    print(email.get_received_time())
inbox.delete_email(messages[0]['id']) # consumes an API call
```

## Contributing
Throw in a PR and I'll get to it ASAP!

## Author
Shashank Saxena
