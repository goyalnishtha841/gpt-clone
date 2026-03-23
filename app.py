import streamlit as st
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
personas = {
    "Helpful": "You are a helpful assistant. Answer clearly.",
    "Teacher": "You are a patient teacher. Explain simply with examples.",
    "Motivator": "You are an energetic motivator. Use encouraging language.",
    "Sarcastic": "You are sarcastic but still helpful. Keep replies short.",
    "Coder": "You are a coding expert. Always show code examples."
}

persona = st.sidebar.selectbox("Choose personality", list(personas.keys()))

temperature = st.sidebar.slider(
    "Creativity (temperature)", 
    min_value=0.0, max_value=1.0, 
    value=0.7, step=0.1
)

max_tokens = st.sidebar.slider(
    "Max reply length (tokens)", 
    min_value=50, max_value=1000, 
    value=300, step=50
)
# this stores your full conversation history
if "messages" not in st.session_state or st.session_state.get("persona") != persona:
    st.session_state.messages = [
        {"role": "system", "content": personas[persona]}
    ]
    st.session_state.persona = persona
    
st.sidebar.divider()

msg_count = len(st.session_state.messages) - 1
st.sidebar.metric("Messages sent", msg_count)

tokens_used = sum(len(m["content"].split()) * 1.3 
                  for m in st.session_state.messages)
st.sidebar.metric("~Tokens used", int(tokens_used))

if st.sidebar.button("Clear chat"):
    st.session_state.messages = [
        {"role": "system", "content": personas[persona]}
    ]
    st.rerun()
st.title("ChatGPT Clone")
st.caption("Built with OpenAI + Streamlit")

# display all previous messages on screen
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# user types a message
if prompt := st.chat_input("Ask me anything..."):

    # show user message on screen
    with st.chat_message("user"):
        st.markdown(prompt)

    # add to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # call OpenAI API with full history
    response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=max_tokens,
    system=st.session_state.messages[0]["content"],
    messages=st.session_state.messages[1:]
)
    reply = response.content[0].text

    # show assistant reply on screen
    with st.chat_message("assistant"):
        st.markdown(reply)

    # add reply to history
    st.session_state.messages.append({"role": "assistant", "content": reply})