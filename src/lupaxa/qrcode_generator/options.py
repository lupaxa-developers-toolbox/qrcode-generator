"""Shared encoding options for segno.make / make_micro / make_sequence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from lupaxa.qrcode_generator.exceptions import ValidationError

_ERROR_LEVELS = frozenset({"L", "M", "Q", "H"})


@dataclass(frozen=True)
class EncodeOptions:
    """Options passed through to segno when building a QR code."""

    error: str | None = None
    version: int | None = None
    micro: bool = False
    encoding: str | None = None
    eci: bool = False
    sequence: bool = False
    symbol_count: int | None = None

    def segno_kwargs(self) -> dict[str, Any]:
        """Return kwargs for ``segno.make`` / ``make_micro`` / ``make_sequence``."""
        if self.micro and self.sequence:
            raise ValidationError("micro QR codes cannot use structured-append sequence")
        kwargs: dict[str, Any] = {}
        if self.error is not None:
            level = self.error.strip().upper()
            if level not in _ERROR_LEVELS:
                raise ValidationError("error must be L, M, Q, or H")
            kwargs["error"] = level.lower()
        if self.version is not None:
            kwargs["version"] = self.version
        if self.encoding:
            kwargs["encoding"] = self.encoding
        if self.eci:
            kwargs["eci"] = True
        return kwargs
