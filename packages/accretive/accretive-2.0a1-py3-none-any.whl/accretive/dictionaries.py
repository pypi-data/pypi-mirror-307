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


''' Accretive dictionaries. '''


from . import __
from . import classes as _classes
from . import objects as _objects


class _Dictionary( # type: ignore
    __.CoreDictionary, metaclass = _classes.Class
): pass


class Dictionary( # pylint: disable=eq-without-hash
    _objects.Object,
    __.a.Generic[ __.H, __.V ], # type: ignore[misc]
):
    ''' Accretive dictionary. '''

    __slots__ = ( '_data_', )

    _data_: _Dictionary

    def __init__(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> None:
        self._data_ = _Dictionary( *iterables, **entries )
        super( ).__init__( )

    def __iter__( self ) -> __.cabc.Iterator[ __.H ]:
        return iter( self._data_ )

    def __len__( self ) -> int:
        return len( self._data_ )

    def __repr__( self ) -> str:
        return "{fqname}( {contents} )".format(
            fqname = __.calculate_fqname( self ),
            contents = str( self._data_ ) )

    def __str__( self ) -> str:
        return str( self._data_ )

    def __contains__( self, key: __.cabc.Hashable ) -> bool:
        return key in self._data_

    def __delitem__( self, key: __.cabc.Hashable ) -> None:
        from .exceptions import IndelibleEntryError
        raise IndelibleEntryError( key )

    def __getitem__( self, key: __.cabc.Hashable ) -> __.a.Any:
        return self._data_[ key ]

    def __setitem__( self, key: __.cabc.Hashable, value: __.a.Any ) -> None:
        self._data_[ key ] = value

    def __eq__( self, other: __.a.Any ) -> __.ComparisonResult:
        if isinstance( other, __.cabc.Mapping ):
            return self._data_ == other
        return NotImplemented

    def __ne__( self, other: __.a.Any ) -> __.ComparisonResult:
        if isinstance( other, __.cabc.Mapping ):
            return self._data_ != other
        return NotImplemented

    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

    def get(
        self,
        key: __.cabc.Hashable,
        default: __.Optional[ __.a.Any ] = __.absent,
    ) -> __.a.Annotation[
        __.a.Any,
        __.a.Doc(
            'Value of entry, if it exists. '
            'Else, supplied default value or ``None``.' )
    ]:
        ''' Retrieves entry associated with key, if it exists. '''
        if __.is_absent( default ): return self._data_.get( key )
        return self._data_.get( key, default )

    def update(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> __.a.Self:
        ''' Adds new entries as a batch. '''
        self._data_.update( *iterables, **entries )
        return self

    def keys( self ) -> __.cabc.KeysView[ __.cabc.Hashable ]:
        ''' Provides iterable view over dictionary keys. '''
        return self._data_.keys( )

    def items( self ) -> __.cabc.ItemsView[ __.cabc.Hashable, __.a.Any ]:
        ''' Provides iterable view over dictionary items. '''
        return self._data_.items( )

    def values( self ) -> __.cabc.ValuesView[ __.a.Any ]:
        ''' Provides iterable view over dictionary values. '''
        return self._data_.values( )

Dictionary.__doc__ = __.generate_docstring(
    Dictionary,
    'dictionary entries accretion',
    'instance attributes accretion',
)
# Register as subclass of Mapping rather than use it as mixin.
# We directly implement, for the sake of efficiency, the methods which the
# mixin would provide.
__.cabc.Mapping.register( Dictionary )


class ProducerDictionary(
    Dictionary,
    __.a.Generic[ __.H, __.V ], # type: ignore[misc]
):
    ''' Accretive dictionary with default value for missing entries. '''

    __slots__ = ( '_producer_', )

    _producer_: __.DictionaryProducer

    def __init__(
        self,
        producer: __.DictionaryProducer,
        /,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument
    ):
        # TODO: Validate producer argument.
        self._producer_ = producer
        super( ).__init__( *iterables, **entries )

    def __repr__( self ) -> str:
        return "{fqname}( {producer}, {contents} )".format(
            fqname = __.calculate_fqname( self ),
            producer = self._producer_,
            contents = str( self._data_ ) )

    def __getitem__( self, key: __.cabc.Hashable ) -> __.a.Any:
        if key not in self:
            value = self._producer_( )
            self[ key ] = value
        else: value = super( ).__getitem__( key )
        return value

    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        dictionary = type( self )( self._producer_ )
        return dictionary.update( self )

ProducerDictionary.__doc__ = __.generate_docstring(
    ProducerDictionary,
    'dictionary entries accretion',
    'dictionary entries production',
    'instance attributes accretion',
)


class ValidatorDictionary(
    Dictionary,
    __.a.Generic[ __.H, __.V ], # type: ignore[misc]
):
    ''' Accretive dictionary with validation of new entries. '''

    __slots__ = ( '_validator_', )

    _validator_: __.DictionaryValidator

    def __init__(
        self,
        validator: __.DictionaryValidator,
        /,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> None:
        self._validator_ = validator
        super( ).__init__( *iterables, **entries )

    def __repr__( self ) -> str:
        return "{fqname}( {validator}, {contents} )".format(
            fqname = __.calculate_fqname( self ),
            validator = self._validator_,
            contents = str( self._data_ ) )

    def __setitem__( self, key: __.cabc.Hashable, value: __.a.Any ) -> None:
        if not self._validator_( key, value ):
            from .exceptions import EntryValidationError
            raise EntryValidationError( key, value )
        super( ).__setitem__( key, value )

    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        dictionary = type( self )( self._validator_ )
        return dictionary.update( self )

    def update(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> __.a.Self:
        ''' Adds new entries as a batch. '''
        from itertools import chain
        # Validate all entries before adding any
        for indicator, value in chain.from_iterable( map(
            lambda element: (
                element.items( )
                if isinstance( element, __.cabc.Mapping )
                else element
            ),
            ( *iterables, entries )
        ) ):
            if not self._validator_( indicator, value ):
                from .exceptions import EntryValidationError
                raise EntryValidationError( indicator, value )
        return super( ).update( *iterables, **entries )

ValidatorDictionary.__doc__ = __.generate_docstring(
    ValidatorDictionary,
    'dictionary entries accretion',
    'dictionary entries validation',
    'instance attributes accretion',
)


class ProducerValidatorDictionary(
    Dictionary,
    __.a.Generic[ __.H, __.V ], # type: ignore[misc]
):
    ''' Accretive dictionary with defaults and validation. '''

    __slots__ = ( '_producer_', '_validator_' )

    _producer_: __.DictionaryProducer
    _validator_: __.DictionaryValidator

    def __init__(
        self,
        producer: __.DictionaryProducer,
        validator: __.DictionaryValidator,
        /,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> None:
        self._producer_ = producer
        self._validator_ = validator
        super( ).__init__( *iterables, **entries )

    def __repr__( self ) -> str:
        return "{fqname}( {producer}, {validator}, {contents} )".format(
            fqname = __.calculate_fqname( self ),
            producer = self._producer_,
            validator = self._validator_,
            contents = str( self._data_ ) )

    def __getitem__( self, key: __.cabc.Hashable ) -> __.a.Any:
        if key not in self:
            value = self._producer_( )
            if not self._validator_( key, value ):
                from .exceptions import EntryValidationError
                raise EntryValidationError( key, value )
            self[ key ] = value
        else: value = super( ).__getitem__( key )
        return value

    def __setitem__( self, key: __.cabc.Hashable, value: __.a.Any ) -> None:
        if not self._validator_( key, value ):
            from .exceptions import EntryValidationError
            raise EntryValidationError( key, value )
        super( ).__setitem__( key, value )

    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        dictionary = type( self )( self._producer_, self._validator_ )
        return dictionary.update( self )

    def update(
        self,
        *iterables: __.DictionaryPositionalArgument,
        **entries: __.DictionaryNominativeArgument,
    ) -> __.a.Self:
        ''' Adds new entries as a batch. '''
        from itertools import chain
        # Validate all entries before adding any
        for indicator, value in chain.from_iterable( map(
            lambda element: (
                element.items( )
                if isinstance( element, __.cabc.Mapping )
                else element
            ),
            ( *iterables, entries )
        ) ):
            if not self._validator_( indicator, value ):
                from .exceptions import EntryValidationError
                raise EntryValidationError( indicator, value )
        return super( ).update( *iterables, **entries )

ProducerValidatorDictionary.__doc__ = __.generate_docstring(
    ProducerValidatorDictionary,
    'dictionary entries accretion',
    'dictionary entries production',
    'dictionary entries validation',
    'instance attributes accretion',
)
