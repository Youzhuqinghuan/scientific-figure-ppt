#!/usr/bin/env python3
"""Read-only deterministic checks for scientific-figure PPTX, PNG, and PDF artifacts."""

from __future__ import annotations

import argparse
import binascii
import collections
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
import zlib
from pathlib import Path, PurePosixPath
from typing import Any


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PLACEHOLDER_RE = re.compile(
    r"(?i)(?:\bTODO\b|\bTBD\b|\bXXXX\b|\blorem\b|\bipsum\b|placeholder)"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint(path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "sha256": sha256_file(path),
    }


def add_check(
    checks: list[dict[str, Any]],
    check_id: str,
    status: str,
    target: str,
    *,
    details: dict[str, Any] | None = None,
    message: str | None = None,
) -> None:
    item: dict[str, Any] = {"id": check_id, "status": status, "target": target}
    if details:
        item["details"] = details
    if message:
        item["message"] = message
    checks.append(item)


def paeth(a: int, b: int, c: int) -> int:
    estimate = a + b - c
    pa = abs(estimate - a)
    pb = abs(estimate - b)
    pc = abs(estimate - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def inspect_png(path: Path, corner_patch: int) -> dict[str, Any]:
    raw = path.read_bytes()
    if not raw.startswith(PNG_SIGNATURE):
        raise ValueError("PNG_BAD_SIGNATURE")

    offset = len(PNG_SIGNATURE)
    chunks: list[tuple[bytes, bytes]] = []
    saw_iend = False
    while offset < len(raw):
        if offset + 12 > len(raw):
            raise ValueError("PNG_TRUNCATED_CHUNK")
        length = struct.unpack(">I", raw[offset : offset + 4])[0]
        chunk_type = raw[offset + 4 : offset + 8]
        data_start = offset + 8
        data_end = data_start + length
        crc_end = data_end + 4
        if crc_end > len(raw):
            raise ValueError("PNG_TRUNCATED_CHUNK")
        data = raw[data_start:data_end]
        expected_crc = struct.unpack(">I", raw[data_end:crc_end])[0]
        actual_crc = binascii.crc32(chunk_type)
        actual_crc = binascii.crc32(data, actual_crc) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ValueError("PNG_BAD_CRC")
        chunks.append((chunk_type, data))
        offset = crc_end
        if chunk_type == b"IEND":
            saw_iend = True
            break

    if not saw_iend:
        raise ValueError("PNG_MISSING_IEND")

    ihdrs = [data for kind, data in chunks if kind == b"IHDR"]
    if len(ihdrs) != 1 or len(ihdrs[0]) != 13:
        raise ValueError("PNG_INVALID_IHDR")
    width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(
        ">IIBBBBB", ihdrs[0]
    )
    if width <= 0 or height <= 0 or width * height > 25_000_000:
        raise ValueError("PNG_INVALID_DIMENSIONS")
    if bit_depth != 8 or color_type not in (4, 6) or interlace != 0:
        raise ValueError("PNG_UNSUPPORTED_ALPHA_FORMAT")
    if compression != 0 or filter_method != 0:
        raise ValueError("PNG_UNSUPPORTED_ENCODING")

    bytes_per_pixel = 2 if color_type == 4 else 4
    stride = width * bytes_per_pixel
    compressed = b"".join(data for kind, data in chunks if kind == b"IDAT")
    if not compressed:
        raise ValueError("PNG_MISSING_IDAT")
    try:
        scanlines = zlib.decompress(compressed)
    except zlib.error as exc:
        raise ValueError("PNG_BAD_IDAT") from exc
    expected_length = height * (stride + 1)
    if len(scanlines) != expected_length:
        raise ValueError("PNG_BAD_SCANLINE_LENGTH")

    rows: list[bytes] = []
    previous = bytearray(stride)
    cursor = 0
    for _ in range(height):
        filter_type = scanlines[cursor]
        cursor += 1
        source = scanlines[cursor : cursor + stride]
        cursor += stride
        reconstructed = bytearray(stride)
        for index, value in enumerate(source):
            left = reconstructed[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
            up = previous[index]
            upper_left = previous[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = up
            elif filter_type == 3:
                predictor = (left + up) // 2
            elif filter_type == 4:
                predictor = paeth(left, up, upper_left)
            else:
                raise ValueError("PNG_INVALID_FILTER")
            reconstructed[index] = (value + predictor) & 0xFF
        rows.append(bytes(reconstructed))
        previous = reconstructed

    alpha_index = bytes_per_pixel - 1
    all_alpha = [
        row[pixel * bytes_per_pixel + alpha_index]
        for row in rows
        for pixel in range(width)
    ]
    if not any(alpha > 0 for alpha in all_alpha):
        raise ValueError("PNG_FULLY_TRANSPARENT")

    patch = max(1, min(corner_patch, width, height))
    coordinates: list[tuple[int, int]] = []
    for y_base in (0, height - patch):
        for x_base in (0, width - patch):
            for y in range(y_base, y_base + patch):
                for x in range(x_base, x_base + patch):
                    coordinates.append((x, y))
    corner_alpha = [
        rows[y][x * bytes_per_pixel + alpha_index] for x, y in coordinates
    ]
    if any(alpha != 0 for alpha in corner_alpha):
        raise ValueError("PNG_CORNERS_NOT_TRANSPARENT")

    nonzero = sum(alpha > 0 for alpha in all_alpha)
    return {
        "width": width,
        "height": height,
        "color_type": color_type,
        "bit_depth": bit_depth,
        "corner_patch": patch,
        "nontransparent_fraction": round(nonzero / len(all_alpha), 6),
    }


def inspect_pptx(path: Path) -> dict[str, Any]:
    if not zipfile.is_zipfile(path):
        raise ValueError("PPTX_NOT_ZIP")
    required = {
        "[Content_Types].xml",
        "_rels/.rels",
        "ppt/presentation.xml",
        "ppt/slides/slide1.xml",
    }
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        duplicates = sorted(name for name, count in collections.Counter(names).items() if count > 1)
        if duplicates:
            raise ValueError("PPTX_DUPLICATE_MEMBER")
        for info in infos:
            pure = PurePosixPath(info.filename)
            if info.flag_bits & 0x1:
                raise ValueError("PPTX_ENCRYPTED_MEMBER")
            if pure.is_absolute() or ".." in pure.parts:
                raise ValueError("PPTX_UNSAFE_MEMBER")
        missing = sorted(required.difference(names))
        if missing:
            raise ValueError("PPTX_MISSING_CORE_MEMBER")
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError("PPTX_BAD_MEMBER_CRC")
        for member in ("[Content_Types].xml", "_rels/.rels", "ppt/presentation.xml"):
            try:
                ET.fromstring(archive.read(member))
            except ET.ParseError as exc:
                raise ValueError("PPTX_INVALID_CORE_XML") from exc
        slide_count = sum(
            name.startswith("ppt/slides/slide") and name.endswith(".xml") and "/_rels/" not in name
            for name in names
        )
    return {"members": len(names), "slides": slide_count}


def parse_json_output(text: str) -> dict[str, Any]:
    start = text.find("{")
    if start < 0:
        raise ValueError("OFFICECLI_INVALID_JSON")
    try:
        value = json.loads(text[start:])
    except json.JSONDecodeError as exc:
        raise ValueError("OFFICECLI_INVALID_JSON") from exc
    if not isinstance(value, dict):
        raise ValueError("OFFICECLI_INVALID_JSON")
    return value


def run_officecli(binary: str, arguments: list[str], timeout: int) -> dict[str, Any]:
    environment = os.environ.copy()
    environment.update(
        {
            "OFFICECLI_SKIP_UPDATE": "1",
            "OFFICECLI_NO_AUTO_RESIDENT": "1",
            "LC_ALL": "C",
            "LANG": "C",
            "TZ": "UTC",
        }
    )
    try:
        completed = subprocess.run(
            [binary, *arguments],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
            env=environment,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("OFFICECLI_TIMEOUT") from exc
    if completed.returncode != 0:
        raise RuntimeError("OFFICECLI_NONZERO_EXIT")
    return parse_json_output(completed.stdout)


def inspect_pdf(path: Path) -> tuple[dict[str, Any], list[str]]:
    if not path.read_bytes()[:5] == b"%PDF-":
        raise ValueError("PDF_BAD_SIGNATURE")
    details: dict[str, Any] = {"size": path.stat().st_size}
    warnings: list[str] = []
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        completed = subprocess.run(
            [pdfinfo, str(path)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60,
            check=False,
        )
        if completed.returncode == 0:
            fields: dict[str, str] = {}
            for line in completed.stdout.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    fields[key.strip()] = value.strip()
            details["pages"] = int(fields.get("Pages", "0"))
            details["page_size"] = fields.get("Page size", "")
            details["encrypted"] = fields.get("Encrypted", "unknown")
            if details["pages"] < 1:
                raise ValueError("PDF_NO_PAGES")
            if str(details["encrypted"]).lower() != "no":
                raise ValueError("PDF_ENCRYPTED")
        else:
            warnings.append("PDFINFO_FAILED")
    else:
        warnings.append("PDFINFO_NOT_FOUND")
    return details, warnings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate scientific-figure delivery artifacts.")
    parser.add_argument("--pptx", type=Path, required=True)
    parser.add_argument("--assets-dir", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    parser.add_argument("--require-assets", action="store_true")
    parser.add_argument("--corner-patch", type=int, default=3)
    parser.add_argument("--officecli", choices=("auto", "required", "skip"), default="auto")
    parser.add_argument("--officecli-bin")
    parser.add_argument("--timeout", type=int, default=90)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.corner_patch < 1 or args.timeout < 1:
        print("error: corner patch and timeout must be positive", file=sys.stderr)
        return 2

    checks: list[dict[str, Any]] = []
    warnings: list[str] = []
    qa_failed = False
    external_error = False

    pptx = args.pptx.expanduser().resolve()
    if not pptx.is_file():
        add_check(checks, "artifact:pptx", "fail", str(pptx), message="PPTX_NOT_FOUND")
        qa_failed = True
        tracked: list[Path] = []
    else:
        tracked = [pptx]
        try:
            details = inspect_pptx(pptx)
            details.update(fingerprint(pptx))
            add_check(checks, "artifact:pptx", "pass", str(pptx), details=details)
        except (OSError, ValueError, zipfile.BadZipFile) as exc:
            add_check(checks, "artifact:pptx", "fail", str(pptx), message=str(exc))
            qa_failed = True

    png_paths: list[Path] = []
    if args.assets_dir:
        assets_dir = args.assets_dir.expanduser().resolve()
        if assets_dir.is_dir():
            png_paths = sorted(assets_dir.rglob("*.png"), key=lambda path: path.as_posix())
            tracked.extend(png_paths)
        elif args.require_assets:
            add_check(checks, "assets:directory", "fail", str(assets_dir), message="ASSET_DIR_NOT_FOUND")
            qa_failed = True
    if args.require_assets and not png_paths:
        add_check(checks, "assets:png-count", "fail", str(args.assets_dir or ""), message="NO_PNG_ASSETS")
        qa_failed = True
    for path in png_paths:
        try:
            details = inspect_png(path, args.corner_patch)
            details.update(fingerprint(path))
            add_check(checks, f"asset:{path.name}", "pass", str(path), details=details)
        except (OSError, ValueError) as exc:
            add_check(checks, f"asset:{path.name}", "fail", str(path), message=str(exc))
            qa_failed = True

    pdf: Path | None = None
    if args.pdf:
        pdf = args.pdf.expanduser().resolve()
        if not pdf.is_file():
            add_check(checks, "artifact:pdf", "fail", str(pdf), message="PDF_NOT_FOUND")
            qa_failed = True
        else:
            tracked.append(pdf)
            try:
                details, pdf_warnings = inspect_pdf(pdf)
                details.update(fingerprint(pdf))
                warnings.extend(pdf_warnings)
                add_check(checks, "artifact:pdf", "pass", str(pdf), details=details)
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                add_check(checks, "artifact:pdf", "fail", str(pdf), message=str(exc))
                qa_failed = True

    before = {str(path): fingerprint(path) for path in tracked if path.is_file()}

    officecli_binary = args.officecli_bin or shutil.which("officecli")
    if args.officecli == "skip":
        add_check(checks, "officecli", "skip", str(pptx), message="OFFICECLI_SKIPPED")
    elif not officecli_binary:
        status = "error" if args.officecli == "required" else "skip"
        add_check(checks, "officecli", status, str(pptx), message="OFFICECLI_NOT_FOUND")
        if args.officecli == "required":
            external_error = True
    elif pptx.is_file():
        office_specs = (
            ("officecli:validate", ["validate", str(pptx), "--json"], "count"),
            ("officecli:issues", ["view", str(pptx), "issues", "--json"], "count"),
            (
                "officecli:no-alt",
                ["query", str(pptx), "picture:no-alt", "--json"],
                "matches",
            ),
        )
        for check_id, command, count_key in office_specs:
            try:
                payload = run_officecli(officecli_binary, command, args.timeout)
                data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
                count = data.get(count_key)
                passed = payload.get("success") is True and count == 0
                add_check(
                    checks,
                    check_id,
                    "pass" if passed else "fail",
                    str(pptx),
                    details={count_key: count},
                    message=None if passed else "OFFICECLI_REPORTED_ISSUES",
                )
                qa_failed = qa_failed or not passed
            except (RuntimeError, ValueError) as exc:
                add_check(checks, check_id, "error", str(pptx), message=str(exc))
                external_error = True

        try:
            environment = os.environ.copy()
            environment.update(
                {
                    "OFFICECLI_SKIP_UPDATE": "1",
                    "OFFICECLI_NO_AUTO_RESIDENT": "1",
                    "LC_ALL": "C",
                    "LANG": "C",
                    "TZ": "UTC",
                }
            )
            completed = subprocess.run(
                [officecli_binary, "view", str(pptx), "text"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=args.timeout,
                check=False,
                env=environment,
            )
            if completed.returncode != 0:
                raise RuntimeError("OFFICECLI_TEXT_NONZERO_EXIT")
            matches = sorted(set(match.group(0) for match in PLACEHOLDER_RE.finditer(completed.stdout)))
            passed = not matches
            add_check(
                checks,
                "officecli:placeholder-text",
                "pass" if passed else "fail",
                str(pptx),
                details={"matches": matches},
                message=None if passed else "PLACEHOLDER_TEXT_FOUND",
            )
            qa_failed = qa_failed or not passed
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            add_check(checks, "officecli:placeholder-text", "error", str(pptx), message=str(exc))
            external_error = True

    after = {str(path): fingerprint(path) for path in tracked if path.is_file()}
    mutated = sorted(path for path in before if before.get(path) != after.get(path))
    add_check(
        checks,
        "readonly:fingerprints",
        "pass" if not mutated else "fail",
        "input artifacts",
        details={"mutated": mutated},
        message=None if not mutated else "ARTIFACT_MUTATED_DURING_QA",
    )
    qa_failed = qa_failed or bool(mutated)

    counts = collections.Counter(item["status"] for item in checks)
    status = "error" if external_error else "fail" if qa_failed else "pass"
    report = {
        "schema_version": 1,
        "status": status,
        "summary": {
            "passed": counts["pass"],
            "failed": counts["fail"],
            "errors": counts["error"],
            "skipped": counts["skip"],
            "warnings": len(warnings),
        },
        "warnings": sorted(set(warnings)),
        "checks": checks,
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized, encoding="utf-8")
    else:
        sys.stdout.write(serialized)

    if external_error:
        return 3
    if qa_failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
