import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import tempfile, os, base64, io

st.set_page_config(page_title="LexiTech 2.0 | Legal & Tax Document Assistant", page_icon="LEXItech.PNG", layout="wide")
st.markdown("""
<style>
.lexi-float-btn {
    position: fixed;
    bottom: 64px;
    right: 20px;
    z-index: 99999;
    background: linear-gradient(135deg, #24101C 0%, #881652 100%);
    color: #FFFFFF !important;
    border: 1.5px solid #FF2A85;
    border-radius: 999px;
    padding: 6px 18px 6px 8px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 13.5px;
    text-decoration: none !important;
    box-shadow: 0 6px 24px rgba(184, 29, 111, 0.45);
    display: inline-flex;
    align-items: center;
    gap: 10px;
}
.lexi-float-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(255, 42, 133, 0.75);
}
.lexi-float-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    object-fit: cover;
    object-position: center 28%;
    border: 1.5px solid #F9A8D4;
    background: #12050D;
}
</style>
<a class="lexi-float-btn" href="https://heidiseckman.github.io/LEXI/" target="_blank" rel="noopener">
    <img class="lexi-float-avatar" src="https://heidiseckman.github.io/LEXI/" alt="LEXI" />
    <span>Ask LEXI</span>
</a>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://googleapis.com');
html, body, .stApp, p, label, h1, h2, h3, h4, li { font-family: 'Plus Jakarta Sans', sans-serif !important; color: #1A161F !important; }
.stApp { background-color: #FFFFFF; background-image: radial-gradient(#E8C5D6 0.75px, transparent 0.75px); background-size: 22px 22px; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #FDF2F7 0%, #F9E6F0 100%); border-right: 1px solid #E5B8CE; }
.mono-tag { font-family: 'JetBrains Mono', monospace !important; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 0.08em; color: #B81D6F !important; text-transform: uppercase; }
.nav-bar { background: rgba(255, 255, 255, 0.94); backdrop-filter: blur(10px); border: 1.5px solid #E5B8CE; border-radius: 14px; padding: 14px 22px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 20px rgba(184, 29, 111, 0.07); }
.status-pill { background: #FDF2F7; border: 1px solid #B81D6F; border-radius: 999px; padding: 6px 14px; font-family: 'JetBrains Mono', monospace !important; font-size: 11px !important; font-weight: 700 !important; color: #B81D6F !important; }
.hero-box { background: linear-gradient(135deg, #24101C 0%, #4A1533 55%, #881652 100%); border-radius: 16px; padding: 24px 28px; margin-bottom: 20px; box-shadow: 0 10px 28px rgba(184, 29, 111, 0.16); }
.hero-box h1, .hero-box p, .hero-box span { color: #FFFFFF !important; }
.corpus-card { background: #FFFFFF; border: 1.5px solid #E5B8CE; border-top: 4px solid #B81D6F; border-radius: 14px; padding: 16px 20px; margin-bottom: 10px; box-shadow: 0 4px 14px rgba(184, 29, 111, 0.05); }
.lexitech-banner { background-color: #FDF2F7; border-left: 6px solid #B81D6F; padding: 14px 18px; border-radius: 10px; font-weight: 700; margin: 14px 0; }
.stSelectbox div[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input, [data-testid="stFileUploaderDropzone"] { background-color: #FDF2F7 !important; color: #1A161F !important; border: 1.5px solid #E5B8CE !important; border-radius: 10px !important; }
[data-testid="stAlert"], [data-testid="stAlertContainer"], .stSpinner > div { background-color: #FDF2F7 !important; color: #1A161F !important; border: 1.5px solid #B81D6F !important; border-radius: 10px !important; }
button, .stButton > button, .stDownloadButton > button, [data-testid="stFileUploaderDropzone"] button, [data-testid="stTextInput"] button { background: linear-gradient(135deg, #B81D6F 0%, #8E1454 100%) !important; color: #FFFFFF !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; box-shadow: 0 4px 12px rgba(184, 29, 111, 0.22) !important; }
button *, .stButton > button *, .stDownloadButton > button *, [data-testid="stFileUploaderDropzone"] button *, [data-testid="stTextInput"] button * { color: #FFFFFF !important; }
[data-testid="stTextInput"] button svg { fill: #FFFFFF !important; }
.lexitech-footer { background: #FDF2F7; border: 1px solid #E5B8CE; border-radius: 12px; padding: 14px 18px; text-align: center; font-size: 12.5px; margin-top: 28px; }
</style>
""", unsafe_allow_html=True)

logo_b64 = ""
if os.path.exists("LEXItech.PNG"):
    im = Image.open("LEXItech.PNG").convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    logo_b64 = base64.b64encode(buf.getvalue()).decode()

LOGO_SVG = f"""
<div style="display:flex;align-items:center;gap:16px;">
  <div style="background:linear-gradient(135deg,#FDF2F7 0%,#FFFFFF 100%);border:2px solid #E5B8CE;border-radius:18px;padding:8px;box-shadow:0 6px 18px rgba(184,29,111,0.16);display:flex;align-items:center;justify-content:center;">
    <img src="data:image/png;base64,{logo_b64}" style="width:86px;height:86px;object-fit:contain;image-rendering:high-quality;" />
  </div>
  <div>
    <div style="font-weight:800;font-size:26px;letter-spacing:-0.02em;line-height:1.1;">LEXI<span style="color:#B81D6F;">TECH</span></div>
    <div class="mono-tag" style="font-size:12px !important;margin-top:3px;">LEGAL &amp; TAX AI STUDIO</div>
  </div>
</div>
"""

with st.sidebar:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="mono-tag">01 // AUTHENTICATION</div>', unsafe_allow_html=True)
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste AI Studio Key...")
    st.markdown("---")
    st.markdown('<div class="mono-tag">02 // GROUNDING PROTOCOL</div>', unsafe_allow_html=True)
    st.caption("Strict closed-book retrieval with mandatory section, tab, and page citations.")
    st.markdown("---")
    st.caption("Architected by **Heidi Seckman**")
st.markdown(f"""
<div class="nav-bar">
  {LOGO_SVG}
  <div class="status-pill">● ENGINE v2.0 // CLOSED-BOOK CITATION AUDITOR</div>
</div>
<div class="hero-box">
  <span style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.1em;opacity:0.85;">SINGLE-CORPUS LEGAL &amp; TAX INTELLIGENCE</span>
  <h1 style="margin:4px 0 8px 0;font-size:30px;">Legal &amp; Tax Document AI Assistant</h1>
  <p style="margin:0;font-size:15px;opacity:0.92;">Upload any contract, lease, or official IRS publication to extract high-risk clauses, verify federal tax rules, and export cited research memos in seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="corpus-card"><div class="mono-tag">STEP 01 // SELECT MODE &amp; SOURCE CORPUS</div><h4 style="margin:4px 0;">Document Ingestion &amp; Audit Parameters</h4><p style="margin:0;font-size:13.5px;">Supports contracts, commercial leases, court filings, and multi-megabyte IRS manuals (Pub 4012, Pub 4491, Pub 17).</p></div>', unsafe_allow_html=True)

c1, c2 = st.columns((1, 1))
with c1:
    mode = st.selectbox("Analysis Mode:", (
        "Contract Risk & Red Flag Scanner",
        "IRS / Tax Guide Citation Lookup"
    ))
with c2:
    uploaded_pdf = st.file_uploader("Upload Source Document (PDF)", type="pdf")

user_question = st.text_area(
    "Research Query or Audit Prompt:",
    value="Scan this document for high-risk clauses, missing protections, or key rules, and cite exact section, tab, and page numbers."
)

if st.button("⚡ Execute Document Audit"):
    if not api_key or not uploaded_pdf:
        st.warning("Paste your Gemini API Key in the left sidebar and upload a PDF document first.")
    else:
        with st.spinner("Scanning document and verifying exact page citations..."):
            try:
                client = genai.Client(api_key=api_key)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_pdf.read())
                    tmp_path = tmp.name

                gemini_file = client.files.upload(file=tmp_path)
                os.remove(tmp_path)

                instruction = (
                    "You are LexiTech 2.0, a meticulous legal and tax research auditor. Answer ONLY using facts "
                    "from the attached PDF. Cite exact section, tab, and page numbers for every point. "
                    "If something is not in the document, state 'Not found in the attached document.'"
                )

                models = tuple(m.name.replace("models/", "") for m in client.models.list() if "gemini" in m.name and "flash" in m.name)
                if not models:
                    models = tuple(m.name.replace("models/", "") for m in client.models.list() if "gemini" in m.name)

                success = False
                for model_name in models:
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=[gemini_file, f"Mode: {mode}\n\nRequest: {user_question}"],
                            config=types.GenerateContentConfig(system_instruction=instruction)
                        )
                        st.session_state["last_report"] = response.text
                        st.session_state["last_model"] = model_name
                        st.session_state["last_file"] = uploaded_pdf.name
                        success = True
                        break
                    except Exception:
                        continue

                if not success:
                    st.warning("Google's free servers are experiencing a brief traffic spike. Wait 15 seconds and click Execute Document Audit again!")
            except Exception as e:
                st.error(f"Error: {e}")

if "last_report" in st.session_state:
    st.markdown(f"<div class='lexitech-banner'>✨ Audit Complete! • Powered by LexiTech 2.0 ({st.session_state['last_model']})</div>", unsafe_allow_html=True)
    st.markdown(st.session_state["last_report"])
    st.download_button(
        label="📥 Export Cited Audit Report (.txt)",
        data=st.session_state["last_report"],
        file_name=f"LexiTech2_Audit_{st.session_state['last_file']}.txt",
        mime="text/plain"
    )

st.markdown('<div class="lexitech-footer"><strong>© 2026 LexiTech by Heidi Seckman. All Rights Reserved.</strong><br>Proprietary software, interface design, and branding—unauthorized copying, cloning, or commercial redistribution is prohibited. For educational and research assistance only; not legal or tax advice.</div>', unsafe_allow_html=True)
