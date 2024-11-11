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


''' Common constants, imports, and utilities. '''

# ruff: noqa: F401
# pylint: disable=unused-import


# Note: Immutability and absence machinery is vendored from elsewhere.
#       This keeps the number of dependencies small, which is desirable for a
#       fundamental library.


from __future__ import annotations

import collections.abc as cabc

from abc import ABCMeta as ABCFactory
from functools import partial as partial_function
from inspect import cleandoc as clean_docstring
from sys import modules
from types import (
    MappingProxyType as DictionaryProxy,
    ModuleType as Module,
    NotImplementedType as TypeofNotImplemented,
    SimpleNamespace,
)

from . import _annotations as a


H = a.TypeVar( 'H', bound = cabc.Hashable )
V = a.TypeVar( 'V' ) # Value


ClassDecorators: a.TypeAlias = (
    cabc.Iterable[ cabc.Callable[ [ type ], type ] ] )
ComparisonResult: a.TypeAlias = bool | TypeofNotImplemented
DictionaryNominativeArgument: a.TypeAlias = a.Annotation[
    a.Any,
    a.Doc(
        'Zero or more keyword arguments from which to initialize '
        'dictionary data.' ),
]
# TODO: Support taking our dictionaries, themselves, as arguments.
#       Supposed to work via structural typing, but must match protocol.
#       https://github.com/python/mypy/issues/2922
#       https://github.com/python/mypy/issues/2922#issuecomment-1186587232
#       https://github.com/python/typing/discussions/1127#discussioncomment-2538837
#       https://mypy.readthedocs.io/en/latest/protocols.html
DictionaryPositionalArgument: a.TypeAlias = a.Annotation[
        cabc.Mapping[ cabc.Hashable, a.Any ]
    |   cabc.Iterable[ tuple[ cabc.Hashable, a.Any] ],
    a.Doc(
        'Zero or more iterables from which to initialize dictionary data. '
        'Each iterable must be dictionary or sequence of key-value pairs. '
        'Duplicate keys will result in an error.' ),
]
DictionaryProducer: a.TypeAlias = a.Annotation[
    cabc.Callable[ [ ], a.Any ],
    a.Doc( 'Callable which produces values for absent dictionary entries.' ),
]
DictionaryValidator: a.TypeAlias = a.Annotation[
    cabc.Callable[ [ cabc.Hashable, a.Any ], bool ],
    a.Doc( 'Callable which validates entries before addition to dictionary.' ),
]
ModuleReclassifier: a.TypeAlias = cabc.Callable[
    [ cabc.Mapping[ str, a.Any ] ], None ]


def repair_class_reproduction( original: type, reproduction: type ) -> None:
    ''' Repairs a class reproduction, if necessary. '''
    from platform import python_implementation
    match python_implementation( ):
        case 'CPython': # pragma: no branch
            _repair_cpython_class_closures( original, reproduction )


def _repair_cpython_class_closures( # pylint: disable=too-complex
    original: type, reproduction: type
) -> None:
    def try_repair_closure( function: cabc.Callable ) -> bool: # type: ignore
        try: index = function.__code__.co_freevars.index( '__class__' )
        except ValueError: return False
        closure = function.__closure__[ index ] # type: ignore
        if original is closure.cell_contents: # pragma: no branch
            closure.cell_contents = reproduction
            return True
        return False # pragma: no cover

    from inspect import isfunction, unwrap
    for attribute in reproduction.__dict__.values( ): # pylint: disable=too-many-nested-blocks
        attribute_ = unwrap( attribute )
        if isfunction( attribute_ ) and try_repair_closure( attribute_ ):
            return
        if isinstance( attribute_, property ):
            for aname in ( 'fget', 'fset', 'fdel' ):
                accessor = getattr( attribute_, aname )
                if None is accessor: continue
                if try_repair_closure( accessor ): return # pragma: no branch


_immutability_label = 'immutability'


class InternalClass( type ):
    ''' Concealment and immutability on class attributes. '''

    _class_attribute_visibility_includes_: cabc.Collection[ str ] = (
        frozenset( ) )

    def __new__(
        factory: type[ type ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, a.Any ], *,
        decorators: ClassDecorators = ( ),
        **args: a.Any
    ) -> InternalClass:
        class_ = type.__new__( factory, name, bases, namespace, **args )
        return _immutable_class__new__( # type: ignore
            class_, decorators = decorators )

    def __init__( selfclass, *posargs: a.Any, **nomargs: a.Any ):
        super( ).__init__( *posargs, **nomargs )
        _immutable_class__init__( selfclass )

    def __dir__( selfclass ) -> tuple[ str, ... ]:
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if  not name.startswith( '_' )
                or name in selfclass._class_attribute_visibility_includes_ ) )

    def __delattr__( selfclass, name: str ) -> None:
        if not _immutable_class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: a.Any ) -> None:
        if not _immutable_class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )


def _immutable_class__new__(
    original: type,
    decorators: ClassDecorators = ( ),
) -> type:
    # Some decorators create new classes, which invokes this method again.
    # Short-circuit to prevent recursive decoration and other tangles.
    decorators_ = original.__dict__.get( '_class_decorators_', [ ] )
    if decorators_: return original
    setattr( original, '_class_decorators_', decorators_ )
    reproduction = original
    for decorator in decorators:
        decorators_.append( decorator )
        reproduction = decorator( original )
        if original is not reproduction:
            repair_class_reproduction( original, reproduction )
        original = reproduction
    decorators_.clear( ) # Flag '__init__' to enable immutability.
    return reproduction


def _immutable_class__init__( class_: type ) -> None:
    # Some metaclasses add class attributes in '__init__' method.
    # So, we wait until last possible moment to set immutability.
    if class_.__dict__.get( '_class_decorators_' ): return
    del class_._class_decorators_
    if ( class_behaviors := class_.__dict__.get( '_class_behaviors_' ) ):
        class_behaviors.add( _immutability_label )
    # TODO: accretive set
    else: setattr( class_, '_class_behaviors_', { _immutability_label } )


def _immutable_class__delattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore immutable base classes.
    if _immutability_label not in class_.__dict__.get(
        '_class_behaviors_', ( )
    ): return False
    raise AttributeError(
        "Cannot delete attribute {name!r} "
        "on class {class_fqname!r}.".format(
            name = name,
            class_fqname = calculate_class_fqname( class_ ) ) )


def _immutable_class__setattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore immutable base classes.
    if _immutability_label not in class_.__dict__.get(
        '_class_behaviors_', ( )
    ): return False
    raise AttributeError(
        "Cannot assign attribute {name!r} "
        "on class {class_fqname!r}.".format(
            name = name,
            class_fqname = calculate_class_fqname( class_ ) ) )


class ConcealerExtension:
    ''' Conceals instance attributes according to some criteria.

        By default, public attributes are displayed.
    '''

    _attribute_visibility_includes_: cabc.Collection[ str ] = frozenset( )

    def __dir__( self ) -> tuple[ str, ... ]:
        return tuple( sorted(
            name for name in super( ).__dir__( )
            if  not name.startswith( '_' )
                or name in self._attribute_visibility_includes_ ) )


class InternalObject( ConcealerExtension, metaclass = InternalClass ):
    ''' Concealment and immutability on instance attributes. '''

    def __delattr__( self, name: str ) -> None:
        raise AttributeError(
            "Cannot delete attribute {name!r} on instance "
            "of class {class_fqname!r}.".format(
                name = name, class_fqname = calculate_fqname( self ) ) )

    def __setattr__( self, name: str, value: a.Any ) -> None:
        raise AttributeError(
            "Cannot assign attribute {name!r} on instance "
            "of class {class_fqname!r}.".format(
                name = name, class_fqname = calculate_fqname( self ) ) )


class Falsifier( metaclass = InternalClass ): # pylint: disable=eq-without-hash
    ''' Produces falsey objects.

        Why not something already in Python?
        :py:class:`object` produces truthy objects.
        :py:class:`types.NoneType` "produces" falsey ``None`` singleton.
        :py:class:`typing_extensions.NoDefault` is truthy singleton.
    '''

    def __bool__( self ) -> bool: return False

    def __eq__( self, other: a.Any ) -> ComparisonResult:
        return self is other

    def __ne__( self, other: a.Any ) -> ComparisonResult:
        return self is not other


class Absent( Falsifier, InternalObject ):
    ''' Type of the sentinel for option without default value. '''

    def __new__( selfclass ) -> a.Self:
        ''' Singleton. '''
        absent_ = globals( ).get( 'absent' )
        if isinstance( absent_, selfclass ): return absent_
        return super( ).__new__( selfclass )


Optional: a.TypeAlias = V | Absent
absent: a.Annotation[
    Absent, a.Doc( ''' Sentinel for option with no default value. ''' )
] = Absent( )


def is_absent( value: object ) -> a.TypeIs[ Absent ]:
    ''' Checks if a value is absent or not. '''
    return absent is value


class CoreDictionary( ConcealerExtension, dict ): # type: ignore[type-arg]
    ''' Accretive subclass of :py:class:`dict`.

        Can be used as an instance dictionary.

        Prevents attempts to mutate dictionary via inherited interface.
    '''

    def __init__(
        self,
        *iterables: DictionaryPositionalArgument,
        **entries: DictionaryNominativeArgument
    ):
        super( ).__init__( )
        self.update( *iterables, **entries )

    def __delitem__( self, key: cabc.Hashable ) -> None:
        from .exceptions import IndelibleEntryError
        raise IndelibleEntryError( key )

    def __setitem__( self, key: cabc.Hashable, value: a.Any ) -> None:
        from .exceptions import IndelibleEntryError
        if key in self: raise IndelibleEntryError( key )
        super( ).__setitem__( key, value )

    def clear( self ) -> a.Never:
        ''' Raises exception. Cannot clear indelible entries. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'clear' )

    def copy( self ) -> a.Self:
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

    def pop( # pylint: disable=unused-argument
        self, key: cabc.Hashable, default: Optional[ a.Any ] = absent
    ) -> a.Never:
        ''' Raises exception. Cannot pop indelible entry. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'pop' )

    def popitem( self ) -> a.Never:
        ''' Raises exception. Cannot pop indelible entry. '''
        from .exceptions import InvalidOperationError
        raise InvalidOperationError( 'popitem' )

    def update(
        self,
        *iterables: DictionaryPositionalArgument,
        **entries: DictionaryNominativeArgument
    ) -> a.Self:
        ''' Adds new entries as a batch. '''
        from itertools import chain
        # Add values in order received, enforcing no alteration.
        for indicator, value in chain.from_iterable( map(
            lambda element: (
                element.items( )
                if isinstance( element, cabc.Mapping )
                else element
            ),
            ( *iterables, entries )
        ) ): self[ indicator ] = value
        return self


class Docstring( str ):
    ''' Dedicated docstring container. '''


def calculate_class_fqname( class_: type ) -> str:
    ''' Calculates fully-qualified name for class. '''
    return f"{class_.__module__}.{class_.__qualname__}"


def calculate_fqname( obj: a.Any ) -> str:
    ''' Calculates fully-qualified name for class of object. '''
    class_ = type( obj )
    return f"{class_.__module__}.{class_.__qualname__}"


def discover_public_attributes(
    attributes: cabc.Mapping[ str, a.Any ]
) -> tuple[ str, ... ]:
    ''' Discovers public attributes of certain types from dictionary.

        By default, callables, including classes, are discovered.
    '''
    return tuple( sorted(
        name for name, attribute in attributes.items( )
        if not name.startswith( '_' ) and callable( attribute ) ) )


def generate_docstring(
    *fragment_ids: type | Docstring | str
) -> str:
    ''' Sews together docstring fragments into clean docstring. '''
    from inspect import cleandoc, getdoc, isclass
    from ._docstrings import TABLE
    fragments = [ ]
    for fragment_id in fragment_ids:
        if isclass( fragment_id ): fragment = getdoc( fragment_id ) or ''
        elif isinstance( fragment_id, Docstring ): fragment = fragment_id
        else: fragment = TABLE[ fragment_id ] # type: ignore
        fragments.append( cleandoc( fragment ) )
    return '\n\n'.join( fragments )


__all__ = ( )
