"""ScamShield — Streamlit UI."""
from pathlib import Path

import pandas as pd
import streamlit as st

from analyzer import AnalysisError, analyze
from ui_helpers import (
    grandma_css,
    highlight_message,
    numbered,
    pressure_dataframe,
    verdict_card_html,
)

st.set_page_config(page_title="ScamShield", page_icon="🛡️", layout="wide")

SAMPLES_DIR = Path(__file__).parent / "samples"
EXAMPLES = [
    ("🏦 Fake bank alert", "1_fake_bank_alert.txt"),
    ("📱 JazzCash (Roman Urdu)", "2_wallet_roman_urdu.txt"),
    ("🎁 Prize scam", "3_prize_scam.txt"),
]
DISCLAIMER = (
    "AI-assisted analysis. It can be wrong. Never share your PIN or OTP, and always "
    "verify through your bank's official app or helpline."
)
LIMITS = (
    "ScamShield analyzes patterns in the message. It does not check live blacklists or "
    "verify that a link or phone number is currently malicious. Nothing you submit is saved."
)

TRIAGE_BUTTONS = [
    ("clicked_link", "🖱️ I clicked the link"),
    ("shared_otp_or_pin", "🔑 I shared my OTP/PIN/password"),
    ("sent_money", "💸 I sent money"),
    ("installed_app", "📲 I installed an app"),
]

# ---------- state ----------
st.session_state.setdefault("report", None)
st.session_state.setdefault("triage", None)
st.session_state.setdefault("msg_text", "")


def load_example(filename: str) -> None:
    st.session_state["msg_text"] = (SAMPLES_DIR / filename).read_text(encoding="utf-8")


# ---------- sidebar ----------
with st.sidebar:
    st.title("🛡️ ScamShield")
    st.caption("Detect. Explain. Protect your family. Recover.")
    grandma = st.toggle("👵 Grandma Mode", help="Simpler screen, bigger text, Roman Urdu first")
    st.markdown("**How to use**")
    st.markdown(
        "1. Paste the message or upload a screenshot.\n"
        "2. Press **Analyze**.\n"
        "3. Read the verdict, warn your family, and follow the steps."
    )
    st.warning(DISCLAIMER)
    st.markdown("[GitHub](https://github.com/your-username/scamshield) (placeholder link)")

if grandma:
    st.markdown(grandma_css(), unsafe_allow_html=True)

# ---------- input ----------
st.title("🛡️ ScamShield")
st.caption("Check a suspicious SMS, WhatsApp message, email, or screenshot.")

st.text_area(
    "Paste the suspicious message here",
    key="msg_text",
    height=150,
    placeholder="Paste an SMS, WhatsApp message or email here...",
)
uploaded = st.file_uploader("...or upload a screenshot", type=["png", "jpg", "jpeg"])

ex_cols = st.columns(len(EXAMPLES) + 1)
ex_cols[0].markdown("**Try an example:**")
for col, (label, fname) in zip(ex_cols[1:], EXAMPLES):
    col.button(label, on_click=load_example, args=(fname,), width="stretch")

if st.button("🔍 Analyze", type="primary", width="stretch"):
    text = st.session_state["msg_text"].strip()
    img_bytes = uploaded.getvalue() if uploaded else None
    img_mime = uploaded.type if uploaded else None
    if not text and not img_bytes:
        st.warning("Please paste a message or upload a screenshot first.")
    else:
        with st.spinner("Analyzing..."):
            try:
                st.session_state["report"] = analyze(text, img_bytes, img_mime)
                st.session_state["triage"] = None
            except AnalysisError as e:
                st.session_state["report"] = None
                st.error(str(e))
            except Exception:  # noqa: BLE001
                st.session_state["report"] = None
                st.error("Couldn't analyze. Please try again.")


# ---------- render pieces ----------
def render_highlighted(r) -> None:
    st.subheader("Your message, with suspicious parts marked")
    st.markdown(highlight_message(r.extracted_text, r.suspicious_phrases), unsafe_allow_html=True)
    shown = [p for p in r.suspicious_phrases if p.phrase and p.phrase.lower() in r.extracted_text.lower()]
    if shown:
        for p in shown:
            st.markdown(f"- **“{p.phrase}”** → {p.reason}")


def render_why(r, show_chart=True) -> None:
    st.markdown(f"**In simple words:** {r.explanation_simple}")
    st.markdown(f"**Roman Urdu:** {r.explanation_roman_urdu}")
    if r.red_flags:
        st.markdown("**Red flags**")
        for f in r.red_flags:
            st.markdown(f"- 🚩 {f}")
    if r.impersonating and r.impersonating.lower() != "none":
        st.markdown(f"**Pretending to be {r.impersonating}.** {r.impersonation_reason}")
    st.markdown("**Links, numbers and accounts found**")
    if r.extracted.urls:
        st.dataframe(
            pd.DataFrame([{"URL": u.url, "Issue": u.issue} for u in r.extracted.urls]),
            width="stretch",
            hide_index=True,
        )
    else:
        st.caption("No links found.")
    if r.extracted.phone_numbers:
        st.markdown("📞 Phone numbers: " + ", ".join(f"`{n}`" for n in r.extracted.phone_numbers))
    if r.extracted.account_numbers:
        st.markdown("🏦 Accounts/wallets: " + ", ".join(f"`{n}`" for n in r.extracted.account_numbers))
    if show_chart:
        st.markdown("**Pressure Profile** (how hard the message tries to manipulate you)")
        st.bar_chart(pressure_dataframe(r.pressure_profile), y="Score")


def render_how(r) -> None:
    h = r.how_this_scam_works
    c1, c2, c3 = st.columns(3)
    c1.info(f"**1. Hook**\n\n{h.hook}")
    c2.warning(f"**2. Pressure**\n\n{h.pressure}")
    c3.error(f"**3. Payment / data theft**\n\n{h.payment}")
    st.markdown("### Real vs Fake")
    left, right = st.columns(2)
    with left:
        st.markdown("**This message**")
        st.error(r.extracted_text)
    with right:
        st.markdown("**What a genuine message looks like**")
        st.success(r.real_vs_fake.genuine_example)
    if r.real_vs_fake.real_org_never_asks:
        st.markdown("**A real organization will never ask you for:**")
        for item in r.real_vs_fake.real_org_never_asks:
            st.markdown(f"- ❌ {item}")


def render_todo(r) -> None:
    st.markdown("**What to do now**")
    for i, s in enumerate(r.what_to_do, 1):
        st.markdown(f"{i}. {s}")
    st.markdown("**Safe reply**")
    st.code(r.safe_reply, language=None, wrap_lines=True)


def render_triage(r) -> None:
    st.markdown("### 🆘 I Already Acted")
    st.caption("Tap what happened. These steps are already prepared. No new analysis runs.")
    cols = st.columns(4)
    for col, (key, label) in zip(cols, TRIAGE_BUTTONS):
        if col.button(label, key=f"triage_{key}", width="stretch"):
            st.session_state["triage"] = key
    choice = st.session_state["triage"]
    if choice:
        steps = getattr(r.recovery_triage, choice)
        label = dict(TRIAGE_BUTTONS)[choice]
        st.error(f"**URGENT — {label}. Do these in order, starting now:**")
        if steps:
            st.markdown(numbered(steps))
        else:
            st.info("No specific steps for this case. Contact your bank through its official app.")
        st.warning(
            "Contact your bank through its official app or the helpline on your card, "
            "never a number from the message."
        )


def render_share(r) -> None:
    st.markdown("**Family warning (Roman Urdu)** — use the copy icon, then forward it")
    st.code(r.family_warning_roman_urdu, language=None, wrap_lines=True)
    st.markdown("**Report pack** — for your bank or the authorities (e.g. FIA Cyber Crime Wing)")
    st.code(r.report_text, language=None, wrap_lines=True)
    st.download_button(
        "⬇️ Download report as .txt",
        data=r.report_text,
        file_name="scamshield_report.txt",
        mime="text/plain",
    )


# ---------- results ----------
r = st.session_state["report"]
if r is not None:
    st.divider()
    st.markdown(verdict_card_html(r), unsafe_allow_html=True)
    st.progress(min(max(r.scam_probability, 0), 100) / 100, text=f"Scam probability: {r.scam_probability}%")

    if grandma:
        st.markdown(f"### {r.explanation_roman_urdu}")
        st.markdown(r.explanation_simple)
        if r.what_to_do:
            st.markdown("**Kya karein / What to do:**")
            for i, s in enumerate(r.what_to_do[:3], 1):
                st.markdown(f"{i}. {s}")
        st.markdown("**Family ko bhejein:**")
        st.code(r.family_warning_roman_urdu, language=None, wrap_lines=True)
        render_triage(r)
        with st.expander("More details"):
            render_highlighted(r)
            render_why(r, show_chart=True)
            render_how(r)
            render_todo(r)
            render_share(r)
    else:
        render_highlighted(r)
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Why it's suspicious", "How the scam works", "What to do", "Share & Report"]
        )
        with tab1:
            render_why(r)
        with tab2:
            render_how(r)
        with tab3:
            render_todo(r)
            st.divider()
            render_triage(r)
        with tab4:
            render_share(r)

    st.divider()
    if r.confidence_note:
        st.caption(f"🔎 Confidence note: {r.confidence_note}")
    st.caption(DISCLAIMER)
    st.caption(LIMITS)
else:
    st.info(LIMITS)
