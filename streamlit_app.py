import streamlit as st
import google.generativeai as genai

# 1. Access the secret key we just saved
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Key not found. Please add it to Streamlit Secrets!")
    st.stop()

st.set_page_config(page_title="TrailMind AI", page_icon="🚲")
st.title("🚲 TrailMind AI: The Brain")

# 2. Set the "MTB Expert" Personality
model = genai.GenerativeModel('gemini-1.5-flash', 
                              system_instruction="You are TrailMind, an expert mountain bike mechanic and trail guide. You provide technical, safe, and encouraging advice.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a tech question (e.g., 'How do I bleed Shimano brakes?')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 3. Get the real AI response
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})