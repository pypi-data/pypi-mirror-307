import sys
import traceback
from abc import abstractmethod
from typing import Any

from flask import request
from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.WebhookService import AbstractWebhookHandler
from sapiopylib.rest.pojo.webhook.WebhookResult import SapioWebhookResult


class AbstractWebserviceHandler(AbstractWebhookHandler):
    """
    A base class for constructing "webservice" endpoints on your webhook server. These are endpoints that can be
    communicated with by external sources without needing to format the payload JSON in the webhook context format that
    webhook handlers expect.

    The entire payload JSON is sent to the run method of this class. It is up to the run method to determine how
    this JSON should be parsed. In order to communicate with a Sapio system, a SapioUser object must be able to be
    defined using the payload. Functions have been provided for constructing users with various authentication methods.

    Since this extends AbstractWebhookHandler, you can still register endpoints from this class in the same way you
    would normal webhook endpoints.
    """
    def post(self) -> dict[str, Any]:
        """
        Internal method to be executed to translate incoming requests.
        """
        # noinspection PyBroadException
        try:
            return self.run(request.json).to_json()
        except Exception:
            print('Error occurred while running webservice custom logic. See traceback.', file=sys.stderr)
            traceback.print_exc()
            return SapioWebhookResult(False, display_text="Error occurred during webservice execution.").to_json()

    @abstractmethod
    def run(self, payload: dict[str, Any]) -> SapioWebhookResult:
        pass

    def basic_auth(self, url: str, username: str, password: str) -> SapioUser:
        """
        :param url: The URL of the Sapio system that requests from this user will be sent to.
            Must end in /webservice/api
        :param username: The username to authenticate requests with.
        :param password: The password to authenticate requests with.
        :return: A SapioUser that will authenticate requests using basic auth.
        """
        return SapioUser(url, self.verify_sapio_cert, self.client_timeout_seconds, username=username, password=password)

    def api_token_auth(self, url: str, api_token: str) -> SapioUser:
        """
        :param url: The URL of the Sapio system that requests from this user will be sent to.
            Must end in /webservice/api
        :param api_token: The API token to authenticate requests with.
        :return: A SapioUser that will authenticate requests using an API token.
        """
        return SapioUser(url, self.verify_sapio_cert, self.client_timeout_seconds, api_token=api_token)

    def bearer_token_auth(self, url: str, bearer_token: str) -> SapioUser:
        """
        :param url: The URL of the Sapio system that requests from this user will be sent to.
            Must end in /webservice/api
        :param bearer_token: The bearer token to authenticate requests with.
        :return: A SapioUser that will authenticate requests using a bearer token.
        """
        return SapioUser(url, self.verify_sapio_cert, self.client_timeout_seconds, bearer_token=bearer_token)
