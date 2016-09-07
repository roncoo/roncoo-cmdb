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
import uuid

from flask import json, current_app

from flask_jsonrpc.types import Object, Any
from flask_jsonrpc.site import JSONRPC_VERSION_DEFAULT
from flask_jsonrpc._compat import text_type, NativeStringIO, Request, urlopen


class ServiceProxy(object):
    DEFAULT_HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, service_url, service_name=None, version=JSONRPC_VERSION_DEFAULT, headers=None):
        self.version = text_type(version)
        self.service_url = service_url
        self.service_name = service_name
        self.headers = headers or self.DEFAULT_HEADERS

    def __getattr__(self, name):
        if self.service_name != None:
            name = '{0}.{1}'.format(self.service_name, name)
        params = dict(self.__dict__, service_name=name)
        return self.__class__(**params)

    def __repr__(self):
        return json.dumps({
            'jsonrpc': self.version,
            'method': self.service_name
        })

    def send_payload(self, params):
        """Performs the actual sending action and returns the result
        """
        data = json.dumps({
            'jsonrpc': self.version,
            'method': self.service_name,
            'params': params,
            'id': text_type(uuid.uuid4())
        })
        data_binary = data.encode('utf-8')
        url_request = Request(self.service_url, data_binary, headers=self.headers)
        return urlopen(url_request).read()

    def __call__(self, *args, **kwargs):
        params = kwargs if len(kwargs) else args
        if Any.kind(params) == Object and self.version != '2.0':
            raise Exception('Unsupport arg type for JSON-RPC 1.0 '
                            '(the default version for this client, '
                            'pass version="2.0" to use keyword arguments)')
        r = self.send_payload(params)
        y = json.loads(r)
        if 'error' in y:
            try:
                if current_app.config['DEBUG']:
                    print('{0} error {1!r}'.format(self.service_name, y))
            except:
                pass
        return y


class FakePayload(object):
    """
    A wrapper around StringIO that restricts what can be read since data from
    the network can't be seeked and cannot be read outside of its content
    length. This makes sure that views can't do anything under the test client
    that wouldn't work in Real Life.
    """
    def __init__(self, content):
        self.__content = NativeStringIO(content)
        self.__len = len(content)

    def read(self, num_bytes=None):
        if num_bytes is None:
            num_bytes = self.__len or 0
        assert self.__len >= num_bytes, 'Cannot read more than the available bytes from the HTTP incoming data.'
        content = self.__content.read(num_bytes)
        self.__len -= num_bytes
        return content


class TestingServiceProxy(ServiceProxy):
    """Service proxy which works inside Django unittests
    """

    def __init__(self, client, *args, **kwargs):
        super(TestingServiceProxy, self).__init__(*args, **kwargs)
        self.client = client

    def send_payload(self, params):
        dump = json.dumps({
            'jsonrpc': self.version,
            'method': self.service_name,
            'params': params,
            'id': text_type(uuid.uuid4())
        })
        dump_payload = FakePayload(dump)
        response = current_app.post(self.service_url, **{'wsgi.input' : dump_payload, 'CONTENT_LENGTH' : len(dump)})
        return response.content
