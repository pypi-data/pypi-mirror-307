from __future__ import annotations

from collections import UserDict
import functools
from typing import (
    Any,
    cast,
    Dict,
    Literal,
    Mapping,
    NoReturn,
    Optional,
    overload,
    Protocol,
    Sequence,
    Tuple,
    Union,
)

from falcon import errors
from falcon._typing import DeserializeSync
from falcon._typing import SerializeSync
from falcon.constants import MEDIA_JSON
from falcon.constants import MEDIA_MULTIPART
from falcon.constants import MEDIA_URLENCODED
from falcon.constants import PYPY
from falcon.media.base import BaseHandler
from falcon.media.base import BinaryBaseHandlerWS
from falcon.media.json import JSONHandler
from falcon.media.multipart import MultipartFormHandler
from falcon.media.multipart import MultipartParseOptions
from falcon.media.urlencoded import URLEncodedFormHandler
from falcon.util import mediatypes
from falcon.util import misc


class MissingDependencyHandler(BinaryBaseHandlerWS):
    """Placeholder handler that always raises an error.

    This handler is used by the framework for media types that require an
    external dependency that can not be found.
    """

    def __init__(self, handler: str, library: str) -> None:
        self._msg = ('The {} requires the {} library, which is not installed.').format(
            handler, library
        )

    def _raise(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise RuntimeError(self._msg)

    # TODO(kgriffs): Add support for async later if needed.
    serialize = deserialize = _raise


_ResolverMethodReturnTuple = Tuple[
    BaseHandler, Optional[SerializeSync], Optional[DeserializeSync]
]


class ResolverMethod(Protocol):
    @overload
    def __call__(
        self, media_type: Optional[str], default: str, raise_not_found: Literal[False]
    ) -> Union[Tuple[None, None, None], _ResolverMethodReturnTuple]: ...

    @overload
    def __call__(
        self,
        media_type: Optional[str],
        default: str,
        raise_not_found: Literal[True] = ...,
    ) -> _ResolverMethodReturnTuple: ...

    def __call__(
        self, media_type: Optional[str], default: str, raise_not_found: bool = True
    ) -> Union[Tuple[None, None, None], _ResolverMethodReturnTuple]: ...


class Handlers(UserDict):
    """A :class:`dict`-like object that manages Internet media type handlers."""

    data: Dict[str, BaseHandler]

    def __init__(self, initial: Optional[Mapping[str, BaseHandler]] = None) -> None:
        self._resolve: ResolverMethod = self._create_resolver()

        handlers: Mapping[str, BaseHandler] = initial or {
            MEDIA_JSON: JSONHandler(),
            MEDIA_MULTIPART: MultipartFormHandler(),
            MEDIA_URLENCODED: URLEncodedFormHandler(),
        }

        # NOTE(jmvrbanac): Directly calling UserDict as it's not inheritable.
        # Also, this results in self.update(...) being called.
        UserDict.__init__(self, handlers)

    def __setitem__(self, key: str, value: BaseHandler) -> None:
        super().__setitem__(key, value)

        # NOTE(kgriffs): When the mapping changes, we do not want to use a
        #   cached handler from the previous mapping, in case it was
        #   replaced.
        self._resolve.cache_clear()  # type: ignore[attr-defined]

    def __delitem__(self, key: str) -> None:
        super().__delitem__(key)

        # NOTE(kgriffs): Similar to __setitem__(), we need to avoid resolving
        #   to a cached handler that was removed.
        self._resolve.cache_clear()  # type: ignore[attr-defined]

    def _create_resolver(self) -> ResolverMethod:
        # PERF(kgriffs): Under PyPy the LRU is relatively expensive as compared
        #   to the common case of the self.data lookup succeeding. Using
        #   _lru_cache_for_simple_logic() takes this into account by essentially
        #   creating a nop but also decorating the method with a dummy
        #   cache_clear().
        # PERF(kgriffs): Most apps will probably only use one or two media handlers,
        #   but we use maxsize=64 to give us some wiggle room just in case someone
        #   is using versioned media types or something, and to cover various
        #   combinations of the method args. We may need to tune this later.
        @misc._lru_cache_for_simple_logic(maxsize=64)
        def resolve(
            media_type: Optional[str], default: str, raise_not_found: bool = True
        ) -> Union[Tuple[None, None, None], _ResolverMethodReturnTuple]:
            if media_type == '*/*' or not media_type:
                media_type = default

            # PERF(kgriffs): Under CPython we do not need this shortcut to
            #   improve performance since most calls will be resolved by the
            #   LRU cache on resolve(). On the other hand, it doesn't hurt,
            #   and it certainly makes a difference under PyPy.
            try:
                handler = self.data[media_type]
            except KeyError:
                handler = None

            if not handler:
                # PERF(kgriffs): We just do this slower check every time, rather
                #   than trying to first check the dict directly, since the result
                #   will almost always be cached anyway.
                # NOTE(kgriffs): Wrap keys in a tuple to make them hashable.
                matched_type = _best_match(media_type, tuple(self.data.keys()))

                if not matched_type:
                    if raise_not_found:
                        raise errors.HTTPUnsupportedMediaType(
                            description='{0} is an unsupported media type.'.format(
                                media_type
                            )
                        )

                    return None, None, None

                handler = self.data[matched_type]

            return (
                handler,
                getattr(handler, '_serialize_sync', None),
                getattr(handler, '_deserialize_sync', None),
            )

        return cast(ResolverMethod, resolve)

    def copy(self) -> Handlers:
        """Create a shallow copy of this instance of handlers.

        The resulting copy contains the same keys and values, but it can be
        customized separately without affecting the original object.

        Returns:
            A shallow copy of handlers.

        .. versionadded:: 4.0
        """
        # NOTE(vytas): In the unlikely case we are dealing with a subclass,
        #   return the matching type.
        handlers_cls = type(self)
        return handlers_cls(self.data)


def _best_match(media_type: str, all_media_types: Sequence[str]) -> Optional[str]:
    result = None

    try:
        # NOTE(jmvrbanac): Mimeparse will return an empty string if it can
        # parse the media type, but cannot find a suitable type.
        result = mediatypes.best_match(all_media_types, media_type)
    except ValueError:
        pass

    return result


if PYPY:
    # NOTE(kgriffs): The most common case for resolve() is that the
    #   direct self.data shortcut will succeed. In this case, the LRU
    #   lookup for resolve() is actually slower under PyPy than just
    #   executing the method's body each time.
    #
    #   However, if the shortcut does not succeed, invoking best_match()
    #   is relatively expensive, so it does make sense to use an LRU
    #   in that case.
    _best_match = functools.lru_cache(maxsize=64)(_best_match)  # pragma: nocover


# NOTE(vytas): An ugly way to work around circular imports.
MultipartParseOptions._DEFAULT_HANDLERS = Handlers(
    {
        MEDIA_JSON: JSONHandler(),
        MEDIA_URLENCODED: URLEncodedFormHandler(),
    }
)
