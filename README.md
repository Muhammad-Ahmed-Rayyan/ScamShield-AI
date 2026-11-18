# 🛡️ ScamShield

**Detect. Explain. Protect your family. Recover.**

ScamShield is an open-source web app that analyzes a suspicious SMS, WhatsApp message, email, or screenshot with the Gemini API. It tells you whether it is a scam, **explains why**, **warns your family in Roman Urdu**, **helps you recover if you already acted**, and **generates a report** for your bank or the authorities.

## The problem

Scam messages (fake bank alerts, JazzCash/Easypaisa impersonation, prize, job and courier/customs scams) look more real every day. The people most at risk (parents, elders, first-time digital payment users) have nobody to ask. Most scam checkers only say "scam / not scam". They don't explain the tactics, help someone who already clicked or paid, warn the family in their own language, or produce an evidence pack.

## Features

1. Multi-channel input: pasted text and/or screenshot (PNG/JPG)
2. Link, phone and account extractor, with per-URL problem flags (lookalike domains, odd TLDs, shorteners)
3. Impersonation detector
4. Safe reply generator
5. Family Share card in Roman Urdu (copy icon)
6. "How this scam works": Hook, Pressure, Payment
7. Report pack (copy icon + .txt download)
8. **"I Already Acted" Recovery Triage** (clicked link / shared OTP / sent money / installed app). Generated in the same Gemini call, so the buttons never trigger a new API call
9. Pressure Profile bar chart (urgency, fear, authority, greed, secrecy)
10. Highlighted message with a reason for each suspicious phrase (hover or list below)
11. Real vs Fake Twin, plus what the real organization never asks for
12. Grandma Mode: bigger text, Roman Urdu first, minimal screen

## Screenshot

_Add a screenshot here (`docs/screenshot.png`)._

## Setup

```bash
git clone <your-repo-url> scamshield
cd scamshield
pip install -r requirements.txt
cp .env.example .env        # Windows: copy .env.example .env
# edit .env and set GEMINI_API_KEY (get one at https://aistudio.google.com/apikey)
streamlit run app.py
```

`GEMINI_MODEL` in `.env` defaults to `gemini-3.8-flash`. Change it to any current Gemini Flash model name listed in Google AI Studio.

## How it works

One Gemini call per analysis. The prompt (`prompts.py`) and a Pydantic schema (`schema.py`) are sent with `response_mime_type="application/json"`, so the model returns structured JSON that the Streamlit UI (`app.py`) renders. The last result is kept in `st.session_state`, so button clicks never re-call the API.

```
app.py          Streamlit UI
analyzer.py     Gemini call, retry once, friendly errors
schema.py       Pydantic response models
prompts.py      System prompt
ui_helpers.py   Highlighting, chart data, styling
samples/        Test messages
```

## Privacy and limitations

- Nothing is stored. No database, no login, nothing written to disk. Messages are sent to the Gemini API for analysis.
- ScamShield **analyzes patterns in the message**. It does **not** check live blacklists or verify that a link or phone number is currently malicious.
- AI-assisted analysis can be wrong. Never share your PIN or OTP, and always verify through your bank's official app or the helpline printed on your card.
- Your API key lives only in `.env`, which is git-ignored.

## Testing

Run each file in `samples/` through the app. Expected: samples 1-5 flagged (Likely Scam / Suspicious), samples 6-7 marked **Safe**. Also test one screenshot upload.

## Future roadmap

- Session scam history and stats dashboard
- Voice note and call recording analysis (Gemini accepts audio)
- "Test Yourself" scam-spotting game
- Live URL-reputation and phone-number blacklist checks via threat-intelligence APIs
- WhatsApp bot and browser extension
- Community-reported scam database
- More languages (Sindhi, Pashto, Punjabi) and text-to-speech read-aloud
- Bank and wallet integrations for fintech apps

## Contributing

Issues and pull requests are welcome. Keep the app dependency-light and never commit `.env`.

## License

MIT. See [LICENSE](LICENSE).
