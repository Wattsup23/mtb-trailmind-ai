import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Access the secret key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Key not found in Streamlit Secrets!")
    st.stop()

st.set_page_config(page_title="TrailMind AI", page_icon="🚲")
st.title("🚲 TrailMind AI: Brain & Eyes")

# 2. Setup the Expert Model
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are 'TrailMind AI,' a master MTB mechanic. You identify parts from photos and give technical maintenance advice."
)

# 3. Sidebar for Image Uploads (The Eyes)
st.sidebar.header("Identify a Part")
uploaded_file = st.sidebar.file_uploader("Upload a photo of your bike part", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.sidebar.image(img, caption="Part to analyze", use_container_width=True)
    if st.sidebar.button("Analyze Photo"):
        with st.spinner("Analyzing your gear..."):
            # Sends image + text prompt to the AI
            response = model.generate_content(["Identify this MTB part and tell me common maintenance or torque specs for it.", img])
            st.write("### AI Analysis of your Photo:")
            st.write(response.text)
            st.divider()

# 4. Chat Interface (The Brain)
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