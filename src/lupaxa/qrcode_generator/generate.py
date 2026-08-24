"""Build ``segno.QRCode`` objects and save them."""

from __future__ import annotations

import sys
from base64 import b64encode
from pathlib import Path
from typing import Any

import segno

from lupaxa.qrcode_generator.exceptions import ValidationError
from lupaxa.qrcode_generator.logo import (
    DEFAULT_LOGO_SIZE,
    render_png_with_logo,
    validate_logo_request,
)
from lupaxa.qrcode_generator.options import EncodeOptions
from lupaxa.qrcode_generator.payloads import (
    email_payload,
    event_payload,
    geo_payload,
    sms_payload,
    tel_payload,
    text_payload,
    url_payload,
    vcard_payload,
    wifi_payload,
)

QRResult = segno.QRCode | segno.QRCodeSequence
_URI_KINDS = frozenset({"png", "svg"})


def make_qr(content: str, options: EncodeOptions | None = None) -> QRResult:
    """Encode ``content`` as a QR code, Micro QR, or structured-append sequence."""
    opts = options or EncodeOptions()
    kwargs = opts.segno_kwargs()
    if opts.sequence:
        kwargs.pop("eci", None)
        return segno.make_sequence(content, symbol_count=opts.symbol_count, **kwargs)
    if opts.micro:
        kwargs.pop("eci", None)
        return segno.make_micro(content, **kwargs)
    kwargs["micro"] = False
    return segno.make(content, **kwargs)


def _colour(value: str | None) -> str | None:
    if value is None:
        return None
    if value.lower() in {"none", "transparent"}:
        return None
    return value


def _save_kwargs(
    *,
    scale: int,
    border: int,
    dark: str | None,
    light: str | None,
    kind: str | None,
    dpi: int | None,
) -> dict[str, Any]:
    if scale < 1:
        raise ValidationError("scale must be >= 1")
    if border < 0:
        raise ValidationError("border must be >= 0")
    kwargs: dict[str, Any] = {"scale": scale, "border": border}
    if dark is not None:
        kwargs["dark"] = _colour(dark)
    if light is not None:
        kwargs["light"] = _colour(light)
    if kind:
        kwargs["kind"] = kind
    if dpi is not None:
        kwargs["dpi"] = dpi
    return kwargs


def save_qr(
    qrcode: QRResult,
    output: str | Path,
    *,
    scale: int = 10,
    border: int = 4,
    dark: str | None = None,
    light: str | None = None,
    kind: str | None = None,
    dpi: int | None = None,
    logo: str | Path | None = None,
    logo_size: float = DEFAULT_LOGO_SIZE,
) -> Path | None:
    """Save ``qrcode`` to ``output``.

    Use ``output="-"`` to write to stdout (``kind`` defaults to ``png``).
    Returns ``None`` when writing to stdout.

    ``logo`` is centred on a PNG. The QR code must use error correction H.
    """
    kwargs = _save_kwargs(scale=scale, border=border, dark=dark, light=light, kind=kind, dpi=dpi)
    if logo is not None:
        validate_logo_request(qrcode, output=output, kind=kind, logo_size=logo_size)
        assert isinstance(qrcode, segno.QRCode)
        png = render_png_with_logo(
            qrcode,
            logo,
            logo_size=logo_size,
            save_kwargs=kwargs,
            dpi=dpi,
        )
        if str(output) == "-":
            sys.stdout.buffer.write(png)
            return None
        path = Path(output)
        if path.parent != Path("."):
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(png)
        return path
    if str(output) == "-":
        out_kind = kind or "png"
        kwargs["kind"] = out_kind
        qrcode.save(sys.stdout.buffer, **kwargs)
        return None
    path = Path(output)
    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)
    qrcode.save(str(path), **kwargs)
    return path


def data_uri(
    qrcode: QRResult,
    *,
    kind: str = "png",
    scale: int = 10,
    border: int = 4,
    dark: str | None = None,
    light: str | None = None,
    logo: str | Path | None = None,
    logo_size: float = DEFAULT_LOGO_SIZE,
) -> str:
    """Return a PNG or SVG data URI for a single QR code."""
    if not isinstance(qrcode, segno.QRCode):
        raise ValidationError("data URI is only supported for a single QR code")
    if kind not in _URI_KINDS:
        raise ValidationError("data URI kind must be png or svg")
    kwargs = _save_kwargs(scale=scale, border=border, dark=dark, light=light, kind=None, dpi=None)
    if logo is not None:
        validate_logo_request(qrcode, output="qrcode.png", kind=kind, logo_size=logo_size)
        png = render_png_with_logo(
            qrcode,
            logo,
            logo_size=logo_size,
            save_kwargs=kwargs,
            dpi=None,
        )
        return "data:image/png;base64," + b64encode(png).decode("ascii")
    if kind == "svg":
        return qrcode.svg_data_uri(**kwargs)
    return qrcode.png_data_uri(**kwargs)


def make_text(text: str, options: EncodeOptions | None = None) -> QRResult:
    """QR code for plain text."""
    return make_qr(text_payload(text), options)


def make_url(url: str, options: EncodeOptions | None = None) -> QRResult:
    """QR code for an http(s) URL."""
    return make_qr(url_payload(url), options)


def make_wifi(
    ssid: str,
    password: str | None = None,
    auth: str = "WPA",
    hidden: bool = False,
    options: EncodeOptions | None = None,
) -> QRResult:
    """QR code for a Wi-Fi configuration."""
    return make_qr(
        wifi_payload(ssid, password=password, auth=auth, hidden=hidden),
        options,
    )


def make_vcard(
    first_name: str,
    last_name: str,
    email: str | None = None,
    phone: str | None = None,
    org: str | None = None,
    title: str | None = None,
    url: str | None = None,
    street: str | None = None,
    city: str | None = None,
    region: str | None = None,
    postcode: str | None = None,
    country: str | None = None,
    note: str | None = None,
    nickname: str | None = None,
    birthday: str | None = None,
    cellphone: str | None = None,
    homephone: str | None = None,
    workphone: str | None = None,
    fax: str | None = None,
    photo_uri: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
    options: EncodeOptions | None = None,
) -> QRResult:
    """QR code for a vCard."""
    return make_qr(
        vcard_payload(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            org=org,
            title=title,
            url=url,
            street=street,
            city=city,
            region=region,
            postcode=postcode,
            country=country,
            note=note,
            nickname=nickname,
            birthday=birthday,
            cellphone=cellphone,
            homephone=homephone,
            workphone=workphone,
            fax=fax,
            photo_uri=photo_uri,
            lat=lat,
            lng=lng,
        ),
        options,
    )


def make_tel(number: str, options: EncodeOptions | None = None) -> QRResult:
    """QR code for a tel: URI."""
    return make_qr(tel_payload(number), options)


def make_email(
    to: str,
    subject: str | None = None,
    body: str | None = None,
    cc: str | None = None,
    bcc: str | None = None,
    options: EncodeOptions | None = None,
) -> QRResult:
    """QR code for a mailto: URI."""
    return make_qr(
        email_payload(to=to, subject=subject, body=body, cc=cc, bcc=bcc),
        options,
    )


def make_sms(
    number: str,
    message: str | None = None,
    *,
    ios: bool = False,
    options: EncodeOptions | None = None,
) -> QRResult:
    """QR code for an SMS URI."""
    return make_qr(sms_payload(number, message, ios=ios), options)


def make_geo(lat: float, lng: float, options: EncodeOptions | None = None) -> QRResult:
    """QR code for a geographic location."""
    return make_qr(geo_payload(lat, lng), options)


def make_event(
    summary: str,
    start: str,
    end: str,
    location: str | None = None,
    description: str | None = None,
    *,
    uid: str | None = None,
    dtstamp: str | None = None,
    options: EncodeOptions | None = None,
) -> QRResult:
    """QR code for an iCalendar VEVENT."""
    return make_qr(
        event_payload(
            summary,
            start,
            end,
            location=location,
            description=description,
            uid=uid,
            dtstamp=dtstamp,
        ),
        options,
    )
