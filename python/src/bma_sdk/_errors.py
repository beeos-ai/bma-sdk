from __future__ import annotations

from typing import Optional

from anthropic import APIStatusError


def error_code(error: BaseException) -> Optional[str]:
    """BMA's reason for an API error (`error.code` of the Anthropic error
    envelope, e.g. "idempotency_key_reused"), or None when `error` is not an API
    status error or has no code. Branch on it rather than on the message.
    (The official `error.details.error_code` is not set by BMA.)"""
    if not isinstance(error, APIStatusError):
        return None
    body = error.body
    inner = body.get("error") if isinstance(body, dict) else None
    code = inner.get("code") if isinstance(inner, dict) else None
    return code if isinstance(code, str) else None
