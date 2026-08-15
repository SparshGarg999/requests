"""
requests._types
~~~~~~~~~~~~~~~

This module contains type aliases used internally by the Requests library.
These types are not part of the public API and must not be relied upon
by external code.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, MutableMapping, Sequence
from typing import (
    TYPE_CHECKING,
    Any,
    Protocol,
    TypeAlias,
    TypeVar,
    runtime_checkable,
)

_T_co = TypeVar("_T_co", covariant=True)
_KT_co = TypeVar("_KT_co", covariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)


@runtime_checkable
class SupportsRead(Protocol[_T_co]):
    def read(self, length: int = ..., /) -> _T_co: ...


def has_read(obj: Any) -> TypeIs[SupportsRead[str | bytes]]:
    """Check if obj supports read, including __getattr__ based proxies."""
    return isinstance(obj, SupportsRead) or hasattr(obj, "read")


@runtime_checkable
class SupportsItems(Protocol[_KT_co, _VT_co]):
    def items(self) -> Iterable[tuple[_KT_co, _VT_co]]: ...


# These are needed at runtime for default_hooks() return type
HookType: TypeAlias = Callable[["Response"], Any]
HooksInputType: TypeAlias = Mapping[str, Iterable[HookType] | HookType]

if TYPE_CHECKING:
    from http.cookiejar import CookieJar
    from typing_extensions import Self, TypedDict, TypeIs

    from .cookies import RequestsCookieJar
    from .models import PreparedRequest, Request, Response

    QueryParamValue: TypeAlias = str | bytes | int | float | None
    QueryParams: TypeAlias = (
        Mapping[str, QueryParamValue | Sequence[QueryParamValue]]
        | Sequence[tuple[str, QueryParamValue]]
    )

    AuthType: TypeAlias = (
        tuple[str, str]
        | Callable[[PreparedRequest], PreparedRequest]
        | None
    )

    HeadersType: TypeAlias = (
        Mapping[str, str | bytes | None]
        | Mapping[bytes, str | bytes | None]
    )

    # Used for data= parameter
    # File-like objects, mappings, lists of tuples, strings, bytes
    DataType: TypeAlias = (
        Any
    )

    # Form tuples for files=
    FileContent: TypeAlias = (
        SupportsRead[str | bytes]
        | str
        | bytes
    )

    FileTuple2: TypeAlias = tuple[str | None, FileContent]
    FileTuple3: TypeAlias = tuple[str | None, FileContent, str]
    FileTuple4: TypeAlias = tuple[str | None, FileContent, str, Mapping[str, str]]
    FileValue: TypeAlias = (
        FileContent
        | FileTuple2
        | FileTuple3
        | FileTuple4
    )

    FilesType: TypeAlias = (
        Mapping[str, FileValue]
        | Sequence[tuple[str, FileValue]]
    )

    UriType: TypeAlias = str | bytes

    ParamsType: TypeAlias = QueryParams | bytes | str | None

    TimeoutType: TypeAlias = float | tuple[float | None, float | None] | None
    ProxiesType: TypeAlias = MutableMapping[str, str]
    HooksType: TypeAlias = dict[str, list[HookType]] | None
    VerifyType: TypeAlias = bool | str
    CertType: TypeAlias = str | tuple[str, str] | None
    JsonType: TypeAlias = (
        None
        | bool
        | int
        | float
        | str
        | Sequence["JsonType"]
        | Mapping[str, "JsonType"]
        | Any
    )

    # TypedDicts for Unpack kwargs (PEP 692)

    class BaseRequestKwargs(TypedDict, total=False):
        headers: HeadersType
        cookies: RequestsCookieJar | CookieJar | dict[str, str] | None
        files: FilesType
        auth: AuthType
        timeout: TimeoutType
        allow_redirects: bool
        proxies: dict[str, str] | None
        hooks: HooksInputType | None
        stream: bool | None
        verify: VerifyType | None
        cert: CertType

    class RequestKwargs(BaseRequestKwargs, total=False):
        """kwargs for request(), options(), head(), delete()."""

        params: ParamsType
        data: DataType
        json: JsonType

    class GetKwargs(BaseRequestKwargs, total=False):
        data: DataType
        json: JsonType

    class PostKwargs(BaseRequestKwargs, total=False):
        params: ParamsType

    class DataKwargs(BaseRequestKwargs, total=False):
        """kwargs for put(), patch()."""

        params: ParamsType
        json: JsonType
