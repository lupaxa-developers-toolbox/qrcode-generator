"""Centre-logo overlay for PNG QR codes."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import segno

from lupaxa.qrcode_generator.exceptions import ValidationError

DEFAULT_LOGO_SIZE = 0.2
MAX_LOGO_SIZE = 0.25

QRLike = segno.QRCode | segno.QRCodeSequence


def require_pillow() -> Any:
    """Import Pillow or raise a ValidationError with an install hint."""
    try:
        from PIL import Image
    except ImportError as exc:
        raise ValidationError(
            "logo overlay requires Pillow; install lupaxa-qrcode-generator[logo]"
        ) from exc
    return Image


def output_kind(output: str | Path, kind: str | None) -> str:
    """Return the writer kind for ``output``."""
    if kind:
        return kind.lower()
    if str(output) == "-":
        return "png"
    suffix = Path(str(output)).suffix.lstrip(".").lower()
    return suffix or "png"


def validate_logo_request(
    qrcode: QRLike,
    *,
    output: str | Path,
    kind: str | None,
    logo_size: float,
) -> None:
    """Reject logo overlays that scanners or writers cannot support."""
    if not isinstance(qrcode, segno.QRCode):
        raise ValidationError("logo overlay is not supported for structured-append sequences")
    if getattr(qrcode, "is_micro", False):
        raise ValidationError("logo overlay is not supported for Micro QR codes")
    error = getattr(qrcode, "error", None)
    if str(error).upper() != "H":
        raise ValidationError("logo overlay requires error correction H")
    if output_kind(output, kind) != "png":
        raise ValidationError("logo overlay is only supported for PNG output")
    if not 0 < logo_size <= MAX_LOGO_SIZE:
        raise ValidationError(f"logo size must be greater than 0 and at most {MAX_LOGO_SIZE}")


def render_png_with_logo(
    qrcode: segno.QRCode,
    logo: str | Path,
    *,
    logo_size: float,
    save_kwargs: dict[str, Any],
    dpi: int | None,
) -> bytes:
    """Render ``qrcode`` as PNG and paste ``logo`` in the centre."""
    image_cls = require_pillow()
    logo_path = Path(logo)
    if not logo_path.is_file():
        raise ValidationError(f"logo file not found: {logo_path}")

    buffer = BytesIO()
    writer_kwargs = {key: value for key, value in save_kwargs.items() if key != "kind"}
    qrcode.save(buffer, kind="png", **writer_kwargs)
    buffer.seek(0)
    qr_image = image_cls.open(buffer).convert("RGBA")
    logo_image = image_cls.open(logo_path).convert("RGBA")
    max_side = max(1, int(min(qr_image.size) * logo_size))
    logo_image.thumbnail((max_side, max_side), image_cls.Resampling.LANCZOS)
    box = (
        (qr_image.size[0] - logo_image.size[0]) // 2,
        (qr_image.size[1] - logo_image.size[1]) // 2,
    )
    qr_image.paste(logo_image, box, logo_image)
    out = BytesIO()
    png_kwargs: dict[str, Any] = {}
    if dpi is not None:
        png_kwargs["dpi"] = (dpi, dpi)
    qr_image.save(out, format="PNG", **png_kwargs)
    return out.getvalue()
