<p align="center">
  <a href="https://github.com/lupaxa-developers-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/developers-toolbox/readme-logo.png" alt="Developers Toolbox" />
  </a>
</p>

<h1 align="center">QRCode Generator</h1>

CLI and library to generate QR codes for text, Wi-Fi, contacts, email,
SMS, locations, and calendar events.

The PyPI name is `lupaxa-qrcode-generator`. The import path is
`lupaxa.qrcode_generator`. The CLI is `qrcode-generator` (also installed
as `qrcodes`). `lupaxa` is a namespace package — there is no
`lupaxa/__init__.py`.

## Install

```bash
pip install lupaxa-qrcode-generator
pip install lupaxa-qrcode-generator[logo]  # optional centre-logo overlay (Pillow)
```

Requires Python 3.10+. Runtime dependency: [segno](https://pypi.org/project/segno/).

## Usage

Each `make_*` helper returns a `segno.QRCode` (or a `QRCodeSequence` when
`EncodeOptions(sequence=True)`). Pass that to `save_qr`. The file suffix
chooses the format (`png`, `svg`, `pdf`, and others that segno supports).
`scale` must be `>= 1`. `border` must be `>= 0`. Parent directories are
created when needed. `output="-"` writes to stdout (set `kind` for binary
formats). Invalid payloads raise `ValidationError`.

```python
from lupaxa.qrcode_generator import EncodeOptions, data_uri, make_text, make_wifi, save_qr

save_qr(make_text("Hello Simon"), "hello.png")
save_qr(make_wifi("MyWifi", password="Secret!", auth="WPA"), "wifi.png")
save_qr(
    make_text("Hello Simon", options=EncodeOptions(error="H")),
    "hello.svg",
    kind="svg",
    dark="#6D95D3",
    light="transparent",
)
print(data_uri(make_text("Hello Simon"), kind="png"))
```

```bash
qrcode-generator text "Hello Simon" -o hello.png
qrcode-generator wifi --ssid "MyWifi" --password "Secret!" --auth WPA -o wifi.png
qrcode-generator --error H --kind svg text "Hello Simon" -o hello.svg
qrcode-generator --logo logo.png text "Hello Simon" -o branded.png
qrcode-generator --version
qrcode-generator --help
```

`python -m lupaxa.qrcode_generator` is the same as the console script.
The CLI prints the output path and exits `0`. Exit `2` is bad input
(invalid URL, WPA without a password, bad event datetime, and so on).

`--password` is visible in the process list and shell history. Prefer a
throwaway guest network when you can.

## Payloads

Imported from `lupaxa.qrcode_generator`. Matching CLI subcommands:
`text`, `url`, `wifi`, `vcard`, `tel`, `email`, `sms`, `geo`, `event`.

| Name              | Role                                   |
| ----------------- | -------------------------------------- |
| `make_text`       | Plain text                             |
| `make_url`        | Absolute `http` / `https` URL          |
| `make_wifi`       | WIFI: configuration                    |
| `make_vcard`      | vCard 3.0                              |
| `make_tel`        | `tel:` URI                             |
| `make_email`      | `mailto:` URI                          |
| `make_sms`        | `sms:` URI (`ios=` for `&body=`)       |
| `make_geo`        | `geo:` URI                             |
| `make_event`      | iCalendar VEVENT                       |
| `make_qr`         | Encode an arbitrary string             |
| `save_qr`         | Write a QR code; optional centre logo  |
| `data_uri`        | PNG or SVG data URI                    |
| `EncodeOptions`   | Error, version, micro, ECI, sequence   |
| `ValidationError` | Invalid payload or save option         |

Payload string builders live in `lupaxa.qrcode_generator.payloads` if you
want the encoded text without a QR object.

## Payload Rules

**URL.** Must be an absolute `http` or `https` URL, not a bare host.

**Wi-Fi.** `--auth WPA` (default) and `WEP` require `--password`. Use
`--auth nopass` for an open network.

**SMS.** Default query is RFC-style `sms:+44...?body=...`. Add `--ios`
for the iOS `sms:+44...&body=...` form.

**Event.** `--start` and `--end` must be `YYYYMMDD`, `YYYYMMDDTHHMMSS`,
or `YYYYMMDDTHHMMSSZ`. Summary, location, and description are escaped
for iCalendar (`\\`, `\;`, `\,`, newlines).

**Geo.** Latitude is `-90` to `90`. Longitude is `-180` to `180`.

**vCard.** Extra fields: `--nickname`, `--birthday` (`YYYY-MM-DD`),
`--cellphone` / `--homephone` / `--workphone` / `--fax`, `--photo-uri`,
and `--geo-lat` / `--geo-lng`.

**Logo.** `--logo` centres an image on a PNG. Error correction is set
to `H` unless you already passed `--error H`. Rejected for Micro QR,
structured-append sequences, and non-PNG output. Needs the `[logo]`
extra. Keep `--logo-size` at or under `0.25` and scan the result before
you print it.

## Examples

```bash
qrcode-generator url "https://example.com" -o site.svg
qrcode-generator wifi --ssid "Guest" --auth nopass -o guest.png
qrcode-generator sms --number "+4412345" --message "Meet at 7?" -o sms.png
qrcode-generator geo --lat 51.5014 --lng -0.1419 -o buckingham.png
qrcode-generator event \
    --summary "Project review" \
    --start "20251201T190000Z" \
    --end "20251201T200000Z" \
    --location "Online" \
    -o event.png
qrcode-generator --data-uri png text "Hello Simon"
qrcode-generator --terminal text "Hello Simon"
qrcode-generator -o - --kind svg text "Hello Simon"
```

```python
from lupaxa.qrcode_generator import make_url, save_qr

save_qr(make_url("https://example.com"), "site.svg")
```

## Development

```bash
make init
make python-install-dev
make python-check
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
