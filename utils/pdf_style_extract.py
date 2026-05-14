"""
Extract approximate typography from a reference resume PDF (first page) via pdfplumber.
Used to mirror spacing / hierarchy in generated PDFs (Helvetica substitutes for embedded fonts).
"""
from __future__ import annotations

import os
from statistics import median
from typing import Any


def default_style_profile() -> dict[str, Any]:
    return {
        "name_pt": 20.0,
        "contact_pt": 9.0,
        "section_pt": 11.0,
        "body_pt": 10.0,
        "margins_cm": 1.45,
        "line_leading": 13.5,
        "one_page_compact": True,
        "source": "default",
    }


def extract_style_profile(pdf_path: str) -> dict[str, Any]:
    """
    Analyze first page character sizes / header band to infer name, body, section scale.
    """
    out = default_style_profile()
    out["source"] = "extracted"

    if not pdf_path or not os.path.isfile(pdf_path):
        out["source"] = "default_missing_file"
        return out

    try:
        import pdfplumber
    except ImportError:
        out["source"] = "default_no_pdfplumber"
        return out

    try:
        with pdfplumber.open(pdf_path) as pdf:
            if not pdf.pages:
                out["source"] = "default_empty_pdf"
                return out
            page = pdf.pages[0]
            chars = page.chars or []
    except Exception:
        out["source"] = "default_read_error"
        return out

    if not chars:
        out["source"] = "default_no_chars"
        return out

    sizes = [float(c["size"]) for c in chars if c.get("size")]
    if not sizes:
        return out

    tops = [float(c["top"]) for c in chars]
    band = min(tops) + 110.0
    top_chars = [c for c in chars if float(c["top"]) <= band]
    top_sizes = [float(c["size"]) for c in top_chars if c.get("size")]

    name_pt = max(top_sizes) if top_sizes else max(sizes)
    name_pt = max(16.0, min(float(name_pt), 26.0))

    body_candidates = [s for s in sizes if 8.0 <= s <= 11.5]
    body_pt = float(round(median(body_candidates), 1)) if body_candidates else 10.0

    small_candidates = [s for s in sizes if 7.5 <= s < 9.8]
    contact_pt = float(round(median(small_candidates), 1)) if small_candidates else 9.0

    section_candidates = [s for s in sizes if 10.5 <= s <= 13.5]
    section_pt = float(round(max(section_candidates), 1)) if section_candidates else 11.0
    section_pt = max(body_pt, min(section_pt, 13.5))

    # Tighter margins when many chars (one-page hint)
    n = len(chars)
    margins_cm = 1.45 if n < 2200 else 1.25

    out.update(
        {
            "name_pt": name_pt,
            "contact_pt": contact_pt,
            "section_pt": section_pt,
            "body_pt": body_pt,
            "margins_cm": margins_cm,
            "line_leading": round(body_pt * 1.35, 1),
            "one_page_compact": True,
        }
    )
    return out


def merge_with_default_reference(
    extracted: dict[str, Any],
    reference_pdf_path: str | None,
) -> dict[str, Any]:
    """If extracted failed (default source), try packaged reference PDF."""
    if extracted.get("source", "").startswith("default") and reference_pdf_path and os.path.isfile(reference_pdf_path):
        ref = extract_style_profile(reference_pdf_path)
        if not str(ref.get("source", "")).startswith("default"):
            ref["source"] = "reference_file"
            return ref
    return extracted
