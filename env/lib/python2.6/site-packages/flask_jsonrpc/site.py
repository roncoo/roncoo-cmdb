# -*- coding: utf-8 -*-
# Copyright (c) 2009 Samuel Sutch, <sam@sutch.net>
# Copyright (c) 2012-2015, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# * Neither the name of the Cenobit Technologies nor the names of
#    its contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import re
import decimal
import datetime
from uuid import uuid4
from functools import wraps

from werkzeug.exceptions import HTTPException

from flask.wrappers import Response
from flask import json, jsonify, request, make_response, current_app

from flask_jsonrpc.types import Object, Array, Any
from flask_jsonrpc.helpers import extract_raw_data_request
from flask_jsonrpc._compat import (text_type, string_types, integer_types,
                                   iteritems, iterkeys)
from flask_jsonrpc.exceptions import (Error, ParseError, InvalidRequestError,
                                      MethodNotFoundError, InvalidParamsError,
                                      ServerError, RequestPostError,
                                      InvalidCredentialsError, OtherError)

JSONRPC_VERSION_DEFAULT = '2.0'

empty_dec = lambda f: f
try:
    # TODO: Add CSRF check
    csrf_exempt = empty_dec
except (NameError, ImportError):
    csrf_exempt = empty_dec

NoneType = type(None)
encode_kw = lambda p: dict([(text_type(k), v) for k, v in iteritems(p)])

def encode_kw11(p):
    if not type(p) is dict:
        return {}
    ret = p.copy()
    removes = []
    for k, v in iteritems(ret):
        try:
            int(k)
        except ValueError:
            pass
        else:
            removes.append(k)
    for k in removes:
        ret.pop(k)
    return ret

def encode_arg11(p):
    if type(p) is list:
        return p
    elif not type(p) is dict:
        return []
    else:
        pos = []
        d = encode_kw(p)
        for k, v in iteritems(d):
            try:
                pos.append(int(k))
            except ValueError:
                pass
        pos = list(set(pos))
        pos.sort()
        return [d[text_type(i)] for i in pos]

def validate_params(method, D):
    if type(D['params']) == Object:
        keys = method.json_arg_types.keys()
        if len(keys) != len(D['params']):
            raise InvalidParamsError('Not enough params provided for {0}' \
                .format(method.json_sig))
        for k in keys:
            if not k in D['params']:
                raise InvalidParamsError('{0} is not a valid parameter for {1}' \
                    .format(k, method.json_sig))
            if not Any.kind(D['params'][k]) == method.json_arg_types[k]:
                raise InvalidParamsError('{0} is not the correct type {1} for {2}' \
                    .format(type(D['params'][k]), method.json_arg_types[k], method.json_sig))
    elif type(D['params']) == Array:
        arg_types = list(method.json_arg_types.values())
        try:
            for i, arg in enumerate(D['params']):
                if not Any.kind(arg) == arg_types[i]:
                    raise InvalidParamsError('{0} is not the correct type {1} for {2}' \
                        .format(type(arg), arg_types[i], method.json_sig))
        except IndexError:
            raise InvalidParamsError('Too many params provided for {0}'.format(method.json_sig))
        else:
            if len(D['params']) != len(arg_types):
                raise InvalidParamsError('Not enough params provided for {0}'.format(method.json_sig))


class JSONRPCSite(object):
    """A JSON-RPC Site
    """

    def __init__(self):
        self.urls = {}
        self.uuid = text_type(uuid4())
        self.version = JSONRPC_VERSION_DEFAULT
        self.name = 'Flask-JSONRPC'
        self.register('system.describe', self.describe)

    def register(self, name, method):
        self.urls[text_type(name)] = method

    def extract_id_request(self, raw_data):
        try:
            D = json.loads(raw_data)
            return D.get('id')
        except Exception as e:
            if not raw_data is None and raw_data.find('id') != -1:
                find_id = re.findall(r'["|\']id["|\']:([0-9]+)|["|\']id["|\']:["|\'](.+?)["|\']',
                                     raw_data.replace(' ', ''), re.U)
                if find_id:
                    g1, g2 = find_id[0]
                    raw_id = g1 if g1 else g2
                    if text_type(raw_id).isnumeric():
                        return int(raw_id)
                    return raw_id
            return None

    def empty_response(self, version=JSONRPC_VERSION_DEFAULT):
        resp = {'id': None}
        if version == '1.1':
            resp['version'] = version
            return resp
        if version == '2.0':
            resp['jsonrpc'] = version
        resp.update({'error': None, 'result': None})
        return resp

    def validate_get(self, request, method):
        encode_get_params = lambda r: dict([(k, v[0] if len(v) == 1 else v) for k, v in r])
        if request.method == 'GET':
            method = text_type(method)
            if method in self.urls and getattr(self.urls[method], 'json_safe', False):
                D = {
                    'params': request.args.to_dict(),
                    'method': method,
                    'id': 'jsonrpc',
                    'version': '1.1'
                }
                return True, D
        return False, {}

    def apply_version_2_0(self, f, p):
        return f(**encode_kw(p)) if type(p) is dict else f(*p)

    def apply_version_1_1(self, f, p):
        return f(*encode_arg11(p), **encode_kw(encode_kw11(p)))

    def apply_version_1_0(self, f, p):
        return f(*p)

    def response_obj(self, request, D, version_hint=JSONRPC_VERSION_DEFAULT):
        version = version_hint
        response = self.empty_response(version=version)
        apply_version = {
            '2.0': self.apply_version_2_0,
            '1.1': self.apply_version_1_1,
            '1.0': self.apply_version_1_0
        }

        try:
            try:
                # determine if an object is iterable?
                iter(D)
            except TypeError as e:
                raise InvalidRequestError(getattr(e, 'message', e.args[0] if len(e.args) > 0 else None))

            # version: validate
            if 'jsonrpc' in D:
                if text_type(D['jsonrpc']) not in apply_version:
                    raise InvalidRequestError('JSON-RPC version {0} not supported.'.format(D['jsonrpc']))
                version = request.jsonrpc_version = response['jsonrpc'] = text_type(D['jsonrpc'])
            elif 'version' in D:
                if text_type(D['version']) not in apply_version:
                    raise InvalidRequestError('JSON-RPC version {0} not supported.'.format(D['version']))
                version = request.jsonrpc_version = response['version'] = text_type(D['version'])
            else:
                version = request.jsonrpc_version = JSONRPC_VERSION_DEFAULT

            # params: An Array or Object, that holds the actual parameter values
            # for the invocation of the procedure. Can be omitted if empty.
            if 'params' not in D or not D['params']:
                 D['params'] = []
            if 'method' not in D or 'params' not in D:
                raise InvalidParamsError('Request requires str:"method" and list:"params"')
            if D['method'] not in self.urls:
                raise MethodNotFoundError('Method not found. Available methods: {0}' \
                    .format('\n'.join(list(self.urls.keys()))))

            method = self.urls[text_type(D['method'])]
            if getattr(method, 'json_validate', False):
                validate_params(method, D)

            if 'id' in D and D['id'] is not None: # regular request
                response['id'] = D['id']
                if version in ('1.1', '2.0'):
                    response.pop('error', None)
            else: # notification
                return None, 204

            R = apply_version[version](method, D['params'])

            if 'id' not in D or ('id' in D and D['id'] is None): # notification
                return None, 204

            if isinstance(R, Response):
                if R.status_code == 200:
                    return R, R.status_code
                if R.status_code == 401:
                    raise InvalidCredentialsError(R.status)
                raise OtherError(R.status, R.status_code)

            try:
                # New in Flask version 0.10.
                encoder = current_app.json_encoder()
            except AttributeError:
                encoder = json.JSONEncoder()

            # type of `R` should be one of these or...
            if not sum([isinstance(R, e) for e in \
                    string_types + integer_types + \
                    (float, complex, dict, list, tuple, set, frozenset, NoneType, bool)]):
                try:
                    rs = encoder.default(R) # ...or something this thing supports
                except TypeError as exc:
                    raise TypeError('Return type not supported, for {0!r}'.format(R))

            response['result'] = R
            status = 200
        except Error as e:
            response['error'] = e.json_rpc_format
            if version in ('1.1', '2.0'):
                response.pop('result', None)
            status = e.status
        except HTTPException as e:
            other_error = OtherError(e)
            response['error'] = other_error.json_rpc_format
            response['error']['code'] = e.code
            if version in ('1.1', '2.0'):
                response.pop('result', None)
            status = e.code
        except Exception as e:
            other_error = OtherError(e)
            response['error'] = other_error.json_rpc_format
            status = other_error.status
            if version in ('1.1', '2.0'):
                response.pop('result', None)

        # Exactly one of result or error MUST be specified. It's not
        # allowed to specify both or none.
        if version in ('1.1', '2.0') and 'result' in response:
            response.pop('error', None)

        return response, status

    def batch_response_obj(self, request, D):
        status = 200
        try:
            responses = [self.response_obj(request, d)[0] for d in D]
            if not responses:
                raise InvalidRequestError('Empty array')
        except Error as e:
            for response in responses:
                response.pop('result', None)
                response['error'] = e.json_rpc_format
        except Exception as e:
            other_error = OtherError(e)
            for response in responses:
                response.pop('result', None)
                response['error'] = other_error.json_rpc_format

        for response in responses:
            if response is None:
                continue # notification
            # Exactly one of result or error MUST be specified. It's not
            # allowed to specify both or none.
            if 'result' in response:
                response.pop('error', None)

        if not responses:
            response = self.empty_response(version='2.0')
            response['error'] = InvalidRequestError().json_rpc_format
            response.pop('result', None)
            responses = response

        if not all(responses):
            return '', 204 # notification

        return responses, status

    def make_response(self, rv):
        """Converts the return value from a view function to a real
        response object that is an instance of :attr:`response_class`.
        """
        status_or_headers = headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))

        if rv is None:
            raise ValueError('View function did not return a response')

        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None

        D = json.loads(extract_raw_data_request(request))
        if type(D) is list:
            raise InvalidRequestError('JSON-RPC batch with decorator (make_response) not is supported')
        else:
            response_obj = self.empty_response(version=D['jsonrpc'])
            response_obj['id'] = D['id']
            response_obj['result'] = rv
            response_obj.pop('error', None)
            rv = jsonify(response_obj)

        if status_or_headers is not None:
            if isinstance(status_or_headers, string_types):
                rv.status = status_or_headers
            else:
                rv.status_code = status_or_headers
        if headers:
            rv.headers.extend(headers)

        return rv

    @csrf_exempt
    def dispatch(self, request, method=''):
        # in case we do something json doesn't like, we always get back valid
        # json-rpc response
        response = self.empty_response()
        raw_data = extract_raw_data_request(request)

        try:
            if request.method == 'GET':
                valid, D = self.validate_get(request, method)
                if not valid:
                    raise InvalidRequestError('The method you are trying to access is '
                                              'not availble by GET requests')
            elif not request.method == 'POST':
                raise RequestPostError()
            else:
                try:
                    D = json.loads(raw_data)
                except Exception as e:
                    raise ParseError(getattr(e, 'message', e.args[0] if len(e.args) > 0 else None))

            if type(D) is list:
                return self.batch_response_obj(request, D)

            response, status = self.response_obj(request, D)

            if isinstance(response, Response):
               return response, status

            if response is None and (not 'id' in D or D['id'] is None): # a notification
                response = ''
                return response, status
        except Error as e:
            response.pop('result', None)
            response['error'] = e.json_rpc_format
            status = e.status
        except Exception as e:
            other_error = OtherError(e)
            response.pop('result', None)
            response['error'] = other_error.json_rpc_format
            status = other_error.status

        # extract id the request
        if not response.get('id', False):
            json_request_id = self.extract_id_request(raw_data)
            response['id'] = json_request_id

        # If there was an error in detecting the id in the Request object
        # (e.g. Parse error/Invalid Request), it MUST be Null.
        if not response and 'error' in response:
            if response['error']['name'] in ('ParseError', 'InvalidRequestError', 'RequestPostError'):
                response['id'] = None

        return response, status

    def procedure_desc(self, key):
        M = self.urls[key]
        return {
            'name': M.json_method,
            'summary': M.__doc__,
            'idempotent': M.json_safe,
            'params': [{'type': text_type(Any.kind(t)), 'name': k}
                for k, t in iteritems(M.json_arg_types)],
            'return': {'type': text_type(Any.kind(M.json_return_type))}}

    def service_desc(self):
        return {
            'sdversion': '1.0',
            'name': self.name,
            'id': 'urn:uuid:{0}'.format(text_type(self.uuid)),
            'summary': self.__doc__,
            'version': self.version,
            'procs': [self.procedure_desc(k)
                for k in iterkeys(self.urls)
                    if self.urls[k] != self.describe]}

    def describe(self):
        return self.service_desc()


jsonrpc_site = JSONRPCSite()

