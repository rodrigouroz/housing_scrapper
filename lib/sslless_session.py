from requests import Session
from lib.hostname_ignoring_adapter import HostNameIgnoringAdapter

class SSLlessSession(Session):
    def __init__(self) -> None:
        super().__init__()
        self.mount('https://', HostNameIgnoringAdapter())
    def get(self, url, **kwargs):
        kwargs.setdefault('verify', False)
        return super().get(url, **kwargs)
    def post(self, url, data, **kwargs):
        kwargs.setdefault('verify', False)
        # this will fail is there is no response, so this is assuming the happy path
        r = super().post(url, data, **kwargs).json()
        return r['result']