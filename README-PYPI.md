<!-- markdownlint-disable -->
<p align="center">
  <a href="https://github.com/lupaxa-developers-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/developers-toolbox/readme-logo.png" alt="Project Logo" width="256"/><br/>
  </a>
</p>
<h3 align="center">
  The Lupaxa Developers Toolbox<br />
  Part of The Lupaxa Project
</h3>

<br />

# lupaxa-qrcode-generator

CLI and library to generate QR codes for text, Wi-Fi, contacts, email,
SMS, locations, and calendar events.

Built for scripts and tools used by The Lupaxa Project.

The PyPI name is `lupaxa-qrcode-generator`. The import path is
`lupaxa.qrcode_generator`. The CLI is installed as `qrcode-generator`
and `qrcodes`.

## Features

- Text, URL, Wi-Fi, vCard, tel, email, SMS, geo, and calendar event payloads
- Error correction, version pin, Micro QR, ECI, and structured-append sequences
- Colours, `--kind`, PNG DPI, terminal preview, data URIs, stdout, and optional centre logos (`[logo]` extra)
- Library API returns a `segno.QRCode`; `save_qr` writes PNG, SVG, and other segno formats
- CLI with `--version`, `-o` / `--scale` / `--border`, and a subcommand per type
- Wi-Fi WPA/WEP requires a password; URLs must be absolute `http` / `https`
- SMS supports RFC `?body=` and iOS `&body=` forms
- Calendar events emit escaped iCalendar with `PRODID`, `UID`, and `DTSTAMP`
- Fully typed, linted, formatted, and tested

## Installation

### From PyPI

```bash
pip install lupaxa-qrcode-generator
pip install lupaxa-qrcode-generator[logo]  # centre-logo overlay (Pillow)
```

### From source (development mode)

```bash
pip install -e ".[dev]"
```

Requires Python 3.10+. `lupaxa` is a namespace package — there is no
`lupaxa/__init__.py`.

## Usage

```python
from lupaxa.qrcode_generator import make_text, make_wifi, save_qr

save_qr(make_text("Hello Simon"), "hello.png")
save_qr(make_wifi("MyWifi", password="Secret!", auth="WPA"), "wifi.png")
```

```bash
qrcode-generator text "Hello Simon" -o hello.png
qrcode-generator wifi --ssid "MyWifi" --password "Secret!" --auth WPA -o wifi.png
qrcode-generator url "https://example.com" -o site.png
qrcode-generator --version
qrcode-generator --help
```

## Development

```bash
make init
make python-install-dev
make python-check
make mkdocs-serve
```

Documentation: <https://qrcode-generator.thelupaxaproject.org/>.

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
