import streamlit as st

# Setup the App Identity
st.set_page_config(page_title="TrailMind AI", page_icon="🚲")

st.title("🚲 TrailMind AI: Phase 1")
st.subheader("Your AI Mountain Bike Specialist")

# Initializing the Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handling User Input
if prompt := st.chat_input("Ask about bike maintenance or local trails..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # This is where we will later connect the high-level AI logic
        response = f"I'm currently in Phase 1 setup. You asked about: '{prompt}'. Soon, I'll be able to pull specific torque specs and trail conditions for you!"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})