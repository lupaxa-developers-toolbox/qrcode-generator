"""Save options: colours, kind, dpi, data URI, stdout."""

from __future__ import annotations

from pathlib import Path

import pytest

from lupaxa.qrcode_generator import data_uri, make_text, save_qr


def test_save_kind_svg(tmp_path: Path) -> None:
    path = tmp_path / "code.bin"
    saved = save_qr(make_text("Hello"), path, kind="svg")
    assert saved == path
    text = path.read_text(encoding="utf-8")
    assert "<svg" in text


def test_save_dark_light_png(tmp_path: Path) -> None:
    path = tmp_path / "coloured.png"
    save_qr(make_text("Hello"), path, dark="#6D95D3", light="#111A32")
    assert path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_save_dpi(tmp_path: Path) -> None:
    path = tmp_path / "dpi.png"
    save_qr(make_text("Hello"), path, dpi=300)
    assert path.is_file()


def test_png_data_uri() -> None:
    uri = data_uri(make_text("Hello"), kind="png", scale=2)
    assert uri.startswith("data:image/png;base64,")


def test_svg_data_uri() -> None:
    uri = data_uri(make_text("Hello"), kind="svg")
    assert uri.startswith("data:image/svg+xml")


def test_save_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    result = save_qr(make_text("Hello"), "-", kind="svg")
    assert result is None
    out = capsys.readouterr().out
    assert "<svg" in out
