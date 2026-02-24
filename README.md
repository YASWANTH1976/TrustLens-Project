# 🛡️ TrustLens: AI & Blockchain Threat Intelligence
[![Flask](https://img.shields.io/badge/Flask-Backend-green?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Gemini](https://img.shields.io/badge/Gemini_2.5-AI_Engine-orange?style=for-the-badge)](https://deepmind.google/technologies/gemini/)

**TrustLens** is a decentralized, zero-shot threat intelligence platform designed to detect misinformation, clickbait, and malicious claims in real-time. Moving beyond static CSV-trained machine learning models, TrustLens utilizes **Retrieval-Augmented Generation (RAG)** and **Agentic AI** to evaluate claims against live web data, anchoring verified truths to an immutable Blockchain ledger.

---

---

## 🧠 Core Innovations & Upgraded Architecture

* **Zero-Shot Fact-Checking (RAG):** Bypasses the "Temporal Desynchronization" of static datasets. The system dynamically queries the live web via the DuckDuckGo API and `newspaper3k` to calculate a **Factual Entailment Confidence Score** based on real-time evidence.
* **Explainable AI (XAI):** Solves the "Black Box" problem of traditional ML. Gemini 2.5 Flash is prompt-engineered to output strict JSON heuristics, providing users with the exact reasoning and corroborating sources for its verdict.
* **Cryptographic Ledger Audit:** Verified news abstracts are anchored to a custom Python-based SHA-256 Blockchain. The `/lookup` route recalculates block hashes to detect and flag unauthorized post-publication data tampering.
* **Lexical NLP (Early-Warning Radar):** Integrates `TextBlob` to calculate deterministic scores for **Emotional Intensity (Polarity)** and **Subjective Bias (Subjectivity)**, exposing psychological manipulation and clickbait.
* **Real-Time IP Geolocation:** Uses Python `socket` network resolution and `ip-api` to trace the physical server locations of URLs to identify offshore or proxy-hosted threats.

---

## 🏗️ System Pipeline

1. **Input Layer:** User submits a text claim or news URL via the mobile-responsive UI.
2. **Extraction & Context:** Backend resolves the IP, scrapes article text, and fetches live search corroboration.
3. **Reasoning Engine:** Gemini AI processes the multimodal data to determine Factual Entailment.
4. **Ledger Hashing:** If processed, the abstract is sealed into the Blockchain using SHA-256.
5. **Output:** The UI renders the JSON payload, displaying DEFCON threat levels, radar charts, and the Blockchain Hash ID.

---

## ⚙️ Local Installation & Setup

If you wish to run the Neural Engine locally:

```bash
# 1. Clone the repository
git clone [https://github.com/YASWANTH1976/TrustLens-Project.git](https://github.com/YASWANTH1976/TrustLens-Project.git)
cd TrustLens-Project

# 2. Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Gemini API Key
# On Windows Command Prompt:
set GEMINI_API_KEY="your_api_key_here"
# On Linux/Mac or Git Bash:
export GEMINI_API_KEY="your_api_key_here"

# 5. Boot the server using Gunicorn (Production) or Flask (Development)
gunicorn app:app
# OR
python app.py
