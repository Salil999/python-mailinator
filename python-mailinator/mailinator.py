import requests
import time
from email_message import EmailMessage


class MailinatorInbox:

    INBOX_URL = 'https://api.mailinator.com/api/inbox'
    EMAIL_URL = 'http://api.mailinator.com/api/email'
    DELETE_URL = 'http://api.mailinator.com/api/delete'

    def __init__(self, token=None, default_mailbox=None, is_private_domain=False):
        if(not token):
            raise Exception('Token must be provided!')
        elif(not isinstance(token, str)):
            raise Exception('Token must be a string!')
        self._token = token
        self.default_mailbox = default_mailbox
        self.is_private_domain = is_private_domain

    def set_default_mailbox(self, mb=None):
        if(not isinstance(mb, str)):
            raise Exception('Mailbox must be a string!')
        self.default_mailbox = mb

    def get_default_mailbox(self):
        return self.default_mailbox

    def set_private_domain(self, private=None):
        if(not isinstance(private, bool)):
            raise('Privacy must be a boolean!')
        self.is_private_domain = private

    def get_private_domain(self):
        return self.is_private_domain

    def get_messages(self, default_mailbox=None, private_domain=None):
        if(default_mailbox is None):
            default_mailbox = self.default_mailbox
        if(private_domain is None):
            private_domain = self.is_private_domain
        params = self._construct_params('inbox', mailbox=default_mailbox, private_domain=private_domain)
        response = requests.get(MailinatorInbox.INBOX_URL, params)
        if(response.status_code == 429):
            raise Exception('Too many requests!')
        json_resp = response.json()
        if(not response or not json_resp):
            return dict()
        messages = json_resp.get('messages', [])
        return sorted(messages, key=lambda x: x['seconds_ago'])

    def read_email(self, email_id=None, private_domain=None):
        if(not email_id):
            raise Exception('Must provide an id to delete!')
        elif(not isinstance(email_id, str)):
            raise Exception('id must be a string!')
        if(private_domain is None):
            private_domain = self.is_private_domain
        params = self._construct_params('read', email_id=email_id, private_domain=private_domain)
        response = requests.get(MailinatorInbox.EMAIL_URL, params)
        if(response.status_code == 429):
            raise Exception('Too many requests!')
        return self._parse_email_message(response.json())

    def delete_email(self, email_id=None, private_domain=None):
        if(not email_id):
            raise Exception('Must provide an id to delete!')
        elif(not isinstance(email_id, str)):
            raise Exception('id must be a string!')
        if(private_domain is None):
            private_domain = self.is_private_domain
        params = self._construct_params('delete', email_id=email_id, private_domain=private_domain)
        response = requests.get(MailinatorInbox.DELETE_URL, params)
        if(response.status_code == 429):
            raise Exception('Too many requests!')
        return response.json()

    def _parse_email_message(self, obj):
        obj = obj.get('data', None)
        if(obj is None):
            return EmailMessage()
        sender = obj.get('origfrom', None)
        headers = obj.get('headers', None)
        subject = obj.get('subject', None)
        to = obj.get('to', None)
        msg_id = obj.get('id', None)
        received_time = obj.get('time', None)
        if(received_time is not None):
            date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(received_time / 1000))
        parts = obj.get('parts', None)
        if(parts is not None):
            email_headers = parts[0].get('headers', None)
            body = parts[0].get('body', None)
        return EmailMessage(sender=sender, headers=headers, subject=subject, to=to, message_id=msg_id,
                            received_time=date_time, email_headers=email_headers, message=body)

    def _construct_params(self, api_type, mailbox=None, email_id=None, private_domain=None):
        types = {
            'inbox': {
                'token': self._token,
                'to': mailbox,
                'private_domain': private_domain,
            },
            'delete': {
                'token': self._token,
                'id': email_id,
                'private_domain': private_domain,
            },
            'read': {
                'token': self._token,
                'id': email_id,
                'private_domain': private_domain,
            }
        }
        return types[api_type]
