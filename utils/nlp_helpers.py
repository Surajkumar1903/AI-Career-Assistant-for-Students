"""
Optional NLP helpers — NLTK tokenization and spaCy entities (graceful fallbacks).

Designed for beginner-friendly setups: if models/packages are missing, callers still work.
"""
from __future__ import annotations

import re


def tokenize_words(text: str) -> list[str]:
    """
    Tokenize resume text. Tries NLTK word_tokenize; falls back to regex word tokens.
    """
    if not text:
        return []
    try:
        from nltk.tokenize import word_tokenize  # type: ignore

        return [w.lower() for w in word_tokenize(text)]
    except Exception:
        return re.findall(r"[a-zA-Z\+\#][\w\+\#\./-]*", text.lower())


def spacy_entities(text: str, max_ents: int = 12) -> list[dict]:
    """
    Extract a few named entities if spaCy's small English model is installed:
    `python -m spacy download en_core_web_sm`
    """
    if not text or len(text) < 20:
        return []
    try:
        import spacy  # type: ignore

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text[:8000])
        out = []
        for ent in doc.ents:
            if ent.label_ in {"ORG", "PRODUCT", "GPE", "PERSON"}:
                out.append({"text": ent.text, "label": ent.label_})
            if len(out) >= max_ents:
                break
        return out
    except Exception:
        return []
