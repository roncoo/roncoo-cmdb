# -*- coding: utf-8 -*-

import logging
import json
import string
import socket

try:
    from urllib.request import Request, build_opener
except ImportError:
    # Python 2
    from urllib2 import Request, build_opener

try:
    from urllib.error import URLError, HTTPError as _HTTPError
except ImportError:
    # Python 2
    from urllib2 import URLError, HTTPError as _HTTPError

try:
    from io import BytesIO
except ImportError:
    # Python 2
    try:
        # C implementation
        from cStringIO import StringIO as BytesIO
    except ImportError:
        # Python implementation
        from StringIO import StringIO as BytesIO

try:
    import gzip
except ImportError:
    # Python can be built without zlib/gzip support
    gzip = None

try:
    import requests
except ImportError:
    requests = None

from . import __version__
from .exceptions import (
    ZabbixClientError, TransportError, TimeoutError, HTTPError, ResponseError,
    ContentDecodingError, InvalidJSONError, JSONRPCError
)


# Default network timeout (in seconds)
DEFAULT_TIMEOUT = 30

logger = logging.getLogger(__name__)


def dumps(id_, method, params=None, auth=None):
    rpc_request = {
        'jsonrpc': '2.0',
        'id': id_,
        'method': method
    }

    if params is not None:
        rpc_request['params'] = params
    if auth is not None:
        rpc_request['auth'] = auth

    dump = json.dumps(rpc_request, separators=(',', ':')).encode('utf-8')

    if logger.isEnabledFor(logging.INFO):
        json_str = json.dumps(rpc_request, sort_keys=True)
        logger.info("JSON-RPC request: {0}".format(json_str))

    return dump


def loads(response):
    try:
        rpc_response = json.loads(response.decode('utf-8'))
    except ValueError as e:
        raise InvalidJSONError(e)

    if not isinstance(rpc_response, dict):
        raise ResponseError('Response is not a dict')

    if 'jsonrpc' not in rpc_response or rpc_response['jsonrpc'] != '2.0':
        raise ResponseError('JSON-RPC version not supported')

    if 'error' in rpc_response:
        error = rpc_response['error']
        if 'code' not in error or 'message' not in error:
            raise ResponseError('Invalid JSON-RPC error object')

        code = error['code']
        message = error['message']
        # 'data' may be omitted
        data = error.get('data', None)

        if data is None:
            exception_message = 'Code: {0}, Message: {1}'.format(code, message)
        else:
            exception_message = ('Code: {0}, Message: {1}, ' +
                                 'Data: {2}').format(code, message, data)
        raise JSONRPCError(exception_message, code=code, message=message,
                           data=data)

    if 'result' not in rpc_response:
        raise ResponseError('Response does not contain a result object')

    if logger.isEnabledFor(logging.INFO):
        json_str = json.dumps(rpc_response, sort_keys=True)
        logger.info("JSON-RPC response: {0}".format(json_str))

    return rpc_response


class ZabbixServerProxy(object):

    def __init__(self, url, transport=None):
        self.url = url if not url.endswith('/') else url[:-1]
        self.url += '/api_jsonrpc.php'

        logger.debug("Zabbix server URL: {0}".format(self.url))

        if transport is not None:
            self.transport = transport
        else:
            if requests:
                logger.debug("Using requests as transport layer")
                self.transport = RequestsTransport()
            else:
                logger.debug("Using urllib libraries as transport layer")
                self.transport = UrllibTransport()

        self._request_id = 0
        self._auth_token = None

        self._method_hooks = {
            'apiinfo.version': self._no_auth_method,
            'user.login': self._login,
            'user.authenticate': self._login, # deprecated alias of user.login
            'user.logout': self._logout
        }

    def __getattr__(self, name):
        return ZabbixObject(name, self)

    def call(self, method, params=None):
        method_lower = method.lower()

        if method_lower in self._method_hooks:
            return self._method_hooks[method_lower](method, params=params)

        return self._call(method, params=params, auth=self._auth_token)

    def _call(self, method, params=None, auth=None):
        self._request_id += 1
        rpc_request = dumps(self._request_id, method, params=params, auth=auth)

        content = self.transport.request(self.url, rpc_request)

        rpc_response = loads(content)

        return rpc_response['result']

    def _no_auth_method(self, method, params=None):
        return self._call(method, params=params)

    def _login(self, method, params=None):
        self._auth_token = None

        # Save the new token if the request is successful
        self._auth_token = self._call(method, params=params)

        return self._auth_token

    def _logout(self, method, params=None):
        try:
            result = self._call(method, params=params, auth=self._auth_token)
        except ZabbixClientError:
            raise
        finally:
            self._auth_token = None

        return result


class ZabbixObject(object):

    def __init__(self, name, server_proxy):
        self.name = name
        self.server_proxy = server_proxy

    def __getattr__(self, name):
        def call_wrapper(*args, **kwargs):
            if args and kwargs:
                raise ValueError('JSON-RPC 2.0 does not allow both ' +
                                 'positional and keyword arguments')

            method = '{0}.{1}'.format(self.name, name)
            params = args or kwargs or None
            return self.server_proxy.call(method, params=params)

        # Little hack to avoid clashes with reserved keywords.
        # Example: use configuration.import_() to call configuration.import()
        if name.endswith('_'):
            name = name[:-1]

        return call_wrapper


class Transport(object):

    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self.timeout = timeout

    def request(self, url, rpc_request):
        raise NotImplementedError

    @staticmethod
    def _add_headers(headers):
        # Set the JSON-RPC headers
        json_rpc_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        headers.update(json_rpc_headers)

        # If no custom header exists, set the default user-agent
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'zabbix-client/{0}'.format(__version__)


class RequestsTransport(Transport):

    def __init__(self, *args, **kwargs):
        if not requests:
            raise ValueError('requests is not available')

        self.session = kwargs.pop('session', None)

        super(RequestsTransport, self).__init__(*args, **kwargs)

        if self.session is None:
            self.session = requests.Session()

            # Delete default requests' user-agent
            self.session.headers.pop('User-Agent', None)

        self._add_headers(self.session.headers)

    def request(self, url, rpc_request):
        try:
            response = self.session.post(url, data=rpc_request,
                                         timeout=self.timeout)

            response.raise_for_status()

            content = response.content
        except requests.Timeout as e:
            raise TimeoutError(e)
        except requests.exceptions.ContentDecodingError as e:
            raise ContentDecodingError(e)
        except requests.HTTPError as e:
            raise HTTPError(e)
        except requests.RequestException as e:
            raise TransportError(e)

        return content


class UrllibTransport(Transport):

    def __init__(self, *args, **kwargs):
        self.accept_gzip_encoding = kwargs.pop('accept_gzip_encoding', True)
        headers = kwargs.pop('headers', None)

        super(UrllibTransport, self).__init__(*args, **kwargs)

        self.headers = {}
        if headers:
            for key, value in headers.items():
                self.headers[string.capwords(key, '-')] = value

        self._add_headers(self.headers)

        if self.accept_gzip_encoding and gzip:
            self.headers['Accept-Encoding'] = 'gzip'

        self._opener = build_opener()

    def request(self, url, rpc_request):
        request = Request(url, data=rpc_request, headers=self.headers)

        try:
            response = self._opener.open(request, timeout=self.timeout)

            content = response.read()
        except _HTTPError as e:
            raise HTTPError(e)
        except URLError as e:
            if isinstance(e.reason, socket.timeout):
                raise TimeoutError(e)
            else:
                raise TransportError(e)
        except socket.timeout as e:
            raise TimeoutError(e)

        encoding = response.info().get('Content-Encoding', '').lower()
        if encoding in ('gzip', 'x-gzip'):
            if not gzip:
                raise ValueError('gzip is not available')

            b = BytesIO(content)
            try:
                content = gzip.GzipFile(mode='rb', fileobj=b).read()
            except IOError as e:
                raise ContentDecodingError(e)

        return content
