"""Command-line interface for lupaxa.qrcode_generator."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable

import segno

from lupaxa.qrcode_generator import __version__
from lupaxa.qrcode_generator.exceptions import ValidationError
from lupaxa.qrcode_generator.generate import (
    QRResult,
    data_uri,
    make_email,
    make_event,
    make_geo,
    make_sms,
    make_tel,
    make_text,
    make_url,
    make_vcard,
    make_wifi,
    save_qr,
)
from lupaxa.qrcode_generator.logo import DEFAULT_LOGO_SIZE
from lupaxa.qrcode_generator.options import EncodeOptions

Handler = Callable[[argparse.Namespace], QRResult]


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be >= 1")
    return parsed


def _non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be >= 0")
    return parsed


def _prepare_logo(args: argparse.Namespace) -> None:
    if not args.logo:
        return
    if args.micro:
        raise ValidationError("logo overlay is not supported for Micro QR codes")
    if args.sequence:
        raise ValidationError("logo overlay is not supported for structured-append sequences")
    if args.error and args.error != "H":
        raise ValidationError("logo overlay requires error correction H")
    args.error = "H"


def _encode_options(args: argparse.Namespace) -> EncodeOptions:
    return EncodeOptions(
        error=args.error,
        version=args.qr_version,
        micro=args.micro,
        encoding=args.encoding,
        eci=args.eci,
        sequence=args.sequence,
        symbol_count=args.symbol_count,
    )


def _cmd_text(args: argparse.Namespace) -> QRResult:
    return make_text(args.text, options=_encode_options(args))


def _cmd_url(args: argparse.Namespace) -> QRResult:
    return make_url(args.url, options=_encode_options(args))


def _cmd_wifi(args: argparse.Namespace) -> QRResult:
    return make_wifi(
        ssid=args.ssid,
        password=args.password,
        auth=args.auth,
        hidden=args.hidden,
        options=_encode_options(args),
    )


def _cmd_vcard(args: argparse.Namespace) -> QRResult:
    return make_vcard(
        first_name=args.first_name,
        last_name=args.last_name,
        email=args.email,
        phone=args.phone,
        org=args.org,
        title=args.title,
        url=args.url,
        street=args.street,
        city=args.city,
        region=args.region,
        postcode=args.postcode,
        country=args.country,
        note=args.note,
        nickname=args.nickname,
        birthday=args.birthday,
        cellphone=args.cellphone,
        homephone=args.homephone,
        workphone=args.workphone,
        fax=args.fax,
        photo_uri=args.photo_uri,
        lat=args.geo_lat,
        lng=args.geo_lng,
        options=_encode_options(args),
    )


def _cmd_tel(args: argparse.Namespace) -> QRResult:
    return make_tel(args.number, options=_encode_options(args))


def _cmd_email(args: argparse.Namespace) -> QRResult:
    return make_email(
        to=args.to,
        subject=args.subject,
        body=args.body,
        cc=args.cc,
        bcc=args.bcc,
        options=_encode_options(args),
    )


def _cmd_sms(args: argparse.Namespace) -> QRResult:
    return make_sms(args.number, args.message, ios=args.ios, options=_encode_options(args))


def _cmd_geo(args: argparse.Namespace) -> QRResult:
    return make_geo(args.lat, args.lng, options=_encode_options(args))


def _cmd_event(args: argparse.Namespace) -> QRResult:
    return make_event(
        summary=args.summary,
        start=args.start,
        end=args.end,
        location=args.location,
        description=args.description,
        options=_encode_options(args),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate QR codes for text, Wi-Fi, contacts, email, SMS, geo, and events."
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information and exit.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output filename (default: qrcode.png). Use - for stdout.",
    )
    parser.add_argument(
        "--scale",
        type=_positive_int,
        default=10,
        help="Scaling factor of the QR image (default: 10).",
    )
    parser.add_argument(
        "--border",
        type=_non_negative_int,
        default=4,
        help="Border (quiet zone) size in modules (default: 4).",
    )
    parser.add_argument(
        "--error",
        choices=["L", "M", "Q", "H"],
        help="Error correction level (default: segno chooses).",
    )
    parser.add_argument(
        "--qr-version",
        type=_positive_int,
        help="Pin QR version (1-40, or Micro M1-M4 via --micro).",
    )
    parser.add_argument("--micro", action="store_true", help="Encode as a Micro QR code.")
    parser.add_argument("--encoding", help="Character encoding for the payload (e.g. utf-8).")
    parser.add_argument("--eci", action="store_true", help="Include an ECI header.")
    parser.add_argument(
        "--sequence",
        action="store_true",
        help="Use structured append (multiple symbols) for long payloads.",
    )
    parser.add_argument(
        "--symbol-count",
        type=_positive_int,
        help="Number of symbols when using --sequence.",
    )
    parser.add_argument("--dark", help="Dark module colour (name, #RGB, or #RRGGBB).")
    parser.add_argument(
        "--light",
        help="Light module colour. Use none or transparent for a transparent background.",
    )
    parser.add_argument(
        "--kind",
        help="Force output format (png, svg, pdf, …) instead of the file suffix.",
    )
    parser.add_argument("--dpi", type=_positive_int, help="PNG DPI metadata.")
    parser.add_argument(
        "--terminal",
        action="store_true",
        help="Print an ANSI QR code to the terminal.",
    )
    parser.add_argument(
        "--data-uri",
        choices=["png", "svg"],
        help="Print a PNG or SVG data URI to stdout (skips the default file).",
    )
    parser.add_argument(
        "--logo",
        help="Image to centre on the QR code (PNG output, error correction H).",
    )
    parser.add_argument(
        "--logo-size",
        type=float,
        default=DEFAULT_LOGO_SIZE,
        help=f"Logo width as a fraction of the QR image (default: {DEFAULT_LOGO_SIZE}, max: 0.25).",
    )

    subparsers = parser.add_subparsers(dest="command")

    text_parser = subparsers.add_parser("text", help="Plain text.")
    text_parser.add_argument("text", help="Text to encode.")
    text_parser.set_defaults(handler=_cmd_text)

    url_parser = subparsers.add_parser("url", help="HTTP or HTTPS URL.")
    url_parser.add_argument("url", help="Absolute http(s) URL.")
    url_parser.set_defaults(handler=_cmd_url)

    wifi_parser = subparsers.add_parser("wifi", help="Wi-Fi configuration.")
    wifi_parser.add_argument("--ssid", required=True, help="Network name (SSID).")
    wifi_parser.add_argument("--password", help="Password (omit for open networks).")
    wifi_parser.add_argument(
        "--auth",
        choices=["WEP", "WPA", "nopass"],
        default="WPA",
        help="Authentication type (default: WPA).",
    )
    wifi_parser.add_argument(
        "--hidden",
        action="store_true",
        help="Set if the SSID is hidden.",
    )
    wifi_parser.set_defaults(handler=_cmd_wifi)

    vcard_parser = subparsers.add_parser("vcard", help="Business card (vCard).")
    vcard_parser.add_argument("--first-name", required=True, help="First name.")
    vcard_parser.add_argument("--last-name", required=True, help="Last name.")
    vcard_parser.add_argument("--email", help="Email address.")
    vcard_parser.add_argument("--phone", help="Phone number.")
    vcard_parser.add_argument("--org", help="Organisation / company.")
    vcard_parser.add_argument("--title", help="Job title / role.")
    vcard_parser.add_argument("--url", help="Website URL.")
    vcard_parser.add_argument("--street", help="Street address.")
    vcard_parser.add_argument("--city", help="City.")
    vcard_parser.add_argument("--region", help="Region / state / county.")
    vcard_parser.add_argument("--postcode", help="Postcode / ZIP.")
    vcard_parser.add_argument("--country", help="Country.")
    vcard_parser.add_argument("--note", help="Notes / memo.")
    vcard_parser.add_argument("--nickname", help="Nickname.")
    vcard_parser.add_argument("--birthday", help="Birthday as YYYY-MM-DD.")
    vcard_parser.add_argument("--cellphone", help="Mobile phone.")
    vcard_parser.add_argument("--homephone", help="Home phone.")
    vcard_parser.add_argument("--workphone", help="Work phone.")
    vcard_parser.add_argument("--fax", help="Fax number.")
    vcard_parser.add_argument("--photo-uri", help="Photo URI.")
    vcard_parser.add_argument("--geo-lat", type=float, help="Contact latitude.")
    vcard_parser.add_argument("--geo-lng", type=float, help="Contact longitude.")
    vcard_parser.set_defaults(handler=_cmd_vcard)

    tel_parser = subparsers.add_parser("tel", help="Telephone number (tel: URI).")
    tel_parser.add_argument("--number", required=True, help="Phone number.")
    tel_parser.set_defaults(handler=_cmd_tel)

    email_parser = subparsers.add_parser(
        "email", help="Email (mailto: with subject / body / cc / bcc)."
    )
    email_parser.add_argument("--to", required=True, help="Primary recipient.")
    email_parser.add_argument("--subject", help="Subject.")
    email_parser.add_argument("--body", help="Body text.")
    email_parser.add_argument("--cc", help="CC recipients (comma separated, optional).")
    email_parser.add_argument("--bcc", help="BCC recipients (comma separated, optional).")
    email_parser.set_defaults(handler=_cmd_email)

    sms_parser = subparsers.add_parser("sms", help="SMS message (sms: URI).")
    sms_parser.add_argument("--number", required=True, help="Phone number.")
    sms_parser.add_argument("--message", help="Message body.")
    sms_parser.add_argument(
        "--ios",
        action="store_true",
        help="Use iOS sms:number&body= form instead of ?body=.",
    )
    sms_parser.set_defaults(handler=_cmd_sms)

    geo_parser = subparsers.add_parser("geo", help="Geographic location (geo: URI).")
    geo_parser.add_argument("--lat", type=float, required=True, help="Latitude.")
    geo_parser.add_argument("--lng", type=float, required=True, help="Longitude.")
    geo_parser.set_defaults(handler=_cmd_geo)

    event_parser = subparsers.add_parser("event", help="Calendar event (iCalendar VEVENT).")
    event_parser.add_argument("--summary", required=True, help="Event summary / title.")
    event_parser.add_argument(
        "--start",
        required=True,
        help="Start datetime (e.g. 20251201 or 20251201T190000Z).",
    )
    event_parser.add_argument(
        "--end",
        required=True,
        help="End datetime (e.g. 20251201 or 20251201T200000Z).",
    )
    event_parser.add_argument("--location", help="Location.")
    event_parser.add_argument("--description", help="Description / notes.")
    event_parser.set_defaults(handler=_cmd_event)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"qrcode-generator {__version__}")
        return 0

    handler: Handler | None = getattr(args, "handler", None)
    if handler is None:
        parser.error("a subcommand is required unless --version is used")

    try:
        _prepare_logo(args)
        qrcode = handler(args)
        if args.terminal:
            qrcode.terminal()
        if args.data_uri:
            print(
                data_uri(
                    qrcode,
                    kind=args.data_uri,
                    scale=args.scale,
                    border=args.border,
                    dark=args.dark,
                    light=args.light,
                    logo=args.logo,
                    logo_size=args.logo_size,
                )
            )
        write_file = args.output is not None or (not args.terminal and not args.data_uri)
        if write_file:
            dest = args.output if args.output is not None else "qrcode.png"
            path = save_qr(
                qrcode,
                dest,
                scale=args.scale,
                border=args.border,
                dark=args.dark,
                light=args.light,
                kind=args.kind,
                dpi=args.dpi,
                logo=args.logo,
                logo_size=args.logo_size,
            )
            if path is not None:
                print(f"Saved QR code to {path}")
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except (ValueError, segno.DataOverflowError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    return 0
