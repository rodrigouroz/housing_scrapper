from requests import Session
from lib.hostname_ignoring_adapter import HostNameIgnoringAdapter

class SSLlessSession(Session):
    def post(self, url, data, **kwargs):
        kwargs.setdefault('verify', False)
        # this will fail is there is no response, so this is assuming the happy path
        r = super().post(url, data, **kwargs).json()
        return r['result']