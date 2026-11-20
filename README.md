<div align="center">

# 🛡️ ScamShield

*Detect. Explain. Protect your family. Recover.*

![Last Commit](https://img.shields.io/github/last-commit/Muhammad-Ahmed-Rayyan/ScamShield-AI)
![Python](https://img.shields.io/badge/Python-100%25-blue?logo=python)
![languages](https://img.shields.io/github/languages/count/Muhammad-Ahmed-Rayyan/ScamShield-AI)

<br>

Built with the tools and technologies:  
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

</div>

---

## 🧠 Project Summary

**ScamShield** is an open-source web app that analyzes a suspicious SMS, WhatsApp message, email, or screenshot using the **Gemini API**. It tells you whether it is a scam, **explains why**, **warns your family in Roman Urdu**, **helps you recover if you already acted**, and **generates a report** for your bank or the authorities.

Scam messages (fake bank alerts, JazzCash/Easypaisa impersonation, prize, job, and courier/customs scams) look more real every day, and the people most at risk (parents, elders, first-time digital payment users) have nobody to ask. Most scam checkers only say "scam / not scam". ScamShield goes further: it explains the tactics, helps someone who already clicked or paid, warns the family in their own language, and produces an evidence pack.

---

## 🚀 Features

- 📥 **Multi-Channel Input:** Paste text and/or upload a screenshot (PNG/JPG).
- 🔗 **Link, Phone & Account Extractor:** Per-URL problem flags for lookalike domains, odd TLDs, and shorteners.
- 🎭 **Impersonation Detector:** Identifies which bank, wallet, or organization the message pretends to be.
- 💬 **Safe Reply Generator:** A ready-made, safe response you can send back.
- 👨‍👩‍👧 **Family Share Card:** Roman Urdu warning with a one-click copy icon.
- 🪝 **"How This Scam Works":** Breaks the scam into Hook, Pressure, and Payment.
- 📄 **Report Pack:** Copy icon plus `.txt` download for your bank or authorities (e.g. FIA Cyber Crime Wing).
- 🆘 **"I Already Acted" Recovery Triage:** Steps for *clicked link / shared OTP / sent money / installed app*, generated in the same Gemini call so the buttons never trigger a new API request.
- 📊 **Pressure Profile Chart:** Scores urgency, fear, authority, greed, and secrecy.
- 🖍️ **Highlighted Message:** Each suspicious phrase is marked with a reason (hover or list below).
- 🆚 **Real vs Fake Twin:** Shows a genuine example and what a real organization never asks for.
- 👵 **Grandma Mode:** Bigger text, Roman Urdu first, minimal screen.

---

## ⚙️ How It Works

One Gemini call per analysis. The prompt (`prompts.py`) and a Pydantic schema (`schema.py`) are sent with `response_mime_type="application/json"`, so the model returns structured JSON that the Streamlit UI (`app.py`) renders. The last result is kept in `st.session_state`, so button clicks never re-call the API.

---

## 🗃️ Project Structure

```bash
ScamShield-AI
├── samples
│   ├── 1_fake_bank_alert.txt
│   ├── 2_wallet_roman_urdu.txt
│   ├── 3_prize_scam.txt
│   ├── 4_job_scam.txt
│   ├── 5_courier_customs.txt
│   ├── 6_genuine_bank.txt
│   └── 7_genuine_otp.txt
├── app.py                         # Streamlit UI
├── analyzer.py                    # Gemini call, retry once, friendly errors
├── schema.py                      # Pydantic response models
├── prompts.py                     # System prompt
├── ui_helpers.py                  # Highlighting, chart data, styling
├── ScamShield_Project_Spec.md     # Project specification
├── requirements.txt               # Project dependencies
├── .env.example                   # Environment variable template
└── .gitignore
```

---

## 🔧 Setup & Installation

> Make sure Python 3.8+ is installed.

```bash
# Clone the repo
git clone https://github.com/Muhammad-Ahmed-Rayyan/ScamShield-AI.git
cd ScamShield-AI

# (Optional) Create a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install required libraries
pip install -r requirements.txt

# Create your .env file
# On Windows
copy .env.example .env
# On macOS/Linux
cp .env.example .env

# Run the Streamlit app
streamlit run app.py
```

---

## 🔑 API Configuration

To run ScamShield, add your Gemini API key to the `.env` file in the project root:

```.env
GEMINI_API_KEY="YOUR-GEMINI-API-KEY"
GEMINI_MODEL="gemini-3.8-flash"
```

- **Gemini API Key:** Generate one at [Google AI Studio](https://aistudio.google.com/apikey).
- **Gemini Model:** Defaults to `gemini-3.8-flash`. Change it to any current Gemini Flash model name listed in Google AI Studio.

> Your API key lives only in `.env`, which is git-ignored. Never commit it.

---

## 🧪 Testing

Run each file in `samples/` through the app.

- ✅ Samples **1–5** should be flagged (*Likely Scam* / *Suspicious*)
- ✅ Samples **6–7** should be marked **Safe**
- ✅ Also test one screenshot upload

---

## 🔒 Privacy & Limitations

- 🚫 **Nothing is stored:** No database, no login, nothing written to disk. Messages are sent to the Gemini API for analysis only.
- 🔍 **Pattern analysis only:** ScamShield does **not** check live blacklists or verify that a link or phone number is currently malicious.
- ⚠️ **AI can be wrong:** Never share your PIN or OTP, and always verify through your bank's official app or the helpline printed on your card.

---

## 🛣️ Future Roadmap

- 📈 Session scam history and stats dashboard
- 🎙️ Voice note and call recording analysis (Gemini accepts audio)
- 🎮 "Test Yourself" scam-spotting game
- 🛰️ Live URL-reputation and phone-number blacklist checks via threat-intelligence APIs
- 🤖 WhatsApp bot and browser extension
- 👥 Community-reported scam database
- 🌐 More languages (Sindhi, Pashto, Punjabi) and text-to-speech read-aloud
- 🏦 Bank and wallet integrations for fintech apps

---

<div align="center">

⭐ Found this project useful? Give it a star on GitHub!

</div>
