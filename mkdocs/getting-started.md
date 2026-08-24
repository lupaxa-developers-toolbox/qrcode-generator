# Getting started

## Requirements

- Python 3.10 or newer
- [segno](https://pypi.org/project/segno/) (installed with the package)

## Install

```bash
python3 -m pip install lupaxa-qrcode-generator
python3 -m pip install 'lupaxa-qrcode-generator[logo]'  # optional centre logos
```

The PyPI name is `lupaxa-qrcode-generator`. The import path is
`lupaxa.qrcode_generator`. The console scripts are `qrcode-generator`
and `qrcodes`. `lupaxa` is a namespace package — there is no
`lupaxa/__init__.py`.

### From source (development)

```bash
make init
make python-install-dev
```

Site Markdown lives in `mkdocs/` (not GitHub’s special `docs/` directory).
After makefile-skills are installed:

```bash
make mkdocs-serve
```

## First code

```python
from lupaxa.qrcode_generator import make_text, save_qr

qr = make_text("Hello Simon")
save_qr(qr, "hello.png")
```

The same from the shell:

```bash
qrcode-generator text "Hello Simon" -o hello.png
```

The CLI prints the output path and exits `0`. Exit `2` means bad input
(invalid URL, WPA without a password, bad event datetime, and so on).

## Wi-Fi

WPA and WEP networks require `--password`. Open networks use `--auth nopass`.

```bash
qrcode-generator wifi --ssid "MyWifi" --password "Secret!" --auth WPA -o wifi.png
```

## Makefile helpers

```bash
make init                 # clone makefile-skills into .makefiles/
make python-install-dev   # editable install with [dev]
make python-check         # lint + type + test (via makefile-skills)
make mkdocs-serve         # local docs site
```
