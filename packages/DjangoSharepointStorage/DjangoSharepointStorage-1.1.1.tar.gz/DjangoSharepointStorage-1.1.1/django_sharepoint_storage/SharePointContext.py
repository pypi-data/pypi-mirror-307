from datetime import datetime, timedelta
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from django.conf import settings


class SharePointContext:
    _instance = None
    _client_credentials = None
    _ctx = None
    _last_created = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharePointContext, cls).__new__(cls)
            cls._initialize(cls._instance)
        elif datetime.now() - cls._last_created > timedelta(hours=23):
            cls._initialize(cls._instance)
        return cls._instance

    @classmethod
    def _initialize(cls, instance):
        client_id = getattr(settings, 'SHAREPOINT_APP_CLIENT_ID', 'client_id')
        client_secret = getattr(settings, 'SHAREPOINT_APP_CLIENT_SECRET', 'client_secret')
        sharepoint_url = getattr(settings, 'SHAREPOINT_URL', 'sharepoint_url')

        instance._client_credentials = ClientCredential(client_id, client_secret)
        instance._ctx = ClientContext(sharepoint_url).with_credentials(instance._client_credentials)
        cls._last_created = datetime.now()

    @property
    def client_credentials(self):
        return self._client_credentials

    @property
    def ctx(self):
        return self._ctx