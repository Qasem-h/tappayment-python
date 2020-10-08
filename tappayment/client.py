import json
import requests

from .constants import HTTP_STATUS_CODE, ERROR_CODE, URL

from .errors import (BadRequestError,
                     GatewayError,
                     ServerError)

from . import resources
from types import ModuleType


def capitalize_camel_case(string):
    return "".join(map(str.capitalize, string.split('_')))


# Create a dict of resource classes
RESOURCE_CLASSES = {}
for name, module in resources.__dict__.items():
    if isinstance(module, ModuleType) and \
            capitalize_camel_case(name) in module.__dict__:
        RESOURCE_CLASSES[name] = module.__dict__[capitalize_camel_case(name)]



class Client:
    """TapPayment client class"""
    DEFAULTS = {
        'base_url': URL.BASE_URL,
    }

    def __init__(self, session=None, api_token=None, **options):
        """
        Initialize a Client object with session,
        optional auth handler, and options
        """
        self.session = session or requests.Session()
        self.api_token = api_token
        self.auth = None
        self.base_url = self.DEFAULTS['base_url']
        # intializes each resource
        # injecting this client object into the constructor
        for name, Klass in RESOURCE_CLASSES.items():
            setattr(self, name, Klass(self))

    def _update_header(self, options):
        token_header = {'Authorization': 'Bearer ' + self.api_token }
        if 'headers' not in options:
            options['headers'] = {}

        options['headers'].update({'Content-type': 'application/json'})
        options['headers'].update(token_header)
        return options

    def request(self, method, path, **options):
        """
        Dispatches a request to the TapPayment HTTP API
        """
        options = self._update_header(options)

        url = "{}{}".format(self.base_url, path)
        print(url)
        response = getattr(self.session, method)(url, auth=self.auth,
                                                 **options)
        print(response.json())
        if ((response.status_code >= HTTP_STATUS_CODE.OK) and
                (response.status_code < HTTP_STATUS_CODE.REDIRECT)):
            return response.json()
        else:
            msg = ""
            code = ""
            json_response = response.json()
            if 'error' in json_response:
                if 'description' in json_response['error']:
                    msg = json_response['error']['description']
                if 'code' in json_response['error']:
                    code = str(json_response['error']['code'])

            if str.upper(code) == ERROR_CODE.BAD_REQUEST_ERROR:
                raise BadRequestError(msg)
            elif str.upper(code) == ERROR_CODE.GATEWAY_ERROR:
                raise GatewayError(msg)
            elif str.upper(code) == ERROR_CODE.SERVER_ERROR:
                raise ServerError(msg)
            else:
                raise ServerError(msg)

    def get(self, path, params, **options):
        """
        Parses GET request options and dispatches a request
        """
        return self.request('get', path, params=params, **options)

    def post(self, path, data, **options):
        """
        Parses POST request options and dispatches a request
        """
        data, options = self._update_request(data, options)
        return self.request('post', path, data=data, **options)

    def patch(self, path, data, **options):
        """
        Parses PATCH request options and dispatches a request
        """
        data, options = self._update_request(data, options)
        return self.request('patch', path, data=data, **options)

    def delete(self, path, data, **options):
        """
        Parses DELETE request options and dispatches a request
        """
        data, options = self._update_request(data, options)
        return self.request('delete', path, data=data, **options)

    def put(self, path, data, **options):
        """
        Parses PUT request options and dispatches a request
        """
        data, options = self._update_request(data, options)
        return self.request('put', path, data=data, **options)

    def _update_request(self, data, options):
        """
        Updates The resource data and header options
        """
        data = json.dumps(data)
        token_header = {'Authorization': 'Bearer ' + self.api_token }
        if 'headers' not in options:
            options['headers'] = {}

        options['headers'].update({'Content-type': 'application/json'})
        options['headers'].update(token_header)
        return data, options
