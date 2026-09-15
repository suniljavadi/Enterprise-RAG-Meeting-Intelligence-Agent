import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")
st.set_page_config(page_title="RAG Intelligence", page_icon="◈", layout="wide")
st.markdown("""<style>body{background:#f4f1ea}.block-container{max-width:1250px;padding-top:2rem}.hero{padding:1.5rem 0;border-bottom:1px solid #d8d1c4;margin-bottom:1rem}.hero h1{font-family:Georgia,serif;color:#173b3f;font-size:3rem;margin:0}.hero p{color:#67706e;font-size:1.05rem}.stButton>button{background:#173b3f;color:white;border:0;border-radius:3px}</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>RAG Intelligence</h1><p>Grounded answers across operational documents and meeting decisions.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.caption("ENTERPRISE KNOWLEDGE WORKSPACE")
    page = st.radio("Workspace", ["Ask the knowledge base", "Documents", "Meetings", "Action items"])
    st.divider()
    st.caption("Local fallback mode is active when no LLM key is configured.")

if page == "Ask the knowledge base":
    st.subheader("Ask a grounded question")
    question = st.text_area("Question", placeholder="What was decided about the deployment process?", height=100)
    if st.button("Search and answer", type="primary") and question:
        with st.spinner("Retrieving evidence..."):
            response = requests.post(f"{API_URL}/api/v1/query", json={"question": question}, timeout=60)
        if response.ok:
            result = response.json()
            st.markdown("### Answer")
            st.write(result["answer"])
            st.metric("Confidence", f'{result.get("confidence", 0):.0%}')
            st.markdown("### Citations")
            for citation in result.get("citations", []):
                st.info(f'{citation["document"]} · page {citation["page"]} · {citation["section"]} · `{citation["chunk_id"][:8]}`')
            with st.expander("Retrieved chunks"):
                for item in result.get("evidence", []):
                    st.write(item["text"])
        else:
            st.error(response.text)
elif page == "Documents":
    st.subheader("Document explorer")
    upload = st.file_uploader("Upload PDF, DOCX, TXT, Markdown, or CSV")
    if upload and st.button("Index document"):
        response = requests.post(f"{API_URL}/api/v1/documents/upload", data=upload.getvalue(), headers={"X-Filename": upload.name}, timeout=60)
        st.success(response.json() if response.ok else response.text)
elif page == "Meetings":
    st.subheader("Meeting intelligence")
    response = requests.get(f"{API_URL}/api/v1/meetings", timeout=20)
    for meeting in response.json() if response.ok else []:
        with st.expander(meeting["title"]):
            st.write(meeting["summary"])
            st.write("Decisions:", meeting["decisions"])
            st.write("Risks:", meeting["risks"])
elif page == "Action items":
    st.subheader("Action-item dashboard")
    response = requests.get(f"{API_URL}/api/v1/action-items", timeout=20)
    st.dataframe(response.json() if response.ok else [], use_container_width=True)
