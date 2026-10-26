import streamlit as st
from groq import Groq

st.title("⚡ My Fast Cloud AI Assistant")
st.caption("Running 100% free via Groq Cloud — Perfect for Chromebooks!")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

@st.cache_resource
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)

client = get_groq_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Type your message here..."):
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("assistant"):
        with st.spinner("Groq AI is typing..."):
            try:
                response = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": "You are a helpful website chatbot assistant."},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=256,
                    temperature=0.7
                )
                ai_text = response.choices[0].message.content
            except Exception as e:
                ai_text = f"Groq Connection Alert: {e}"
                
        st.markdown(ai_text)
    st.session_state.messages.append({"role": "assistant", "content": ai_text})
