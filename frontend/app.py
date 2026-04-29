import streamlit as st
import requests
import time

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="MediReference AI | Clinical Edition",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Safe, Minimal CSS (No hiding structural headers!)
st.markdown("""
<style>
    /* Safe clinical background color */
    .stApp {
        background-color: #f4f7f6;
    }
    /* Style the chat input box safely */
    .stChatInputContainer {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* Custom divider */
    hr {
        border-top: 2px solid #e0e6ed;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar - Enterprise Control Center
with st.sidebar:
    st.title("⚕️ MediReference AI")
    st.caption("v2.0 - Local RAG Architecture")
    st.markdown("---")
    
    st.markdown("### 🎛️ System Diagnostics")
    st.success("🟢 **Model:** Llama 3.2 (Active)")
    st.success("🟢 **Vector DB:** Chroma (Connected)")
    st.success("🟢 **Network:** Air-Gapped (Secure)")
    
    st.markdown("---")
    st.markdown("### 📚 Loaded Modules")
    st.info("• WHO Pediatrics\n• ADA Endocrinology\n• General Cardiology")
    
    st.markdown("---")
    if st.button("🔄 Reset Clinical Session", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    # Professional Footer
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
        "Lead Engineer: Ch Sri Santosh Karthikeya<br>"
        "SRM University AP</div>", 
        unsafe_allow_html=True
    )

# 4. Main Dashboard Header
col1, col2 = st.columns([4, 1])
with col1:
    st.header("⚕️ Clinical Guideline Assistant")
    st.markdown("**Secure, Local Medical Retrieval.** Ask evidence-based questions below.")
with col2:
    st.button("Status: Online", disabled=True)
st.markdown("---")

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to the MediReference Clinical Terminal. How can I assist with your patient guidelines today?"}]

# 6. Render Chat History
for message in st.session_state.messages:
    avatar = "⚕️" if message["role"] == "assistant" else "🧑‍⚕️"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 7. User Input & Backend Processing
if prompt := st.chat_input("Enter clinical query (e.g., 'What is the newborn ventilation rate?')..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍⚕️"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚕️"):
        message_placeholder = st.empty()
        
        with st.spinner("Searching local clinical databases..."):
            try:
                response = requests.post("http://127.0.0.1:8000/api/ask", json={"question": prompt})
                
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer found.")
                    st.toast('Data retrieved successfully!', icon='✅')
                else:
                    answer = f"⚠️ **Error:** Backend returned status code {response.status_code}."
            except Exception as e:
                answer = "⚠️ **Connection Error:** Cannot reach the FastAPI backend. Ensure main.py is running."
        
        # Simulated typing effect
        full_response = ""
        for chunk in answer.split():
            full_response += chunk + " "
            time.sleep(0.02)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
