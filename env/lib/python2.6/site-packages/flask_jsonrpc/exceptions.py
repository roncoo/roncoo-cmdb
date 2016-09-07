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
from flask import current_app

from flask_jsonrpc._compat import text_type

try:
    from flaskext.babel import gettext as _
    _("You're lazy...") # this function lazy-loads settings (pragma: no cover)
except (ImportError, NameError):
    _ = lambda t, *a, **k: t

class Error(Exception):
    """Error class based on the JSON-RPC 2.0 specs
    http://groups.google.com/group/json-rpc/web/json-rpc-1-2-proposal

      code    - number
      message - string
      data    - object

      status  - number    from http://groups.google.com/group/json-rpc/web/json-rpc-over-http JSON-RPC over HTTP Errors section
    """

    code = 0
    message = None
    data = None
    status = 200

    def __init__(self, message=None, code=None):
        """Setup the Exception and overwrite the default message
        """
        super(Error, self).__init__()
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    @property
    def json_rpc_format(self):
        """Return the Exception data in a format for JSON-RPC
        """

        error = {
            'name': text_type(self.__class__.__name__),
            'code': self.code,
            'message': '{0}: {1}'.format(text_type(self.__class__.__name__), text_type(self.message)),
            'data': self.data
        }

        if current_app.config['DEBUG']:
            import sys, traceback
            error['stack'] = traceback.format_exc()
            error['executable'] = sys.executable

        return error

# Exceptions
# from http://groups.google.com/group/json-rpc/web/json-rpc-1-2-proposal

# The error-codes -32768 .. -32000 (inclusive) are reserved for pre-defined errors.
# Any error-code within this range not defined explicitly below is reserved for future use

class ParseError(Error):
    """Invalid JSON. An error occurred on the server while parsing the JSON text.
    """
    code = -32700
    message = _('Parse error.')

class InvalidRequestError(Error):
    """The received JSON is not a valid JSON-RPC Request.
    """
    code = -32600
    message = _('Invalid Request.')

class MethodNotFoundError(Error):
    """The requested remote-procedure does not exist / is not available.
    """
    code = -32601
    message = _('Method not found.')

class InvalidParamsError(Error):
    """Invalid method parameters.
    """
    code = -32602
    message = _('Invalid params.')

class ServerError(Error):
    """Internal JSON-RPC error.
    """
    code = -32603
    message = _('Internal error.')

# -32099..-32000    Server error.
# Reserved for implementation-defined server-errors.

# The remainder of the space is available for application defined errors.

class RequestPostError(InvalidRequestError):
    """JSON-RPC requests must be POST
    """
    message = _('JSON-RPC requests must be POST')

class InvalidCredentialsError(Error):
    """Invalid login credentials
    """
    code = 401
    message = _('Invalid login credentials')
    status = 401

class OtherError(Error):
    """catchall error
    """
    code = 500
    message = _('Error missed by other execeptions')
    status = 200
