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
from flask_jsonrpc._compat import text_type, string_types, integer_types, reduce

def _types_gen(T):
    yield T
    if hasattr(T, 't'):
        for l in T.t:
            yield l
            if hasattr(l, 't'):
                for ll in _types_gen(l):
                    yield ll


class Type(type):
    """ A rudimentary extension to `type` that provides polymorphic
    types for run-time type checking of JSON data types. IE:

    assert type(u'') == String
    assert type('') == String
    assert type('') == Any
    assert Any.kind('') == String
    assert Any.decode('str') == String
    assert Any.kind({}) == Object
    assert Any.kind(1) == Number
    assert Any.kind(1.3333) == Number
    """

    def __init__(self, *args, **kwargs):
        super(Type, self).__init__(*args, **kwargs)

    def __eq__(self, other):
        for T in _types_gen(self):
            if isinstance(other, Type) and getattr(other, 't', False) and T in other.t:
                return True
            if type.__eq__(T, other) is True:
                return True
        return False

    def __str__(self):
        return getattr(self, '_name', 'unknown')

    def N(self, n):
        self._name = n
        return self

    def I(self, *args):
        self.t = list(args)
        return self

    def kind(self, t):
        if type(t) is Type:
            return t
        ty = lambda t: type(t)
        if type(t) is type:
            ty = lambda t: t
        return reduce(
            lambda L, R: R if (hasattr(R, 't') and ty(t) == R) else L,
            [T for T in _types_gen(self) if T is not Any])

    def decode(self, n):
        return reduce(
            lambda L, R: R if (text_type(R) == n) else L,
            _types_gen(self))

# JSON primatives and data types
Object = Type('Object', (object,), {}).I(dict).N('obj')
Number = Type('Number', (object,), {}).I(*(integer_types + (float, complex))).N('num')
Boolean = Type('Boolean', (object,), {}).I(bool).N('bool')
String = Type('String', (object,), {}).I(*string_types).N('str')
Array = Type('Array', (object,), {}).I(list, set, frozenset, tuple).N('arr')
Nil = Type('Nil', (object,), {}).I(type(None)).N('nil')
Any = Type('Any', (object,), {}).I(Object, Number, Boolean, String, Array, Nil).N('any')
