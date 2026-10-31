"""A client library for accessing BMA extensions to the Anthropic Managed Agents API"""

from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
