"""Encoding options: error correction, version, micro, sequence, ECI."""

from __future__ import annotations

import pytest
import segno

from lupaxa.qrcode_generator import EncodeOptions, ValidationError, make_qr, make_text


def test_error_correction_h() -> None:
    qr = make_text("Hello", options=EncodeOptions(error="H"))
    assert isinstance(qr, segno.QRCode)
    assert qr.error == "H"


def test_pin_version() -> None:
    qr = make_text("Hello", options=EncodeOptions(version=5))
    assert isinstance(qr, segno.QRCode)
    assert qr.version == 5


def test_micro_qr() -> None:
    qr = make_text("Hi", options=EncodeOptions(micro=True))
    assert isinstance(qr, segno.QRCode)
    assert qr.is_micro


def test_sequence_returns_multiple_symbols() -> None:
    qr = make_qr("hello world " * 40, options=EncodeOptions(sequence=True, symbol_count=3))
    assert isinstance(qr, segno.QRCodeSequence)
    assert len(qr) == 3


def test_eci_and_encoding_utf8() -> None:
    qr = make_text("café", options=EncodeOptions(encoding="utf-8", eci=True))
    assert isinstance(qr, segno.QRCode)
    assert qr.mode is not None


def test_invalid_error_level() -> None:
    with pytest.raises(ValidationError, match="error"):
        make_text("Hello", options=EncodeOptions(error="X"))


def test_micro_and_sequence_conflict() -> None:
    with pytest.raises(ValidationError, match="sequence"):
        make_text("Hello", options=EncodeOptions(micro=True, sequence=True))
