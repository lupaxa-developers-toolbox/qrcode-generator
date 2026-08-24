"""Centre logo overlay on PNG output."""

from __future__ import annotations

from pathlib import Path

import pytest

from lupaxa.qrcode_generator import (
    EncodeOptions,
    ValidationError,
    make_qr,
    make_text,
    save_qr,
)
from lupaxa.qrcode_generator.cli import main

pytest.importorskip("PIL")

from PIL import Image  # noqa: E402


def _red_logo(path: Path) -> Path:
    Image.new("RGB", (32, 32), (255, 0, 0)).save(path)
    return path


def test_logo_paints_centre(tmp_path: Path) -> None:
    logo = _red_logo(tmp_path / "logo.png")
    output = tmp_path / "qr.png"
    save_qr(
        make_text("Hello Simon", options=EncodeOptions(error="H")),
        output,
        logo=logo,
        logo_size=0.2,
    )
    image = Image.open(output)
    centre = image.getpixel((image.size[0] // 2, image.size[1] // 2))
    assert centre[:3] == (255, 0, 0)


def test_logo_requires_error_h(tmp_path: Path) -> None:
    logo = _red_logo(tmp_path / "logo.png")
    with pytest.raises(ValidationError, match="error correction H"):
        save_qr(make_text("Hello Simon"), tmp_path / "qr.png", logo=logo)


def test_logo_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ValidationError, match="logo"):
        save_qr(
            make_text("Hello Simon", options=EncodeOptions(error="H")),
            tmp_path / "qr.png",
            logo=tmp_path / "missing.png",
        )


def test_logo_rejects_bad_size(tmp_path: Path) -> None:
    logo = _red_logo(tmp_path / "logo.png")
    qr = make_text("Hello Simon", options=EncodeOptions(error="H"))
    with pytest.raises(ValidationError, match="logo size"):
        save_qr(qr, tmp_path / "qr.png", logo=logo, logo_size=0)
    with pytest.raises(ValidationError, match="logo size"):
        save_qr(qr, tmp_path / "too-big.png", logo=logo, logo_size=0.5)


def test_logo_rejects_sequence(tmp_path: Path) -> None:
    logo = _red_logo(tmp_path / "logo.png")
    qr = make_qr(
        "hello world " * 40,
        options=EncodeOptions(sequence=True, symbol_count=3, error="H"),
    )
    with pytest.raises(ValidationError, match="sequence"):
        save_qr(qr, tmp_path / "qr.png", logo=logo)


def test_logo_rejects_micro(tmp_path: Path) -> None:
    logo = _red_logo(tmp_path / "logo.png")
    qr = make_text("Hi", options=EncodeOptions(micro=True))
    with pytest.raises(ValidationError, match="Micro"):
        save_qr(qr, tmp_path / "qr.png", logo=logo)


def test_logo_rejects_svg(tmp_path: Path) -> None:
    logo = _red_logo(tmp_path / "logo.png")
    with pytest.raises(ValidationError, match="PNG"):
        save_qr(
            make_text("Hello Simon", options=EncodeOptions(error="H")),
            tmp_path / "qr.svg",
            logo=logo,
        )


def test_logo_cli_forces_h(tmp_path: Path) -> None:
    logo = _red_logo(tmp_path / "logo.png")
    output = tmp_path / "qr.png"
    assert main(["--logo", str(logo), "-o", str(output), "text", "Hello Simon"]) == 0
    image = Image.open(output)
    centre = image.getpixel((image.size[0] // 2, image.size[1] // 2))
    assert centre[:3] == (255, 0, 0)
