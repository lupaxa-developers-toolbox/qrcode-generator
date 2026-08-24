"""lupaxa.qrcode_generator — QR codes for text, Wi-Fi, contacts, and more.

Install the ``lupaxa-qrcode-generator`` package and import this namespace.
The CLI is ``qrcode-generator``.
"""

from __future__ import annotations

from lupaxa.qrcode_generator.exceptions import QRCodeError, ValidationError
from lupaxa.qrcode_generator.generate import (
    data_uri,
    make_email,
    make_event,
    make_geo,
    make_qr,
    make_sms,
    make_tel,
    make_text,
    make_url,
    make_vcard,
    make_wifi,
    save_qr,
)
from lupaxa.qrcode_generator.options import EncodeOptions
from lupaxa.qrcode_generator.version import __version__, get_version

__all__ = [
    "EncodeOptions",
    "QRCodeError",
    "ValidationError",
    "__version__",
    "data_uri",
    "get_version",
    "make_email",
    "make_event",
    "make_geo",
    "make_qr",
    "make_sms",
    "make_tel",
    "make_text",
    "make_url",
    "make_vcard",
    "make_wifi",
    "save_qr",
]
