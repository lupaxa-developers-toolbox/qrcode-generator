"""Errors raised by lupaxa.qrcode_generator."""

from __future__ import annotations


class QRCodeError(Exception):
    """Base error for this package."""


class ValidationError(QRCodeError, ValueError):
    """Raised when a payload or CLI argument is invalid."""
