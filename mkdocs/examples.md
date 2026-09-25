# Examples

## Text and URL

```bash
qrcode-generator text "Hello Simon" -o hello.png
qrcode-generator url "https://example.com" -o site.svg
```

```python
from lupaxa.qrcode_generator import make_text, make_url, save_qr

save_qr(make_text("Hello Simon"), "hello.png")
save_qr(make_url("https://example.com"), "site.svg")
```

## Wi-Fi

```bash
qrcode-generator wifi --ssid "MyWifi" --password "Secret!" --auth WPA -o wifi.png
qrcode-generator wifi --ssid "Guest" --auth nopass -o guest.png
```

## Contact

```bash
qrcode-generator vcard \
    --first-name "Simon" --last-name "Escher" \
    --email "simon@example.com" \
    --phone "+44123456789" \
    --cellphone "+44111" \
    --nickname "Simon" \
    --birthday "2000-01-02" \
    --org "Example Ltd" \
    --title "Engineer" \
    --url "https://example.com" \
    -o simon_vcard.png
```

## Email, SMS, Location

```bash
qrcode-generator email \
    --to "someone@example.com" \
    --subject "Hi" \
    --body "This came from a QR code" \
    -o email.png

qrcode-generator sms --number "+4412345" --message "Meet at 7?" -o sms.png
qrcode-generator sms --number "+4412345" --message "Meet at 7?" --ios -o sms-ios.png
qrcode-generator geo --lat 51.5014 --lng -0.1419 -o buckingham.png
```

## Calendar Event

```bash
qrcode-generator event \
    --summary "Project review" \
    --start "20251201T190000Z" \
    --end "20251201T200000Z" \
    --location "Online" \
    --description "Catch-up session" \
    -o event.png
```

Commas, semicolons, and newlines in the summary, location, or
description are escaped so calendar apps can parse the payload.

## Colours, SVG, and Data URIs

```bash
qrcode-generator --error H --dark "#6D95D3" --light none --kind svg \
    text "Hello Simon" -o hello.svg
qrcode-generator --data-uri png text "Hello Simon"
qrcode-generator --terminal text "Hello Simon"
qrcode-generator -o - --kind svg text "Hello Simon"
```

## Centre Logo

PNG only. The CLI sets error correction to H. Install the `logo` extra
for Pillow.

```bash
qrcode-generator --logo logo.png --logo-size 0.2 \
    text "Hello Simon" -o branded.png
```

```python
from lupaxa.qrcode_generator import EncodeOptions, make_text, save_qr

save_qr(
    make_text("Hello Simon", options=EncodeOptions(error="H")),
    "branded.png",
    logo="logo.png",
)
```
