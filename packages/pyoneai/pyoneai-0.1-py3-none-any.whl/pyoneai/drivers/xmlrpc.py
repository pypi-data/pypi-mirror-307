from types import TracebackType
from typing import Any, Literal, Self
from xml.etree.ElementTree import Element, ParseError, fromstring
from xmlrpc.client import ServerProxy

# ERRORS ===============================================================

# NOTE: Error codes, names, and messages are defined here:
# https://docs.opennebula.io/6.8/integration_and_development/system_interfaces/api.html


class _OneXMLRPCError(Exception):
    _MESSAGE = ""

    def __init__(self, message) -> None:
        super().__init__(f"{self._MESSAGE}\n{message}")


class OneXMLRPCAuthenticationError(_OneXMLRPCError):
    _MESSAGE = "User could not be authenticated."


class OneXMLRPCAuthorizationError(_OneXMLRPCError):
    _MESSAGE = "User is not authorized to perform the requested action."


class OneXMLRPCExistenceError(_OneXMLRPCError):
    _MESSAGE = "The requested resource does not exist."


class OneXMLRPCActionError(_OneXMLRPCError):
    _MESSAGE = "Wrong state to perform action."


class OneXMLRPCAPIError(_OneXMLRPCError):
    _MESSAGE = "Wrong parameters."


class OneXMLRPCInternalError(_OneXMLRPCError):
    _MESSAGE = "Internal error."


class OneXMLRPCAllocationError(_OneXMLRPCError):
    _MESSAGE = "The resource cannot be allocated."


class OneXMLRPCLockError(_OneXMLRPCError):
    _MESSAGE = "The resource is locked."


_ERRORS = {
    0x0100: OneXMLRPCAuthenticationError,
    0x0200: OneXMLRPCAuthorizationError,
    0x0400: OneXMLRPCExistenceError,
    0x0800: OneXMLRPCActionError,
    0x1000: OneXMLRPCAPIError,
    0x2000: OneXMLRPCInternalError,
    0x4000: OneXMLRPCAllocationError,
    0x8000: OneXMLRPCLockError,
}


# XML PARSING ==========================================================

# TODO: XML parsing functions need additional considerations.
# Alternatively, an external library like `xmltodict` can be used.


def _extract(element: Element) -> str | dict[str, Any] | None:
    if not element:
        return element.text

    data: dict[str, Any] = {}
    for node in element:
        result = _extract(node)
        if (node_data := data.get(node.tag)) is None:
            data[node.tag] = result
        else:
            if isinstance(node_data, list):
                node_data.append(result)
            else:
                data[node.tag] = [node_data, result]
    # data['custom_attrs'] = element.attrib
    return data


def _parse(response: str) -> dict[str, Any]:
    try:
        element = fromstring(response)
    except ParseError as err:
        raise ValueError("'response' cannot be parsed") from err

    return {element.tag: _extract(element)}


# REQUEST HANDLING =====================================================


class OnedServerProxy:
    def __init__(self, uri: str, session: str) -> None:
        self._server_proxy = ServerProxy(uri=uri)
        self._session = session

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        self.close()
        return False

    def __call__(self, method_name: str, *args) -> Any:
        resp = self.request(method_name, *args)
        if isinstance(resp, str) and resp[0] == "<" and resp[-1] == ">":
            return _parse(resp)
        return resp

    def request(self, method_name: str, *args) -> Any:
        method = getattr(self._server_proxy, method_name)
        success, body, error_code, *error_info = method(self._session, *args)
        if success:
            return body
        error = f"Error: {body}"
        code = f"Error code: {hex(error_code)}"
        info = "Error info: " + " ".join(map(str, error_info))
        raise _ERRORS[error_code](f"{error}\n{code}\n{info}")

    def close(self) -> None:
        self._server_proxy("close")()
