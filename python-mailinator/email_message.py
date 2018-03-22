class EmailMessage:
    def __init__(self, sender=None, headers=None, subject=None, to=None, message_id=None, received_time=None, email_headers=None, message=None):
        self._sender = sender
        self._headers = headers
        self._subject = subject
        self._to = to
        self._message_id = message_id
        self._received = received_time
        self._email_headers = email_headers
        self._message = message

    def get_sender(self):
        return self._sender

    def get_headers(self):
        return self._headers

    def get_subject(self):
        return self._subject

    def get_receiver(self):
        return self._to

    def get_message_id(self):
        return self._message_id

    def get_received_time(self):
        return self._received

    def get_email_headers(self):
        return self._email_headers

    def get_body(self):
        return self._message

    def __str__(self):
        return 'EmailMessage(sender={}, headers={}, subject={}, receiver={}, message_id={}, received_time={}, email_headers={}, message={})'.format(
            self._sender, self._headers, self._subject, self._to, self._message_id, self._received, self._email_headers, self._message
        )
