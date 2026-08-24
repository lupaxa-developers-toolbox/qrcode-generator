"""Allow ``python -m lupaxa.qrcode_generator`` to run the CLI."""

from __future__ import annotations

from lupaxa.qrcode_generator.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
