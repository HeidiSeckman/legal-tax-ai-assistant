import streamlit as st
from google import genai
from google.genai import types
import tempfile, os

st.set_page_config(page_title="LexiTech | Legal & Tax Document Assistant", page_icon="LEXItech.PNG")

# Custom LexiTech Berry & Blush Theme (crisp dark text + soft blush boxes)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1F1F24; }
    [data-testid="stSidebar"] { background-color: #FDF2F7; }
    label, .stMarkdown, p, span { color: #1F1F24 !important; }
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextArea textarea,
    .stTextInput input,
    [data-testid="stFileUploaderDropzone"] {
        background-color: #FDF2F7 !important;
        color: #1F1F24 !important;
        border: 1px solid #E8C5D6 !important;
    }
    .stButton > button {
        background-color: #B81D6F !important;
        color: #FFFFFF !important;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover { background-color: #961559 !important; }
    .stButton > button p, .stButton > button span { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
    st.image("LEXItech.PNG", width=115)
with col2:
    st.title("Legal & Tax Document AI Assistant")
    st.caption("Powered by LexiTech • For educational and professional research assistance only.")

st.sidebar.image("LEXItech.PNG", width=130)
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

mode = st.selectbox("Choose Analysis Mode:", [
    "Contract Risk & Red Flag Scanner",
    "IRS / Tax Guide Citation Lookup"
])

uploaded_pdf = st.file_uploader("Upload a PDF Document (Contract, Lease, or IRS Guide)", type=["pdf"])
user_question = st.text_area("What would you like to analyze or check?", 
    value="Scan this document for high-risk clauses, missing protections, or key rules, and cite exact page numbers.")

if st.button("Run AI Analysis"):
    if not api_key or not uploaded_pdf:
        st.warning("Make sure you entered your API key on the left and uploaded a PDF!")
    else:
        with st.spinner("Reading document and checking rules..."):
            try:
                client = genai.Client(api_key=api_key)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_pdf.read())
                    tmp_path = tmp.name

                gemini_file = client.files.upload(file=tmp_path)
                os.remove(tmp_path)

                instruction = (
                    "You are a meticulous legal and tax research assistant. Answer ONLY using facts "
                    "from the attached PDF. Cite exact section and page numbers for every point. "
                    "If something is not in the document, state 'Not found in the attached document.'"
                )

                models = [m.name.replace("models/", "") for m in client.models.list() if "gemini" in m.name and "flash" in m.name]
                if not models:
                    models = [m.name.replace("models/", "") for m in client.models.list() if "gemini" in m.name]

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
                    st.warning("Google's free servers are experiencing a brief traffic spike. Wait 15 seconds and click Run AI Analysis again!")
            except Exception as e:
                st.error(f"Error: {e}")

if "last_report" in st.session_state:
    st.success(f"Analysis Complete! (Powered by {st.session_state['last_model']})")
    st.markdown(st.session_state["last_report"])
    st.download_button(
        label="📥 Download Study / Audit Report",
        data=st.session_state["last_report"],
        file_name=f"AI_Audit_{st.session_state['last_file']}.txt",
        mime="text/plain"
    )uploaded_pdf = st.file_uploader("Upload a PDF Document (Contract, Lease, or IRS Guide)", type=["pdf"])
user_question = st.text_area("What would you like to analyze or check?", 
    value="Scan this document for high-risk clauses, missing protections, or key rules, and cite exact page numbers.")

if st.button("Run AI Analysis"):
    if not api_key or not uploaded_pdf:
        st.warning("Make sure you entered your API key on the left and uploaded a PDF!")
    else:
        with st.spinner("Reading document and checking rules..."):
            try:
                client = genai.Client(api_key=api_key)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_pdf.read())
                    tmp_path = tmp.name

                gemini_file = client.files.upload(file=tmp_path)
                os.remove(tmp_path)

                instruction = (
                    "You are a meticulous legal and tax research assistant. Answer ONLY using facts "
                    "from the attached PDF. Cite exact section and page numbers for every point. "
                    "If something is not in the document, state 'Not found in the attached document.'"
                )

                models = [m.name.replace("models/", "") for m in client.models.list() if "gemini" in m.name and "flash" in m.name]
                if not models:
                    models = [m.name.replace("models/", "") for m in client.models.list() if "gemini" in m.name]

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
                    st.warning("Google's free servers are experiencing a brief traffic spike. Wait 15 seconds and click Run AI Analysis again!")
            except Exception as e:
                st.error(f"Error: {e}")

if "last_report" in st.session_state:
    st.success(f"Analysis Complete! (Powered by {st.session_state['last_model']})")
    st.markdown(st.session_state["last_report"])
    st.download_button(
        label="📥 Download Study / Audit Report",
        data=st.session_state["last_report"],
        file_name=f"AI_Audit_{st.session_state['last_file']}.txt",
        mime="text/plain"
    )
