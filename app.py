import streamlit as st
from openai import OpenAI
import os


provider = os.getenv("PROVIDER", "openai").lower()

# ตั้งค่าผู้ให้บริการ
if provider == "openrouter":
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    model_name = "gpt-3.5-turbo"
else:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = "https://api.openai.com/v1"
    model_name = "gpt-3.5-turbo"

client = OpenAI(api_key=api_key, base_url=base_url)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Engineer Chatbot", page_icon="🌌", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;600&display=swap');
body {
    font-family: 'Prompt', sans-serif;
    background: radial-gradient(circle at top, #0b132b, #1c2541, #3a506b);
    color: #f0f8ff;
}
h1, h2, h3 {
    text-align: center;
    color: #ffffff;
    font-weight: 600;
    text-shadow: 0 0 8px rgba(173,216,230,0.6);
}
.header {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    backdrop-filter: blur(8px);
    margin-bottom: 25px;
}
.chat-card {
    background: rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    backdrop-filter: blur(6px);
}
.chat-card-user {
    border-left: 4px solid #5bc0be;
}
.chat-card-assistant {
    border-left: 4px solid #9eeaf9;
}
div[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.1);
    color: #ffffff;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.25);
}
.stButton>button {
    background: linear-gradient(90deg, #3a86ff, #4361ee);
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    padding: 8px 18px;
    box-shadow: 0 0 10px rgba(67,97,238,0.4);
    transition: 0.25s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 14px rgba(67,97,238,0.8);
}
.sidebar-content {
    color: #e0f7fa;
    font-size: 15px;
}
.footer {
    text-align: center;
    color: #aad8ff;
    margin-top: 30px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
    <h1>🌌 AI Chatbot for AI Engineer</h1>
    <h4 style="color:#a9d6e5;">พัฒนาโดย นางสาวนิรมล วงษายา (Niramol Wongsaya)</h4>
    <p style="color:#d7e3fc;">Chatbot ผู้ช่วยตอบคำถามด้าน AI, LLM และ Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=90)
    st.markdown("<h3 style='color:#a9def9;'>⚙️ Settings</h3>", unsafe_allow_html=True)
    provider_display = "🟦 OpenAI" if provider == "openai" else "🟣 OpenRouter"
    st.markdown(f"<div class='sidebar-content'><b>Provider:</b> {provider_display}</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div class='sidebar-content'>💡 สามารถรีเซ็ตการสนทนา หรือปรับแต่งค่าการทำงานได้ที่นี่</div>", unsafe_allow_html=True)
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = [
            {"role": "system", "content": "คุณเป็นผู้ช่วย AI ที่ตอบคำถามด้านเทคโนโลยี AI และ Machine Learning ด้วยภาษาง่าย"}
        ]
        st.experimental_rerun()

# ---------------- INITIAL STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "คุณเป็นผู้ช่วย AI ที่ตอบคำถามด้านเทคโนโลยี AI และ Machine Learning ด้วยภาษาง่าย"}
    ]

# ---------------- CHAT HISTORY ----------------
st.subheader("💬 สนทนากับผู้ช่วย AI")
for msg in st.session_state.messages[1:]:
    role_class = "chat-card-user" if msg["role"] == "user" else "chat-card-assistant"
    with st.container():
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-card {role_class}'><b>👩‍💻 คุณ:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-card {role_class}'><b>🤖 ผู้ช่วย AI:</b> {msg['content']}</div>", unsafe_allow_html=True)

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("พิมพ์คำถามของคุณที่นี่...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("🛰️ กำลังประมวลผลคำตอบ..."):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    <hr>
    © 2025 Niramol Wongsaya | Developed with using <b>Streamlit</b><br>
</div>
""", unsafe_allow_html=True)
