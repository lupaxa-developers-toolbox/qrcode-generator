# QRCode Generator

CLI and library to generate QR codes for text, Wi-Fi, contacts, email,
SMS, locations, and calendar events.

Install the **`lupaxa-qrcode-generator`** package and import the
`lupaxa.qrcode_generator` namespace. Use it from Python or from the
`qrcode-generator` CLI.

```bash
pip install lupaxa-qrcode-generator
```

```python
from lupaxa.qrcode_generator import make_text, save_qr

save_qr(make_text("Hello Simon"), "hello.png")
```

```bash
qrcode-generator text "Hello Simon" -o hello.png
qrcode-generator --version
```

## What You Get

- A library that returns `segno.QRCode` objects plus `save_qr`
- Subcommands for the common payload types phones actually open
- Error correction, Micro QR, colours, data URIs, terminal preview, stdout
- Validation for Wi-Fi passwords, http(s) URLs, geo ranges, and event dates
- Python 3.10+, one runtime dependency (`segno`)
