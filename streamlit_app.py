import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Secure API Connection
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Missing API Key! Add it to Streamlit Secrets.")
    st.stop()

st.set_page_config(page_title="TrailMind AI", page_icon="🚲", layout="wide")
st.title("🚲 TrailMind AI: Brain & Eyes")

# 2. Expert Personality Setup
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are 'TrailMind AI,' a master mountain bike mechanic. You help riders identify parts, check for wear, and provide torque specs."
)

# 3. Sidebar: The Diagnostic Center
st.sidebar.header("📸 Diagnostic Center")
uploaded_file = st.sidebar.file_uploader("Upload a photo of a bike part", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.sidebar.image(img, caption="Analyzing this part...", use_container_width=True)
    
    if st.sidebar.button("Analyze Gear"):
        with st.chat_message("assistant"):
            with st.spinner("Inspecting your bike..."):
                # This version ensures the image is formatted correctly for the AI
                response = model.generate_content(
                    contents=["Identify this MTB part and give tech advice.", img]
                )
                st.markdown(response.text)

# 4. Standard Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a tech question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})