# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Accretive namespaces. '''


from . import __
from . import objects as _objects


class Namespace( _objects.Object ): # pylint: disable=eq-without-hash
    ''' Accretive namespaces. '''

    def __init__(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **attributes: __.DictionaryNominativeArgument
    ) -> None:
        super( ).__init__( )
        super( ).__getattribute__( '__dict__' ).update(
            *iterables, **attributes )

    def __repr__( self ) -> str:
        attributes = ', '.join( tuple(
            f"{key} = {value!r}" for key, value
            in super( ).__getattribute__( '__dict__' ).items( ) ) )
        fqname = __.calculate_fqname( self )
        if not attributes: return f"{fqname}( )"
        return f"{fqname}( {attributes} )"

    def __eq__( self, other: __.a.Any ) -> __.ComparisonResult:
        mydict = super( ).__getattribute__( '__dict__' )
        if isinstance( other, ( Namespace, __.SimpleNamespace ) ):
            return mydict == other.__dict__
        return NotImplemented

    def __ne__( self, other: __.a.Any ) -> __.ComparisonResult:
        mydict = super( ).__getattribute__( '__dict__' )
        if isinstance( other, ( Namespace, __.SimpleNamespace ) ):
            return mydict != other.__dict__
        return NotImplemented

Namespace.__doc__ = __.generate_docstring(
    Namespace, 'description of namespace', 'instance attributes accretion' )
