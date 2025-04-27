import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model="llama3-70b-8192",
    temperature=1.5
)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history=[SystemMessage(content="You are a helpful AI assistant")]

st.set_page_config(page_title="Saranyu's Chatbot 🤖", page_icon="🤖", layout="wide")
st.title("Saranyu's Chatbot ")

chat_placeholder=st.container()

user_input=st.text_input("You:", key="user_input", placeholder="Type your message here...")
send_button=st.button("Send")

if send_button and user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    if user_input.lower()=='close the chat':
        st.stop()
    res=model.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(AIMessage(content=res.content))
    st.session_state.scroll=True
    st.rerun()

with chat_placeholder:
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            st.markdown(f"<div style='text-align: right; color: white; background-color: #0a84ff; padding: 8px; border-radius: 10px; margin: 5px 0;'>{message.content}</div>", unsafe_allow_html=True)
        elif isinstance(message, AIMessage):
            st.markdown(f"<div style='text-align: left; background-color: #e5e5ea; padding: 8px; border-radius: 10px; margin: 5px 0;'>{message.content}</div>", unsafe_allow_html=True)

if 'scroll' in st.session_state and st.session_state.scroll:
    st.session_state.scroll=False
    st.markdown(
        """
        <script>
            window.scrollTo(0,document.body.scrollHeight);
        </script>
        """,
        unsafe_allow_html=True
    )
