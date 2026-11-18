import streamlit as st
from google import genai
from google.genai import types
import tempfile, os

st.set_page_config(page_title="Legal & Tax Document Assistant", page_icon="⚖️")
st.title("⚖️ Legal & Tax Document AI Assistant")
st.caption("For educational and professional research assistance only. Not legal or tax advice.")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

mode = st.selectbox("Choose Analysis Mode:", [
    "Contract Risk & Red Flag Scanner",
    "IRS / Tax Guide Citation Lookup"
])

uploaded_pdf = st.file_uploader("Upload a PDF Document (Contract, Lease, or IRS Guide)", type=["pdf"])
user_question = st.text_area("What would you like to analyze or check?", 
    value="Scan this document for high-risk clauses, missing protections, or key rules, and cite exact page numbers.")

if st.button("Run AI Analysis") and uploaded_pdf and api_key:
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

            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=[gemini_file, f"Mode: {mode}\n\nRequest: {user_question}"],
                config=types.GenerateContentConfig(system_instruction=instruction)
            )
            st.success("Analysis Complete!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
elif st.button("Test Check"):
    st.warning("Make sure you entered your API key on the left and uploaded a PDF!")
