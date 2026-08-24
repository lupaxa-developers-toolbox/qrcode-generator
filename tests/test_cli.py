"""CLI dispatch and validation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from lupaxa.qrcode_generator import __version__
from lupaxa.qrcode_generator.cli import main


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--version"]) == 0
    assert f"qrcode-generator {__version__}" in capsys.readouterr().out


def test_text_writes_png(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    output = tmp_path / "hello.png"
    assert main(["-o", str(output), "text", "Hello Simon"]) == 0
    assert output.is_file()
    assert output.stat().st_size > 0
    assert str(output) in capsys.readouterr().out


def test_wifi_wpa_without_password(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["wifi", "--ssid", "Office"]) == 2
    err = capsys.readouterr().err
    assert "error:" in err
    assert "password" in err


def test_url_rejects_bare_host() -> None:
    assert main(["url", "example.com"]) == 2


def test_module_entry_version() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "lupaxa.qrcode_generator", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert f"qrcode-generator {__version__}" in proc.stdout


def test_data_uri_does_not_write_default_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    assert main(["--data-uri", "png", "text", "Hello"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("data:image/png;base64,")
    assert not (tmp_path / "qrcode.png").exists()


def test_stdout_svg(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["-o", "-", "--kind", "svg", "text", "Hello"]) == 0
    assert "<svg" in capsys.readouterr().out


def test_removed_subcommands_are_rejected() -> None:
    for argv in (
        ["mecard", "--name", "Doe"],
        ["mms", "--number", "+4412345"],
        ["epc", "--name", "X", "--iban", "DE89", "--amount", "1", "--text", "x"],
    ):
        with pytest.raises(SystemExit):
            main(argv)


def test_vcard_extra_fields_cli(tmp_path: Path) -> None:
    output = tmp_path / "vcard.png"
    assert (
        main(
            [
                "-o",
                str(output),
                "vcard",
                "--first-name",
                "Simon",
                "--last-name",
                "Escher",
                "--nickname",
                "Simon",
                "--birthday",
                "2000-01-02",
                "--cellphone",
                "+44111",
            ]
        )
        == 0
    )
    assert output.is_file()


def test_error_correction_cli(tmp_path: Path) -> None:
    output = tmp_path / "h.png"
    assert main(["--error", "H", "-o", str(output), "text", "Hello"]) == 0
    assert output.is_file()
