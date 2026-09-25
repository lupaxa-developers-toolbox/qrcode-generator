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
as `qrcodes`).

## Install

```bash
pip install lupaxa-qrcode-generator
```

Requires Python 3.10+. Runtime dependency: [segno](https://pypi.org/project/segno/).
Centre-logo overlay needs Pillow: `pip install lupaxa-qrcode-generator[logo]`.

## Usage

```python
from lupaxa.qrcode_generator import make_text, save_qr

qr = make_text("Hello Simon")
save_qr(qr, "hello.png")
```

```bash
qrcode-generator text "Hello Simon" -o hello.png
qrcode-generator wifi --ssid "MyWifi" --password "Secret!" --auth WPA -o wifi.png
qrcode-generator --error H --kind svg text "Hello Simon" -o hello.svg
qrcode-generator --logo logo.png text "Hello Simon" -o branded.png
qrcode-generator --version
```

## Documentation

Site pages live in `mkdocs/` and publish to
<https://qrcode-generator.thelupaxaproject.org/>.

```bash
make init
make python-install-dev
make mkdocs-serve
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
