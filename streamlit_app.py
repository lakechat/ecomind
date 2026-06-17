"""Streamlit UI for EcoMind chatbot"""

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage, AIMessage
from src.agent.graph import agent

st.set_page_config(
    page_title="EcoMind  🌿",
    page_icon="🌿",
)
st.title(" 🌿 EcoMind - Your Sustainability Cocah")
st.caption("Ask me anything about sustainability!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Chat input
if prompt := st.chat_input("Ask me anything about sustainability!"):
    # Add user message
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = agent.invoke({"messages": st.session_state.messages})
            assistant_message = result["messages"][-1]
            st.markdown(assistant_message.content)

    st.session_state.messages.append(assistant_message)




