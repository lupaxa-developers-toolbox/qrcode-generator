"""Payload builders — the strings that go into the QR code."""

from __future__ import annotations

import pytest

from lupaxa.qrcode_generator.exceptions import ValidationError
from lupaxa.qrcode_generator.payloads import (
    event_payload,
    geo_payload,
    sms_payload,
    url_payload,
    vcard_payload,
    wifi_payload,
)


def test_wifi_wpa_requires_password() -> None:
    with pytest.raises(ValidationError, match="password"):
        wifi_payload(ssid="Office", auth="WPA")


def test_wifi_open_omits_password() -> None:
    payload = wifi_payload(ssid="Guest", auth="nopass")
    assert payload.startswith("WIFI:")
    assert "T:nopass" in payload
    assert "S:Guest" in payload


def test_url_requires_http_scheme() -> None:
    with pytest.raises(ValidationError, match="http"):
        url_payload("example.com")
    with pytest.raises(ValidationError, match="http"):
        url_payload("ftp://example.com/file")
    assert url_payload("https://example.com/path") == "https://example.com/path"


def test_sms_rfc_and_ios_query_styles() -> None:
    assert sms_payload("+4412345", "Meet at 7?") == "sms:+4412345?body=Meet%20at%207%3F"
    assert sms_payload("+4412345", "Meet at 7?", ios=True) == "sms:+4412345&body=Meet%20at%207%3F"


def test_geo_range() -> None:
    with pytest.raises(ValidationError, match="latitude"):
        geo_payload(91.0, 0.0)
    with pytest.raises(ValidationError, match="longitude"):
        geo_payload(0.0, 181.0)
    assert geo_payload(51.5014, -0.1419) == "geo:51.5014,-0.1419"


def test_event_escapes_text_and_sets_required_fields() -> None:
    payload = event_payload(
        summary="Project review; bring laptop",
        start="20251201T190000Z",
        end="20251201T200000Z",
        location="Online, UK",
        description="Line 1\nLine 2",
        uid="fixed-uid",
        dtstamp="20250823T120000Z",
    )
    assert payload.startswith("BEGIN:VCALENDAR\r\n")
    assert "PRODID:-//The Lupaxa Project//qrcode-generator//EN" in payload
    assert "UID:fixed-uid" in payload
    assert "DTSTAMP:20250823T120000Z" in payload
    assert "SUMMARY:Project review\\; bring laptop" in payload
    assert "LOCATION:Online\\, UK" in payload
    assert "DESCRIPTION:Line 1\\nLine 2" in payload
    assert payload.endswith("END:VCALENDAR\r\n")


def test_event_rejects_bad_datetime() -> None:
    with pytest.raises(ValidationError, match="start"):
        event_payload("Meet", start="2025-12-01", end="20251201T200000Z")


def test_vcard_extra_fields() -> None:
    payload = vcard_payload(
        first_name="Simon",
        last_name="Escher",
        nickname="Simon",
        birthday="2000-01-02",
        cellphone="+44111",
        homephone="+44222",
        workphone="+44333",
        fax="+44444",
        photo_uri="https://example.com/p.jpg",
        lat=51.5,
        lng=-0.1,
    )
    assert "NICKNAME:Simon" in payload
    assert "BDAY:2000-01-02" in payload
    assert "TEL;TYPE=CELL:+44111" in payload
    assert "PHOTO" in payload
    assert "GEO:51.5;-0.1" in payload
