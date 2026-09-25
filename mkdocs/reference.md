# Reference

## Package Identity

| Item            | Value                               |
| --------------- | ----------------------------------- |
| PyPI name       | `lupaxa-qrcode-generator`           |
| Import path     | `lupaxa.qrcode_generator`           |
| Console scripts | `qrcode-generator`, `qrcodes`       |
| Module entry    | `python -m lupaxa.qrcode_generator` |

`lupaxa` is a namespace package. There is no `lupaxa/__init__.py`.

## Public API

Imported from `lupaxa.qrcode_generator`:

| Name              | Role                                      |
| ----------------- | ----------------------------------------- |
| `make_text`       | Plain text                                |
| `make_url`        | Absolute `http` / `https` URL             |
| `make_wifi`       | WIFI: configuration                       |
| `make_vcard`      | vCard 3.0                                 |
| `make_tel`        | `tel:` URI                                |
| `make_email`      | `mailto:` URI                             |
| `make_sms`        | `sms:` URI (`ios=` for `&body=`)          |
| `make_geo`        | `geo:` URI                                |
| `make_event`      | iCalendar VEVENT                          |
| `make_qr`         | Encode an arbitrary string                |
| `save_qr`         | Write a QR code; optional centre logo     |
| `data_uri`        | PNG or SVG data URI                       |
| `EncodeOptions`   | Error, version, micro, ECI, sequence      |
| `ValidationError` | Invalid payload or save option            |
| `QRCodeError`     | Base exception                            |
| `__version__`     | Package version string                    |
| `get_version`     | Same value as `__version__`               |

Payload string builders live in `lupaxa.qrcode_generator.payloads` for
tests and callers that want the encoded text without a QR object.

## CLI Exit Codes

| Code | Meaning                                      |
| ---- | -------------------------------------------- |
| `0`  | Saved a code, or `--version`                 |
| `2`  | Bad input (`ValidationError` or argparse)    |

## Subcommands

`text`, `url`, `wifi`, `vcard`, `tel`, `email`, `sms`, `geo`, `event`.
