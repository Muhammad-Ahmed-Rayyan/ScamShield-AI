# ScamShield — Full Project Specification

> **Instruction to the AI/agent reading this file:** Build the project exactly as described below. The whole app must be buildable and running in **under 45 minutes** as a live-hackathon entry. Prioritize a working, demo-ready app over polish. Follow the build order in Section 14. Do not add features that are not listed here. Do not add a database or a backend server beyond the Streamlit app.

---

## 1. One-Line Summary

**ScamShield** is an open-source web app that analyzes a suspicious SMS, WhatsApp message, email, or screenshot with the Gemini API, tells the user whether it is a scam, **explains why**, **warns their family in Roman Urdu**, **helps them recover if they already acted**, and **generates a report** to send to their bank or authorities.

**Tagline:** *Detect. Explain. Protect your family. Recover.*

## 2. The Problem

- Scam messages (fake bank alerts, JazzCash/Easypaisa impersonation, prize scams, job scams, courier/FBR fake notices) look more real every day.
- The people most at risk (parents, elders, first-time digital payment users) have nobody to ask.
- Most existing scam checkers only say "scam / not scam." They do **not**:
  - explain the manipulation tactics so users learn to spot them next time,
  - help the person who **already clicked, shared an OTP, or sent money**,
  - produce a warning the family can understand in their own language,
  - produce an evidence pack for reporting.

## 3. Target Users

- Everyday users and families in Pakistan (English, Urdu, and Roman Urdu messages)
- Elderly relatives and first-time mobile-wallet users ("Grandma Mode")
- Small shop owners receiving fake payment screenshots/messages
- Fintech apps and banks (can fork and embed it, since it is open source)

## 4. Tech Stack (keep it minimal)

| Part | Choice |
|---|---|
| Language | Python 3.10+ |
| UI | Streamlit |
| AI | Gemini API via the official `google-genai` SDK |
| Model | A current Gemini **Flash** model (fast and cheap). Read the name from env var `GEMINI_MODEL`, with a sensible default (check Google AI Studio for the current Flash model name). |
| Validation | Pydantic (for the response schema) |
| Config | `python-dotenv`, key in `GEMINI_API_KEY` |
| License | MIT |

**No database. No login. No separate backend. One Gemini call per analysis.**

## 5. Project Structure

```
scamshield/
├── app.py                 # Streamlit UI
├── analyzer.py            # Gemini call + schema + prompt
├── schema.py              # Pydantic models for the JSON response
├── prompts.py             # System prompt text
├── ui_helpers.py          # Highlighting, chart, copy-button helpers
├── samples/               # Sample test messages (txt)
├── requirements.txt
├── .env.example           # GEMINI_API_KEY=your_key_here
├── .gitignore             # must include .env
├── README.md
└── LICENSE                # MIT
```

`requirements.txt`:
```
streamlit
google-genai
pydantic
python-dotenv
pandas
```

## 6. Features to Build (all in scope)

### Core
1. **Multi-channel input.** A text box for pasted SMS/WhatsApp/email text, and an image uploader for screenshots (PNG/JPG). The user can use either. If both are given, send both.
2. **Link, phone, and account extractor.** List every URL, phone number, and account/wallet number found. For each URL, flag problems such as lookalike domains, odd TLDs, URL shorteners, or a mismatch with the claimed brand (e.g. `hbl-secure-login.xyz`).
3. **Impersonation detector.** State who the sender pretends to be (bank, wallet, courier, government body) and explain why the message does not match how that organization genuinely communicates.
4. **Safe reply generator.** Either a short safe reply the user could send, or exactly "Do not reply. Block and delete."
5. **Family Share card.** A short, friendly warning in **Roman Urdu** the user can forward to relatives, with a **copy button**.
6. **"How this scam works."** Three short steps: Hook, Pressure, Payment/Data theft.
7. **Report pack.** A ready-to-send plain-text summary (sender, message, red flags, extracted links/numbers) the user can send to their bank or the authorities, with a **copy button**.

### New additions (the differentiators)
8. **"I Already Acted" Recovery Triage.** Four buttons: *I clicked the link*, *I shared my OTP/PIN/password*, *I sent money*, *I installed an app*. Each shows an urgent, ordered damage-control checklist. All four checklists are generated in the same Gemini call (no extra API call), tailored to this specific scam. **This is the main differentiator.**
9. **Pressure Profile.** A bar chart scoring the manipulation tactics used (Urgency, Fear, Authority, Greed, Secrecy), 0-100 each. This teaches users scammer psychology.
10. **Highlighted Message.** Display the original message with suspicious phrases highlighted in color and a short reason for each (shown below the message or on hover/tooltip).
11. **Real vs Fake Twin.** Show what a **genuine** message from the impersonated organization would typically look like (general, non-specific example), next to the scam, so users learn the difference. Include a "what the real org will never ask for" list.
12. **Grandma Mode toggle.** A sidebar switch: simpler wording, larger text, Roman Urdu shown first, and fewer details on screen (verdict, one-line reason, what to do).

## 7. Gemini Response Schema (single call)

Define this with Pydantic and pass it as `response_schema` with `response_mime_type="application/json"`. Do not rely on free-form JSON.

```json
{
  "extracted_text": "string  // full text of the message; for screenshots, the text read from the image",
  "scam_probability": 0,
  "verdict": "Safe | Suspicious | Likely Scam",
  "scam_type": "string  // e.g. Fake bank alert, Wallet impersonation, Prize scam, Job scam, Courier/Customs scam, Government fine scam, Investment scam, Other, None",
  "impersonating": "string  // organization being imitated, or 'None'",
  "impersonation_reason": "string  // why it does not match how the real org communicates",
  "explanation_simple": "string  // 2-3 simple sentences in plain English",
  "explanation_roman_urdu": "string  // same explanation in Roman Urdu",
  "red_flags": ["string"],
  "suspicious_phrases": [
    {"phrase": "exact substring from extracted_text", "reason": "short reason"}
  ],
  "extracted": {
    "urls": [{"url": "string", "issue": "string"}],
    "phone_numbers": ["string"],
    "account_numbers": ["string"]
  },
  "pressure_profile": {
    "urgency": 0,
    "fear": 0,
    "authority": 0,
    "greed": 0,
    "secrecy": 0
  },
  "how_this_scam_works": {
    "hook": "string",
    "pressure": "string",
    "payment": "string"
  },
  "what_to_do": ["string"],
  "safe_reply": "string  // a safe reply, or exactly: Do not reply. Block and delete.",
  "family_warning_roman_urdu": "string  // short, friendly, forwardable warning",
  "real_vs_fake": {
    "genuine_example": "string  // what a genuine message from this org typically looks like (generic, not a real quote)",
    "real_org_never_asks": ["string"]
  },
  "recovery_triage": {
    "clicked_link": ["ordered steps"],
    "shared_otp_or_pin": ["ordered steps"],
    "sent_money": ["ordered steps"],
    "installed_app": ["ordered steps"]
  },
  "report_text": "string  // ready-to-send summary for a bank or authorities",
  "confidence_note": "string  // what the AI is unsure about, if anything"
}
```

**Schema rules**
- `suspicious_phrases[].phrase` MUST be an exact substring of `extracted_text`, so the app can highlight it with simple string matching. If a phrase is not found in the text, skip highlighting it (do not crash).
- All scores are integers 0-100.
- For a **Safe** message, the lists can be short or empty, the recovery triage can be minimal, and the verdict card must be green. Do not invent red flags for genuine messages.

## 8. System Prompt for Gemini (put in `prompts.py`)

```
You are ScamShield, a scam-message analyst for everyday users in Pakistan and South Asia.

You will receive a message (text and/or a screenshot). The message may be in English, Urdu, or Roman Urdu.

Rules:
1. Analyze carefully and return ONLY JSON that matches the provided schema.
2. Be accurate. Do NOT invent facts, links, phone numbers, or organizations. If something is unknown, say so in confidence_note.
3. Do NOT flag genuine messages as scams just because they mention money, a bank, or a link. Genuine bank/wallet messages exist. Consider: unexpected requests for OTP/PIN/password, urgency, threats, prizes, unknown links, lookalike domains, requests for advance fees, and mismatched sender identity.
4. If the message is probably genuine, set verdict to "Safe", keep scam_probability low, and keep red_flags empty or minimal. Still explain why it appears safe, and add a note to verify through the official app or helpline.
5. suspicious_phrases[].phrase must be copied EXACTLY (character for character) from extracted_text.
6. For screenshots, first read all text into extracted_text.
7. Write explanation_simple in very simple English. Write explanation_roman_urdu and family_warning_roman_urdu in natural, friendly Roman Urdu (Urdu written in English letters) that an elderly relative could understand.
8. The recovery_triage checklists must be urgent, practical, ordered, and specific to this scam type. Include steps like: contacting the bank/wallet through its OFFICIAL app or the helpline printed on the back of the card or on the official website (never a number from the message), changing passwords, blocking cards or wallets, and keeping evidence (screenshots, transaction IDs).
9. Never state a specific helpline phone number unless you are certain it is correct. Prefer saying "the official helpline printed on your card or on the official website." You may mention reporting to the national cybercrime authority (FIA Cyber Crime Wing) without a number.
10. real_vs_fake.genuine_example must be a generic illustration of how a genuine message from that type of organization looks (not a real quote), and real_org_never_asks must list things the real organization never asks for (OTP, PIN, full password, advance fees, etc.).
11. Never encourage the user to engage with the scammer, click links, or call numbers in the message.
12. This is AI-assisted guidance, not a guarantee. Reflect uncertainty honestly in confidence_note.
```

## 9. Backend Logic (`analyzer.py`)

- Load env with `python-dotenv`. Read `GEMINI_API_KEY` and `GEMINI_MODEL`.
- Create the client with the `google-genai` SDK: `from google import genai` and `from google.genai import types`.
- Function `analyze(text: str | None, image_bytes: bytes | None, image_mime: str | None) -> ScamReport`:
  - Build `contents` as a list: the user text (if any), and an image `types.Part.from_bytes(data=..., mime_type=...)` (if any).
  - Config: `system_instruction=SYSTEM_PROMPT`, `response_mime_type="application/json"`, `response_schema=ScamReport` (the Pydantic model), low `temperature` (about 0.2) for consistency.
  - Parse the response into the Pydantic model.
- **Error handling:** wrap the call in try/except. On failure, show a friendly message in the UI ("Couldn't analyze. Please try again."). Retry once on a malformed-JSON or transient error. Never show raw stack traces.
- If neither text nor image is provided, show a warning and do not call the API.
- Cache the last result in `st.session_state` so the UI does not re-call Gemini on every button click (important: the Recovery Triage buttons must NOT trigger a new API call).

## 10. UI Layout (`app.py`)

**Page config:** title "ScamShield", shield icon, wide layout.

**Sidebar**
- Logo/title and tagline
- **Grandma Mode** toggle
- "How to use" (3 lines)
- Safety notice: "AI-assisted. Never share your PIN or OTP with anyone. Verify with your bank's official app or helpline."
- GitHub link placeholder

**Main area, top: Input**
- A large text area: "Paste the suspicious message here"
- An image uploader: "...or upload a screenshot"
- A prominent **"Analyze"** button
- 3 small "Try an example" buttons that fill the text box with sample scams from `samples/` (great for live demos)

**Main area, results (after analysis)**
1. **Verdict card** (full width): color-coded green (Safe), yellow (Suspicious), red (Likely Scam). Shows the verdict, `scam_probability` as a progress bar or big number, the scam type, and "Pretending to be: {impersonating}".
2. **Highlighted message** (Feature 10): the original text with `<mark>` highlights on suspicious phrases, and a list of "phrase → reason" underneath. Escape HTML in the user text before injecting markup (use `html.escape`), then apply highlights. Render with `st.markdown(..., unsafe_allow_html=True)`.
3. **Tabs:**
   - **Why it's suspicious:** explanation, red flags, impersonation reason, extracted links/numbers table (URL, issue), and the **Pressure Profile** bar chart (`st.bar_chart`).
   - **How the scam works:** the Hook, Pressure, and Payment steps as three columns or cards, plus the **Real vs Fake Twin** (side by side: "Scam message" vs "What a genuine message looks like", plus the "real org never asks for" list).
   - **What to do:** the `what_to_do` list, the safe reply (with a copy button), and the **"I Already Acted" section** with 4 buttons (Feature 8). Clicking a button reveals that checklist as a numbered, urgent list with a red/orange style. Show a reminder: "Contact your bank through its official app or the helpline on your card, never a number from the message."
   - **Share & Report:** the **Family Warning** (Roman Urdu) with a copy button, and the **Report pack** text in a code/text box with a copy button, plus a "Download as .txt" button.
4. **Confidence note + disclaimer** at the bottom.

**Grandma Mode behavior**
- Larger font (inject small CSS)
- Show only: verdict, one-line explanation (Roman Urdu first, then English), the top 3 "what to do" steps, the Family Warning, and the Recovery Triage buttons
- Hide: pressure chart, extracted tables, and the report pack (keep them in a collapsed "More details" expander)

**Copy button:** use a small HTML/JS snippet via `st.components.v1.html` that calls `navigator.clipboard.writeText(...)`. If that is flaky, fall back to `st.code(text)` which has a built-in copy icon. Prefer the `st.code` fallback if short on time.

## 11. Sample Test Cases (put in `samples/`, test before the demo)

Create these as text files and make sure the app handles each correctly:

1. **Fake bank alert (English):** "Dear customer, your account will be BLOCKED today. Verify now: http://hbl-secure-login.xyz/verify and enter your PIN."
   *Expect:* Likely Scam, impersonating a bank, lookalike domain flagged.
2. **Wallet impersonation (Roman Urdu):** "Aap ka JazzCash account band ho jayega. Abhi apna OTP is number par bhejein warna paisay zaya ho jayenge."
   *Expect:* Likely Scam, OTP request, urgency and fear high.
3. **Prize scam:** "Congratulations! You won Rs. 500,000 in the lucky draw. Send Rs. 2,000 processing fee to claim."
   *Expect:* Likely Scam, advance-fee, greed score high.
4. **Job scam (WhatsApp):** "Earn Rs. 5000 daily from home, no experience needed. Pay Rs. 1500 registration to start."
   *Expect:* Likely Scam, advance-fee job scam.
5. **Courier/customs scam:** "Your parcel is held at customs. Pay Rs. 3,200 clearance at this link to release it."
   *Expect:* Likely Scam or Suspicious, with an unknown link.
6. **Genuine bank notification (false-alarm check):** "Your account ending 1234 was debited Rs. 1,500 at XYZ Store on 12-Nov. If this wasn't you, call the number on the back of your card."
   *Expect:* **Safe.** No invented red flags.
7. **Genuine OTP message (false-alarm check):** "Your verification code is 482913. Do not share this code with anyone."
   *Expect:* **Safe**, with a note that sharing the code with others would be dangerous.
8. **Screenshot test:** upload a screenshot of any scam message and confirm text extraction and highlighting still work.

**Acceptance criteria:** scams 1-5 are flagged; genuine 6-7 are marked Safe; Roman Urdu output reads naturally; highlights do not crash when a phrase is not found; the Recovery Triage buttons work without a new API call.

## 12. Safety, Ethics, and Honesty (must be visible in the app)

- Show the notice: **"AI-assisted analysis. It can be wrong. Never share your PIN or OTP, and always verify through your bank's official app or helpline."**
- The app **analyzes patterns in the message**. It does **not** check live blacklists or verify that a phone number or link is currently malicious. Do not claim otherwise in the UI or README.
- Do not store user messages. Nothing is saved to disk. Mention this in the README.
- Never put the API key in code or commit `.env`.

## 13. README Contents (generate `README.md`)

Include: project name and tagline, the problem, features list, a screenshot placeholder, setup steps (clone, `pip install -r requirements.txt`, copy `.env.example` to `.env`, add the key, `streamlit run app.py`), how it works (one Gemini call with structured output), limitations, the Future Roadmap (Section 15), contributing notes, and the MIT license.

## 14. Build Order (follow this to stay under time)

1. Create the structure, `requirements.txt`, `.env.example`, `.gitignore`, `LICENSE`.
2. `schema.py` and `prompts.py`.
3. `analyzer.py`, then test it from the command line with sample 1 until the JSON parses correctly.
4. `app.py` basic version: input, Analyze button, and verdict card.
5. Add the tabs: Why, How it works, What to do, Share & Report.
6. Add highlighting (Feature 10) and the pressure chart (Feature 9).
7. Add Recovery Triage buttons (Feature 8) and the Real vs Fake Twin (Feature 11).
8. Add Grandma Mode (Feature 12) and the example buttons.
9. Run all 8 test cases, then fix the prompt for any false alarms or misses.
10. Write the README and run a final full run-through.

**If time runs short, cut in this order:** Grandma Mode, then Real vs Fake Twin, then Pressure Profile. **Never cut:** the verdict, the highlighted message, the extracted links, the Roman Urdu Family Warning, and the Recovery Triage.

## 15. Future Roadmap (to mention in the presentation)

Features deliberately left out of the 1-hour build:
- **Session scam history and stats dashboard** (messages checked, scams caught, top scam types)
- **Voice note and call recording analysis** (Gemini accepts audio, so scam calls and voicemails can be analyzed)
- **"Test Yourself" scam-spotting game** to build user awareness
- **Live URL-reputation and phone-number blacklist checks** via threat-intelligence APIs
- **WhatsApp bot and browser extension versions** so users can check messages without leaving the app they are in
- **Community-reported scam database**, so a new scam reported by one user warns everyone
- **More languages** (Sindhi, Pashto, Punjabi) and **text-to-speech** read-aloud for users who cannot read well
- **Bank and wallet integrations** so fintech apps can embed ScamShield directly

## 16. 60-Second Pitch Script

1. **Problem (10s):** "Scam messages look more real every day, and the people most at risk, like parents and first-time digital payment users, have no one to ask."
2. **Live demo (30s):** A judge types any scam text. Show the verdict, the highlighted suspicious phrases, and the flagged fake link. Click **"I shared my OTP"** to show the recovery steps. Then copy the **Roman Urdu family warning**.
3. **Impact (10s):** "Most tools stop at detection. ScamShield explains the scam, protects the family, and helps people recover after the damage."
4. **Open source (10s):** "It is free to fork, so banks, wallets, and fintech apps can embed it. Our roadmap includes voice-call analysis, live blacklist checks, and a WhatsApp bot."

## 17. Definition of Done

- [ ] App runs with `streamlit run app.py` and the API key from `.env`
- [ ] All 8 test cases behave as described in Section 11
- [ ] All 12 features are visible and working (or the cut features are listed in the README as roadmap)
- [ ] No raw errors are shown to the user
- [ ] README, MIT license, and `.env.example` are present, and `.env` is git-ignored
- [ ] Pushed to a public GitHub repo
- [ ] Demo rehearsed twice with a messy, real-looking scam message
