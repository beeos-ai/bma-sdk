from __future__ import annotations

from typing import Optional

from anthropic import APIStatusError


def error_code(error: BaseException) -> Optional[str]:
    """BMA's reason for an API error (`error.bma_error_code` of the Anthropic
    error envelope, e.g. "idempotency_key_reused"), or None when `error` is not
    an API status error or has no code. Branch on it rather than on the message.
    (`error.code` is its deprecated spelling, read until BMA removes it on
    2026-12-01; the official `error.details.error_code` is not set by BMA.)"""
    if not isinstance(error, APIStatusError):
        return None
    body = error.body
    inner = body.get("error") if isinstance(body, dict) else None
    if not isinstance(inner, dict):
        return None
    for key in ("bma_error_code", "code"):
        code = inner.get(key)
        if isinstance(code, str) and code:
            return code
    return None
