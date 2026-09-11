import streamlit as st

from main import run_pipeline
from core.rag_engine import ask_question


# ---------- Page ----------
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎙️",
    layout="wide"
)

# ---------- Style ----------
st.markdown("""
<style>
.stApp { background:#0b0f19; }
.block-container { max-width:1200px; padding-top:2rem; }

.hero {
    padding:25px;
    border-radius:18px;
    margin-bottom:25px;
    background:linear-gradient(135deg,#171d38,#101827);
    border:1px solid #29324a;
}

.hero h1 {
    margin:0;
    font-size:2.3rem;
    background:linear-gradient(90deg,#818cf8,#38bdf8);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero p { color:#9ca3af; }

.card {
    background:#111827;
    border:1px solid #1f2937;
    border-radius:14px;
    padding:20px;
    margin-bottom:15px;
}

.title {
    color:#9ca3af;
    font-size:.8rem;
    text-transform:uppercase;
    letter-spacing:.06em;
}

.metric {
    background:#111827;
    border:1px solid #1f2937;
    border-radius:12px;
    padding:15px;
    text-align:center;
}

.metric b {
    display:block;
    font-size:1.5rem;
    color:#818cf8;
}

.metric span { color:#9ca3af; font-size:.8rem; }
</style>
""", unsafe_allow_html=True)


# ---------- Session ----------
if "result" not in st.session_state:
    st.session_state.result = None

if "chat" not in st.session_state:
    st.session_state.chat = []


# ---------- Sidebar ----------
with st.sidebar:
    st.title("🎙️ AI Video Assistant")
    st.caption("Turn videos into structured knowledge.")

    source = st.text_input(
        "YouTube URL / File Path",
        placeholder="https://youtube.com/..."
    )

    language = st.selectbox(
        "Language",
        ["english", "hinglish"]
    )

    process = st.button(
        "🚀 Process Video",
        use_container_width=True,
        type="primary"
    )

    if st.session_state.result:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.result = None
            st.session_state.chat = []
            st.rerun()


# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>🎙️ AI Video Assistant</h1>
    <p>
        Summarize videos, extract decisions and action items,
        and chat with your content.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------- Run Pipeline ----------
if process:
    if not source:
        st.warning("Please enter a YouTube URL or local file path.")
    else:
        try:
            with st.spinner("🎬 Processing video..."):
                st.session_state.result = run_pipeline(
                    source,
                    language
                )

            st.session_state.chat = []
            st.success("✅ Processing completed!")

        except Exception as e:
            st.error(f"❌ Error: {e}")


result = st.session_state.result


# ---------- Empty State ----------
if not result:
    st.info(
        "👈 Enter a YouTube URL or local file path and click "
        "**Process Video** to get started."
    )
    st.stop()


# ---------- Title ----------
st.markdown(
    f"""
    <div class="card">
        <div class="title">Generated Title</div>
        <h2>{result["title"]}</h2>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------- Metrics ----------
transcript = result.get("transcript", "")
words = len(transcript.split())

c1, c2, c3, c4 = st.columns(4)

metrics = [
    (words, "Transcript Words"),
    ("🧠", "Summary"),
    ("📌", "Action Items"),
    ("💬", "RAG Chat")
]

for col, (value, label) in zip(
    [c1, c2, c3, c4],
    metrics
):
    with col:
        st.markdown(
            f"""
            <div class="metric">
                <b>{value}</b>
                <span>{label}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------- Summary ----------
st.subheader("🧠 Summary")
with st.container(border=True):
    st.write(result["summary"])


# ---------- Decisions / Actions ----------
c1, c2 = st.columns(2)

with c1:
    st.subheader("✅ Action Items")
    with st.container(border=True):
        st.write(result["action_items"])

with c2:
    st.subheader("🔑 Key Decisions")
    with st.container(border=True):
        st.write(result["key_decisions"])


# ---------- Questions ----------
st.subheader("❓ Open Questions")
with st.container(border=True):
    st.write(result["open_questions"])


# ---------- Transcript ----------
st.subheader("📝 Transcript")

with st.expander("View full transcript"):
    st.text_area(
        "Transcript",
        transcript,
        height=400,
        label_visibility="collapsed"
    )


# ---------- RAG Chat ----------
st.subheader("💬 Chat with your Video")
st.caption("Ask questions about the processed video.")

for message in st.session_state.chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input("Ask something about the video...")

if question:
    st.session_state.chat.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                answer = ask_question(
                    result["rag_chain"],
                    question
                )

            st.markdown(answer)

            st.session_state.chat.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"❌ {e}")
