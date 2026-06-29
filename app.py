import streamlit as st
import streamlit.components.v1 as components
import zipfile
import os
import tempfile
from parser import parse_whatsapp_chat, format_for_ai
from summarizer import summarize_chat

# ---- Page Config ----
st.set_page_config(
    page_title="WhatsApp AI Briefing",
    page_icon="💬",
    layout="centered"
)

# ---- Header ----
st.title("💬 WhatsApp AI Briefing")
st.markdown("Upload your WhatsApp chat export and get an instant AI-powered briefing — read out loud.")

st.divider()

# ---- File Upload ----
uploaded_file = st.file_uploader(
    "📁 Upload your WhatsApp chat (.zip or .txt)",
    type=["zip", "txt"]
)

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:

        if uploaded_file.name.endswith(".zip"):
            zip_path = os.path.join(tmpdir, "chat.zip")
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.read())
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(tmpdir)
            txt_file = None
            for fname in os.listdir(tmpdir):
                if fname.endswith(".txt"):
                    txt_file = os.path.join(tmpdir, fname)
                    break
            if not txt_file:
                st.error("❌ No .txt file found inside the ZIP.")
                st.stop()
        else:
            txt_file = os.path.join(tmpdir, "chat.txt")
            with open(txt_file, "wb") as f:
                f.write(uploaded_file.read())

        messages = parse_whatsapp_chat(txt_file)

        if not messages:
            st.warning("⚠️ No messages found. Check the file format.")
            st.stop()

        st.success(f"✅ Parsed {len(messages)} messages successfully!")

        if st.button("🧠 Generate AI Briefing", use_container_width=True):

            with st.spinner("🤖 AI is reading your chat..."):
                formatted = format_for_ai(messages)
                summary = summarize_chat(formatted)

            # Save summary to session so voice button can use it
            st.session_state["summary"] = summary

# ---- Show summary and voice button OUTSIDE the file block ----
if "summary" in st.session_state:
    summary = st.session_state["summary"]

    st.divider()
    st.subheader("📋 Your Daily Briefing")
    st.markdown(summary)

    st.divider()

    if st.button("🔊 Read Briefing Out Loud", use_container_width=True):
        # Clean text for JS
        clean_text = summary.replace("'", " ").replace('"', " ").replace("\n", " ").replace("`", " ")

        # Inject JS speech directly
        components.html(f"""
            <script>
                function speak() {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance(`{clean_text}`);
                    msg.rate = 0.9;
                    msg.pitch = 1;
                    msg.volume = 1;
                    window.speechSynthesis.speak(msg);
                }}
                speak();
            </script>
            <p style="color:green; font-family:sans-serif;">🔊 Speaking now...</p>
        """, height=60)