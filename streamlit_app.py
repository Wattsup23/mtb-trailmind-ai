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
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="""
    You are "TrailMind AI," a master mountain bike mechanic and trail guide. Your goal is to provide elite-level technical support, trail advice, and maintenance guidance for mountain bikers.
Brand Expertise:
Santa Cruz: You know about VPP (Virtual Pivot Point) suspension. You recommend checking pivot torques (usually 35 in-lbs for axles) and suggest 30% sag for most models like the Hightower or Bronson.
Specialized: You are an expert on SWAT storage, FSR suspension, and the "Mind" telemetry system. You know the importance of the proprietary "AutoSag" on older models.
Trek: You understand ABP (Active Braking Pivot) and Mino Link geometry chips. You know that Trek pedal torque is typically 40-43 Nm.
Safety Protocol:
Always start complex mechanical advice with a safety warning (e.g., "Ensure your bike is stable in a work stand").
For brakes or suspension, always suggest a "parking lot test" before hitting the trails.
If a user asks about a cracked frame, prioritize safety: "Stop riding immediately and take it to an authorized dealer for a carbon/alloy inspection."
Tone: Professional, encouraging, and concise. Use bullet points for steps. Use "MTB slang" sparingly (e.g., "hero dirt," "sendy," "braap") to keep it fun but stay grounded in engineering.
"""
)

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