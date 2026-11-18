"""Highlighting, chart, and styling helpers."""
import html
from typing import List

import pandas as pd

VERDICT_STYLE = {
    "Safe": {"bg": "#e8f5e9", "border": "#2e7d32", "icon": "✅"},
    "Suspicious": {"bg": "#fff8e1", "border": "#f9a825", "icon": "⚠️"},
    "Likely Scam": {"bg": "#ffebee", "border": "#c62828", "icon": "🚨"},
}

HIGHLIGHT_COLORS = ["#ffd54f", "#ff8a80", "#ffab91", "#f48fb1", "#ce93d8"]


def highlight_message(text: str, phrases: list) -> str:
    """Return safe HTML of `text` with suspicious phrases wrapped in <mark>.

    Works on the ORIGINAL text for matching, then escapes every piece, so user
    text can never inject markup. Phrases not found are silently skipped.
    """
    spans = []  # (start, end, reason, color_idx)
    for i, p in enumerate(phrases or []):
        phrase = getattr(p, "phrase", "") or ""
        reason = getattr(p, "reason", "") or ""
        if not phrase.strip():
            continue
        start = text.find(phrase)
        if start == -1:  # fallback: case-insensitive
            start = text.lower().find(phrase.lower())
        if start == -1:
            continue
        spans.append((start, start + len(phrase), reason, i))

    spans.sort(key=lambda s: (s[0], -s[1]))
    merged = []
    last_end = 0
    for s in spans:  # drop overlaps
        if s[0] >= last_end:
            merged.append(s)
            last_end = s[1]

    out, pos = [], 0
    for start, end, reason, i in merged:
        out.append(html.escape(text[pos:start]))
        color = HIGHLIGHT_COLORS[i % len(HIGHLIGHT_COLORS)]
        out.append(
            f'<mark style="background:{color};padding:2px 4px;border-radius:4px;" '
            f'title="{html.escape(reason, quote=True)}">'
            f"{html.escape(text[start:end])}</mark>"
        )
        pos = end
    out.append(html.escape(text[pos:]))
    body = "".join(out).replace("\n", "<br>")
    return (
        '<div style="border:1px solid #ddd;border-radius:8px;padding:14px;'
        'line-height:1.7;background:rgba(127,127,127,0.06);">' + body + "</div>"
    )


def pressure_dataframe(profile) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Score": [
                profile.urgency,
                profile.fear,
                profile.authority,
                profile.greed,
                profile.secrecy,
            ]
        },
        index=["Urgency", "Fear", "Authority", "Greed", "Secrecy"],
    )


def verdict_card_html(report) -> str:
    st_ = VERDICT_STYLE.get(report.verdict, VERDICT_STYLE["Suspicious"])
    imp = html.escape(report.impersonating or "None")
    return f"""
<div style="background:{st_['bg']};border-left:10px solid {st_['border']};
border-radius:10px;padding:18px 22px;color:#222;">
  <div style="font-size:2em;font-weight:800;color:{st_['border']};">
    {st_['icon']} {html.escape(report.verdict)}</div>
  <div style="font-size:1.1em;margin-top:6px;">
    <b>Scam probability:</b> {report.scam_probability}% &nbsp;|&nbsp;
    <b>Type:</b> {html.escape(report.scam_type)} &nbsp;|&nbsp;
    <b>Pretending to be:</b> {imp}</div>
</div>"""


def grandma_css() -> str:
    return """
<style>
html, body, [class*="css"], .stMarkdown, .stMarkdown p, .stMarkdown li, .stButton button {
    font-size: 1.35rem !important;
}
.stButton button { padding: 0.8rem 1rem !important; }
</style>"""


def numbered(steps: List[str]) -> str:
    return "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
