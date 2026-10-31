"""Python client for the BMA REST API.

* :mod:`bma_sdk.rest` - generated from ``contracts/bma/rest.openapi.yaml``.
* :class:`BmaClient` - authentication, event stream, verified artifact downloads.
* :mod:`bma_sdk.facade_extensions` - BMA extensions to the Anthropic Managed
  Agents API (not part of the Anthropic contract).
"""

from .client import DEFAULT_BASE_URL, SDK_VERSION, BmaApiError, BmaClient, StreamFrame, parse_sse, unwrap

__version__ = SDK_VERSION
__all__ = ["DEFAULT_BASE_URL", "SDK_VERSION", "BmaApiError", "BmaClient", "StreamFrame", "parse_sse", "unwrap"]
