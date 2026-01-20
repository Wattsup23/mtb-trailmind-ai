import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Missing API Key!")
    st.stop()

st.set_page_config(page_title="TrailMind AI", page_icon="🚲")
st.title("🚲 TrailMind AI: Expert Mode")

# 2. Setup the "Master Mechanic" with Gemini 2.5
# We use specific instructions to force accuracy.
model = genai.GenerativeModel(
    model_name='models/gemini-2.5-flash',
    system_instruction="""You are a Master Mountain Bike Mechanic. 
    When identifying parts:
    - State the Brand and Model clearly.
    - Check for specific mechanical issues (wear, alignment, dirt).
    - Provide exact torque specs in Nm.
    - If you aren't 100% sure of the model, list the 2 most likely options."""
)

# 3. Sidebar Diagnostic
st.sidebar.header("📸 Diagnostic Center")
uploaded_file = st.sidebar.file_uploader("Upload a photo of a bike part", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    # Fixed the 'use_container_width' warning here:
    st.sidebar.image(img, caption="Part to inspect", width="stretch") 
    
    if st.sidebar.button("Analyze Gear"):
        with st.chat_message("assistant"):
            with st.spinner("Analyzing high-res details..."):
                # We ask the model to look specifically for logos and teeth wear
                response = model.generate_content([
                    "Identify this MTB part. Look at the logos and text on the part. "
                    "Tell me the brand, model, and if you see any signs of wear or damage.", 
                    img
                ])
                st.markdown(response.text)
                st.divider()

# 4. Chat Interface
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