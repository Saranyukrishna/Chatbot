import streamlit as st
import ollama
import PyPDF2
from docx import Document

st.title("ActBot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    st.session_state["full_message"] = ""

def display_chat():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
        else:
            st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

def generate_response():
    response = ollama.chat(model='llama2', stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

def handle_user_input(prompt):
    if len(st.session_state["messages"]) > 1:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        st.session_state["full_message"] = ""
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
    st.session_state["messages"].append({"role": "assistant", "content": st.session_state["full_message"]})

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        content = ""
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            content += page.extract_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        content = "\n".join([para.text for para in doc.paragraphs])
    else:
        content = "File type not supported."
    return content

uploaded_file = st.file_uploader("Upload a file (optional)", type=["txt", "pdf", "docx"])

if uploaded_file:
    content = extract_text_from_file(uploaded_file)
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    st.session_state["full_message"] = ""
    st.session_state["messages"].append({"role": "user", "content": content})
    st.chat_message("user", avatar="🧑‍💻").write(content)
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
    st.session_state["messages"].append({"role": "assistant", "content": st.session_state["full_message"]})

if prompt := st.chat_input():
    handle_user_input(prompt)

display_chat()
