"""Build encoded payload strings for each QR type.

Helpers from ``segno`` are used where they already handle escaping.
Calendar and SMS strings are built here so they can be tested
without writing an image.
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from urllib.parse import quote, urlparse

from segno import helpers

from lupaxa.qrcode_generator.exceptions import ValidationError

_SECURE_WIFI = frozenset({"WPA", "WEP"})
_ICAL_DT_RE = re.compile(
    r"^\d{8}(?:T\d{6}Z?)?$",
)


def text_payload(text: str) -> str:
    """Return the raw text to encode."""
    if not text:
        raise ValidationError("text must not be empty")
    return text


def url_payload(url: str) -> str:
    """Return a URL after requiring an http(s) scheme."""
    if not url:
        raise ValidationError("url must not be empty")
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValidationError("url must be an absolute http or https URL")
    return url


def wifi_payload(
    ssid: str,
    password: str | None = None,
    auth: str = "WPA",
    hidden: bool = False,
) -> str:
    """Return a WIFI: configuration string."""
    if auth in _SECURE_WIFI and not password:
        raise ValidationError(f"{auth} networks require a password")
    return helpers.make_wifi_data(
        ssid=ssid,
        password=password,
        security=auth,
        hidden=hidden,
    )


def vcard_payload(
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
) -> str:
    """Return a vCard 3.0 string."""
    extras: dict[str, str] = {}
    if email:
        extras["email"] = email
    if phone:
        extras["phone"] = phone
    if org:
        extras["org"] = org
    if title:
        extras["title"] = title
    if url:
        extras["url"] = url
    if note:
        extras["memo"] = note
    if nickname:
        extras["nickname"] = nickname
    if birthday:
        extras["birthday"] = birthday
    if cellphone:
        extras["cellphone"] = cellphone
    if homephone:
        extras["homephone"] = homephone
    if workphone:
        extras["workphone"] = workphone
    if fax:
        extras["fax"] = fax
    if photo_uri:
        extras["photo_uri"] = photo_uri
    if any([street, city, region, postcode, country]):
        extras["street"] = street or ""
        extras["city"] = city or ""
        extras["region"] = region or ""
        extras["zipcode"] = postcode or ""
        extras["country"] = country or ""
    try:
        return helpers.make_vcard_data(
            name=f"{last_name};{first_name}",
            displayname=f"{first_name} {last_name}",
            lat=lat,
            lng=lng,
            **extras,
        )
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc


def tel_payload(number: str) -> str:
    """Return a tel: URI."""
    if not number:
        raise ValidationError("phone number must not be empty")
    return f"tel:{number}"


def email_payload(
    to: str,
    subject: str | None = None,
    body: str | None = None,
    cc: str | None = None,
    bcc: str | None = None,
) -> str:
    """Return a mailto: URI."""
    kwargs: dict[str, str] = {"to": to}
    if subject:
        kwargs["subject"] = subject
    if body:
        kwargs["body"] = body
    if cc:
        kwargs["cc"] = cc
    if bcc:
        kwargs["bcc"] = bcc
    # segno currently ships this as make_make_email_data (typo in the library).
    make_email_data = getattr(helpers, "make_email_data", None) or helpers.make_make_email_data
    return make_email_data(**kwargs)


def sms_payload(
    number: str,
    message: str | None = None,
    *,
    ios: bool = False,
) -> str:
    """Return an SMS URI.

    RFC-style uses ``sms:+44...?body=...`` (Android and most scanners).
    Pass ``ios=True`` for the iOS ``sms:+44...&body=...`` form.
    """
    if not number:
        raise ValidationError("phone number must not be empty")
    uri = f"sms:{number}"
    if message:
        sep = "&" if ios else "?"
        uri += f"{sep}body={quote(message)}"
    return uri


def geo_payload(lat: float, lng: float) -> str:
    """Return a geo: URI after checking latitude / longitude ranges."""
    if not -90.0 <= lat <= 90.0:
        raise ValidationError("latitude must be between -90 and 90")
    if not -180.0 <= lng <= 180.0:
        raise ValidationError("longitude must be between -180 and 180")
    return helpers.make_geo_data(lat, lng)


def _escape_ical_text(value: str) -> str:
    """Escape TEXT values per RFC 5545."""
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )


def _require_ical_datetime(label: str, value: str) -> str:
    if not _ICAL_DT_RE.match(value):
        raise ValidationError(f"{label} must be YYYYMMDD, YYYYMMDDTHHMMSS, or YYYYMMDDTHHMMSSZ")
    return value


def event_payload(
    summary: str,
    start: str,
    end: str,
    location: str | None = None,
    description: str | None = None,
    *,
    uid: str | None = None,
    dtstamp: str | None = None,
) -> str:
    """Return a VCALENDAR / VEVENT payload.

    ``start`` and ``end`` must be iCalendar date or date-time values.
    TEXT fields are escaped. ``PRODID``, ``UID``, and ``DTSTAMP`` are set.
    """
    if not summary:
        raise ValidationError("event summary must not be empty")
    start = _require_ical_datetime("start", start)
    end = _require_ical_datetime("end", end)
    if dtstamp is None:
        dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    else:
        dtstamp = _require_ical_datetime("dtstamp", dtstamp)
    if uid is None:
        uid = str(uuid.uuid4())

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//The Lupaxa Project//qrcode-generator//EN",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{dtstamp}",
        f"SUMMARY:{_escape_ical_text(summary)}",
        f"DTSTART:{start}",
        f"DTEND:{end}",
    ]
    if location:
        lines.append(f"LOCATION:{_escape_ical_text(location)}")
    if description:
        lines.append(f"DESCRIPTION:{_escape_ical_text(description)}")
    lines.extend(["END:VEVENT", "END:VCALENDAR"])
    return "\r\n".join(lines) + "\r\n"
