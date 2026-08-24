# Usage

## Library

Each `make_*` helper returns a `segno.QRCode` (or a `QRCodeSequence` when
`EncodeOptions(sequence=True)`). Pass that to `save_qr`. The file suffix
chooses the format (`png`, `svg`, `pdf`, and others that segno supports).

```python
from lupaxa.qrcode_generator import EncodeOptions, data_uri, make_text, make_wifi, save_qr

save_qr(make_text("Hello Simon"), "hello.png", scale=10, border=4)
save_qr(make_wifi("MyWifi", password="Secret!", auth="WPA"), "wifi.svg")
save_qr(
    make_text("Hello Simon", options=EncodeOptions(error="H")),
    "hello.svg",
    kind="svg",
    dark="#6D95D3",
    light="transparent",
)
print(data_uri(make_text("Hello Simon"), kind="png"))
save_qr(
    make_text("Hello Simon", options=EncodeOptions(error="H")),
    "branded.png",
    logo="logo.png",
    logo_size=0.2,
)
```

`scale` must be `>= 1`. `border` must be `>= 0`. Parent directories are
created when needed. `output="-"` writes to stdout (set `kind` for binary
formats).

Invalid payloads raise `ValidationError`:

```python
from lupaxa.qrcode_generator import ValidationError, make_url, make_wifi

try:
    make_url("example.com")
except ValidationError:
    pass

try:
    make_wifi("Office", auth="WPA")
except ValidationError:
    pass
```

## CLI

Shared flags live on the parent parser. Subcommands encode one payload
type.

```bash
qrcode-generator --version
qrcode-generator --help
qrcode-generator text "Hello Simon" -o hello.png --scale 8 --border 4
```

| Flag                | Default      | Meaning                                      |
| ------------------- | ------------ | -------------------------------------------- |
| `-o` / `--output`   | `qrcode.png` | Output path; `-` writes to stdout            |
| `--scale`           | `10`         | Module scale (`>= 1`)                        |
| `--border`          | `4`          | Quiet zone in modules (`>= 0`)               |
| `--error`           |              | Error correction `L` / `M` / `Q` / `H`       |
| `--qr-version`      |              | Pin QR version                               |
| `--micro`           |              | Micro QR                                     |
| `--encoding`        |              | Character encoding (e.g. `utf-8`)            |
| `--eci`             |              | Include an ECI header                        |
| `--sequence`        |              | Structured append for long payloads          |
| `--symbol-count`    |              | Symbol count with `--sequence`               |
| `--dark`            |              | Dark module colour (name or hex)             |
| `--light`           |              | Light colour; `none` = transparent           |
| `--kind`            |              | Force format (`png`, `svg`, `pdf`, …)        |
| `--dpi`             |              | PNG DPI metadata                             |
| `--terminal`        |              | Print an ANSI QR to the terminal             |
| `--data-uri`        |              | Print a `png` or `svg` data URI              |
| `--logo`            |              | Centre an image (PNG out, error `H`)         |
| `--logo-size`       | `0.2`        | Logo width as a fraction (max `0.25`)        |
| `--version`         |              | Print package version and exit `0`           |

## Payload rules

**URL.** `url` is not a free-text alias. The value must be an absolute
`http` or `https` URL.

**Wi-Fi.** `--auth WPA` (default) and `WEP` require `--password`. Use
`--auth nopass` for an open network.

**SMS.** The default query is RFC-style `sms:+44...?body=...`.
Add `--ios` for the iOS `sms:+44...&body=...` form.

**Event.** `--start` and `--end` must be `YYYYMMDD`, `YYYYMMDDTHHMMSS`,
or `YYYYMMDDTHHMMSSZ`. Summary, location, and description are escaped
for iCalendar (`\\`, `\;`, `\,`, newlines).

**Geo.** Latitude is `-90` to `90`. Longitude is `-180` to `180`.

**vCard.** Extra fields: `--nickname`, `--birthday` (`YYYY-MM-DD`),
`--cellphone` / `--homephone` / `--workphone` / `--fax`, `--photo-uri`,
and `--geo-lat` / `--geo-lng`.

**Logo.** `--logo` centres an image on a PNG. Error correction is set
to `H` unless you already passed `--error H`. Rejected for Micro QR,
structured-append sequences, and non-PNG output. Needs
`pip install lupaxa-qrcode-generator[logo]` (Pillow). Keep the logo
at or under `--logo-size 0.25` and scan the result before you print it.

## Passwords on the command line

`--password` is visible in the process list and shell history. That is
normal for a local tool. Prefer a throwaway guest network when you can.
