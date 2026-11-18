# ⚖️ Legal & Tax Document AI Assistant

A grounded AI research and document analysis web application built with **Python**, **Streamlit**, and the **Google GenAI SDK**. Designed to parse dense legal contracts and official IRS tax reference manuals with strict source citations and zero hallucinations.

🔗 **Live Demo:** [Launch the Web App](https://streamlit.app)

---

## 🎯 Why I Built This
Standard AI chatbots frequently guess or invent rules ("hallucinate") when reading complex legal agreements or tax regulations. I built this tool to enforce **closed-book grounding**—forcing the model to answer *only* from the uploaded PDF and cite exact lesson, section, and page numbers for every claim.

## ✨ Key Features
* **Dual Analysis Modes:**
  * **Contract Risk & Red Flag Scanner:** Identifies high-risk clauses, missing protections, and key obligations in leases, NDAs, and agreements.
  * **IRS / Tax Guide Citation Lookup:** Navigates multi-hundred-page IRS VITA/TCE training manuals (verified on **IRS Pub 6744** and **IRS Pub 4491**) to extract exact rules and page citations.
* **Zero-Hallucination System Prompting:** Strict instruction guardrails prevent outside guessing and require explicit `"Not found in the attached document"` fallbacks.
* **Dynamic Model Failover:** Automatically queries active Gemini Flash models on the user's API key and handles temporary server traffic spikes gracefully.
* **One-Click Report Export:** Generates downloadable `.txt` study and audit memos (`📥 Download Study / Audit Report`) for offline review.
* **Privacy-First Architecture:** Uses a secure sidebar password input so users supply their own Gemini API key per session—zero credentials are ever stored in the repository.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Frontend & Cloud Hosting:** Streamlit & Streamlit Community Cloud
* **AI & Document Parsing:** Google GenAI SDK (`google-genai`), Gemini File API (`client.files.upload`)

## 🚀 How to Use
1. Open the [Live Web App](https://streamlit.app).
2. Paste a free [Google AI Studio](https://google.com) API key into the left sidebar.
3. Select an analysis mode, upload any PDF (contract, lease, or IRS publication), and click **Run AI Analysis**.
4. Review the cited breakdown on screen or click **Download Study / Audit Report** to save a local copy.

---
*Disclaimer: Built for educational, study, and professional research assistance only. Does not constitute legal or tax advice.*
