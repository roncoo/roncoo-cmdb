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
import logging
from functools import wraps
from inspect import getargspec

from flask.wrappers import Response
from flask import current_app, request, jsonify

from flask_jsonrpc.site import jsonrpc_site
from flask_jsonrpc._compat import (b, u, text_type, string_types,
                                   OrderedDict, NativeStringIO)
from flask_jsonrpc.types import (Object, Number, Boolean, String, Array,
                                 Nil, Any, Type)
from flask_jsonrpc.helpers import (make_response, jsonify_status_code,
                                   extract_raw_data_request, authenticate)
from flask_jsonrpc.exceptions import (Error, ParseError, InvalidRequestError,
                                      MethodNotFoundError, InvalidParamsError,
                                      ServerError, RequestPostError,
                                      InvalidCredentialsError, OtherError)

default_site = jsonrpc_site
KWARG_RE = re.compile(
    r'\s*(?P<arg_name>[a-zA-Z0-9_]+)\s*=\s*(?P<arg_type>[a-zA-Z]+)\s*$')
SIG_RE = re.compile(
    r'\s*(?P<method_name>[a-zA-Z0-9._]+)\s*(\((?P<args_sig>[^)].*)?\)'
    r'\s*(\->\s*(?P<return_sig>.*))?)?\s*$')


class JSONRPCTypeCheckingUnavailable(Exception):
    pass

def _type_checking_available(sig='', validate=False):
    if not hasattr(type, '__eq__') and validate: # and False:
        raise JSONRPCTypeCheckingUnavailable(
            'Type checking is not available in your version of Python '
            'which is only available in Python 2.6 or later. Use Python 2.6 '
            'or later or disable type checking in {0}'.format(sig))

def _validate_arg(value, expected):
    """Returns whether or not ``value`` is the ``expected`` type.
    """
    if type(value) == expected:
        return True
    return False

def _eval_arg_type(arg_type, T=Any, arg=None, sig=None):
    """Returns a type from a snippit of python source. Should normally be
    something just like 'str' or 'Object'.

        arg_type            the source to be evaluated
        T                         the default type
        arg                     context of where this type was extracted
        sig                     context from where the arg was extracted

    Returns a type or a Type
    """
    try:
        T = eval(arg_type)
    except Exception as e:
        raise ValueError('The type of {0} could not be evaluated in {1} for {2}: {3}' \
            .format(arg_type, arg, sig, text_type(e)))
    else:
        if type(T) not in (type, Type):
            raise TypeError('{0} is not a valid type in {1} for {2}' \
                .format(repr(T), arg, sig))
        return T

def _parse_sig(sig, arg_names, validate=False):
    """Parses signatures into a ``OrderedDict`` of paramName => type.
    Numerically-indexed arguments that do not correspond to an argument
    name in python (ie: it takes a variable number of arguments) will be
    keyed as the stringified version of it's index.

        sig           the signature to be parsed
        arg_names     a list of argument names extracted from python source

    Returns a tuple of (method name, types dict, return type)
    """
    d = SIG_RE.match(sig)
    if not d:
        raise ValueError('Invalid method signature {0}'.format(sig))
    d = d.groupdict()
    ret = [(n, Any) for n in arg_names]
    if text_type('args_sig') in d and type(d['args_sig']) in string_types and d['args_sig'].strip():
        for i, arg in enumerate(d['args_sig'].strip().split(',')):
            _type_checking_available(sig, validate)
            if text_type('=') in arg:
                if not type(ret) is OrderedDict:
                    ret = OrderedDict(ret)
                dk = KWARG_RE.match(arg)
                if not dk:
                    raise ValueError('Could not parse arg type {0} in {1}'.format(arg, sig))
                dk = dk.groupdict()
                if not sum([(k in dk and type(dk[k]) in string_types and bool(dk[k].strip()))
                        for k in ('arg_name', 'arg_type')]):
                    raise ValueError('Invalid kwarg value {0} in {1}'.format(arg, sig))
                ret[dk['arg_name']] = _eval_arg_type(dk['arg_type'], None, arg, sig)
            else:
                if type(ret) is OrderedDict:
                    raise ValueError('Positional arguments must occur '
                                     'before keyword arguments in {0}'.format(sig))
                if len(ret) < i + 1:
                    ret.append((text_type(i), _eval_arg_type(arg, None, arg, sig)))
                else:
                    ret[i] = (ret[i][0], _eval_arg_type(arg, None, arg, sig))
    if not type(ret) is OrderedDict:
        ret = OrderedDict(ret)
    return (d['method_name'],
                    ret,
                    (_eval_arg_type(d['return_sig'], Any, 'return', sig)
                        if d['return_sig'] else Any))

def _inject_args(sig, types):
    """A function to inject arguments manually into a method signature before
    it's been parsed. If using keyword arguments use 'kw=type' instead in
    the types array.

        sig         the string signature
        types       a list of types to be inserted

    Returns the altered signature.
    """
    if '(' in sig:
        parts = sig.split('(')
        sig = '{0}({1}{2}{3}'.format(
            parts[0], ', '.join(types),
            (', ' if parts[1].index(')') > 0 else ''), parts[1]
        )
    else:
        sig = '{0}({1})'.format(sig, ', '.join(types))
    return sig

def _site_api(site):
    def wrapper(method=''):
        response_obj, status_code = site.dispatch(request, method)
        if isinstance(response_obj, Response):
           return response_obj, response_obj.status_code
        is_batch = type(response_obj) is list
        if current_app.config['DEBUG']:
            logging.debug('request: %s', extract_raw_data_request(request))
            logging.debug('response: %s, %s', status_code, response_obj)
        return jsonify_status_code(status_code, response_obj, is_batch=is_batch), status_code
    return wrapper


class JSONRPC(object):

    def __init__(self, app=None, service_url='/api', auth_backend=authenticate, site=default_site,
                 enable_web_browsable_api=False):
        self.service_url = service_url
        self.browse_url = self._make_browse_url(service_url)
        self.enable_web_browsable_api = enable_web_browsable_api
        self.auth_backend = auth_backend
        self.site = site
        self.site_api = _site_api(site)
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def _unique_name(self, suffix=''):
        st = '.'.join((self.service_url + suffix).split('/'))
        st = st[1::] if st.startswith('.') else st
        st = st[0:-1] if st.endswith('.') else st
        return st

    def _make_browse_url(self, service_url):
        return service_url + '/browse' \
            if not service_url.endswith('/') \
            else service_url + 'browse'

    def _register_browse(self, app):
        if app.config['DEBUG'] or self.enable_web_browsable_api:
            self._enable_web_browsable_api(app)

    def _enable_web_browsable_api(self, app, url_prefix=None):
        from flask_jsonrpc.views import browse
        if url_prefix is None:
            url_prefix = self.browse_url
        self.browse_url = url_prefix
        app.register_blueprint(browse.mod, url_prefix=url_prefix,
            jsonrpc_site_name=self._unique_name(), jsonrpc_site=self.site)

    def init_app(self, app):
        self._register_browse(app)
        app.add_url_rule(self.service_url, self._unique_name(), self.site_api, methods=['POST', 'OPTIONS'])
        app.add_url_rule(self.service_url + '/<method>', self._unique_name('/<method>'), self.site_api,
                         methods=['GET', 'OPTIONS'])

    def register_blueprint(self, blueprint):
        blueprint.add_url_rule(self.service_url, '', self.site_api, methods=['POST', 'OPTIONS'])
        blueprint.add_url_rule(self.service_url + '/<method>', '', self.site_api, methods=['GET', 'OPTIONS'])

    def method(self, name, authenticated=False, safe=False, validate=False, **options):
        def decorator(f):
            arg_names = getargspec(f)[0]
            X = {'name': name, 'arg_names': arg_names}
            if authenticated:
                # TODO: this is an assumption
                X['arg_names'] = ['username', 'password'] + X['arg_names']
                X['name'] = _inject_args(X['name'], ('String', 'String'))
                _f = self.auth_backend(f, authenticated)
            else:
                _f = f
            method, arg_types, return_type = _parse_sig(X['name'], X['arg_names'], validate)
            _f.json_args = X['arg_names']
            _f.json_arg_types = arg_types
            _f.json_return_type = return_type
            _f.json_method = method
            _f.json_safe = safe
            _f.json_sig = X['name']
            _f.json_validate = validate
            self.site.register(method, _f)
            return _f
        return decorator

