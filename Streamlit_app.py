import streamlit as st
from langchain_openai import ChatOpenAI
from agent import StoryDesignerAgent  # Quick Story
from novel_agent import NovelDesignerAgent  # Novel Designer
from config import Config

# -------------------------------
# ✅ Init both agents ONCE
# -------------------------------
@st.cache_resource
def init_story_agent():
    llm = ChatOpenAI(model=Config.MODEL_NAME, api_key=Config.OPENAI_API_KEY)
    return StoryDesignerAgent(llm).build_graph()

@st.cache_resource
def init_novel_agent():
    llm = ChatOpenAI(model=Config.MODEL_NAME, api_key=Config.OPENAI_API_KEY)
    return NovelDesignerAgent(llm).build_graph()

story_app = init_story_agent()
novel_app = init_novel_agent()

# -------------------------------
# ✅ Title + Mode
# -------------------------------
st.title("🎬 AI Content Creator")

mode = st.radio("Choose Mode:", ["Quick Story/Poem/Joke", "Novel Designer"])

# -------------------------------
# ✅ Session State
# -------------------------------
if "query" not in st.session_state:
    st.session_state.query = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "awaiting_clarification" not in st.session_state:
    st.session_state.awaiting_clarification = False
if "inputs" not in st.session_state:
    st.session_state.inputs = {}
if "run_next" not in st.session_state:
    st.session_state.run_next = False
if "latest_plot" not in st.session_state:
    st.session_state.latest_plot = ""
if "rerun_needed" not in st.session_state:
    st.session_state.rerun_needed = False

latest = ""
# -------------------------------
# ✅ QUICK STORY MODE
# -------------------------------
if mode == "Quick Story/Poem/Joke":
    st.header("✨ Quick Story Designer")

    query = st.text_area("Describe your idea:", value=st.session_state.query)
    ctype = st.selectbox("Content Type:", ["Short Story", "Poem", "Joke"])
    wlimit = st.number_input("Approx Words:", value=100, min_value=10, max_value=500)
    upload_text = st.text_area("Upload prior content (optional):", "")

    if st.button("Generate"):
        st.session_state.query = query
        st.session_state.messages = []
        st.session_state.awaiting_clarification = False
        st.session_state.inputs = {
            "query": query,
            "content_type": ctype,
            "word_limit": wlimit,
            "uploaded_text": upload_text,
        }

        for event in story_app.stream(st.session_state.inputs):
            st.session_state.messages.append(event)
            if "clarify_story" in event:
                st.session_state.awaiting_clarification = True
                break

    if st.session_state.awaiting_clarification:
        with st.form(key="clarify_form_story"):
            user_reply = st.radio("Is this version acceptable?", ["yes", "no"])
            submit = st.form_submit_button("Submit")

            if submit:
                st.session_state.inputs["user_input"] = user_reply

                if user_reply == "yes":
                    st.session_state.awaiting_clarification = False
                    st.rerun()
                else:
                    for next_event in story_app.stream(st.session_state.inputs):
                        st.session_state.messages.append(next_event)
                        if "clarify_story" in next_event:
                            st.session_state.awaiting_clarification = True
                            break

    st.subheader("📜 Current Draft:")
    latest = ""
    for m in reversed(st.session_state.messages):
        for k, v in m.items():
            if isinstance(v, dict) and "story" in v:
                latest = v["story"]
                break
        if latest:
            break

    if latest:
        st.write(latest)
        if not st.session_state.awaiting_clarification:
            st.download_button("📥 Download Final", latest, file_name="final_story.txt")
    else:
        st.info("Describe your idea above to start.")

# -------------------------------
# ✅ NOVEL DESIGNER MODE
# -------------------------------
# Inside your main Streamlit app — replace only the NOVEL DESIGNER MODE block

# ✅ NOVEL DESIGNER MODE — FULL FIXED BLOCK

if mode == "Novel Designer":
    all_content = []
    st.header("📖 Novel Designer")

    uploaded_file = st.file_uploader("Upload your last saved novel part (.txt):", type=["txt"])
    new_idea = st.text_area("Describe what you want to add next:")
    wlimit = st.number_input("Approx Words for Next Part:", value=500, min_value=100, max_value=5000)

    if st.button("Continue Novel"):
        uploaded_text = uploaded_file.read().decode("utf-8") if uploaded_file else ""

        st.session_state.query = new_idea
        st.session_state.messages = []
        st.session_state.awaiting_clarification = False
        st.session_state.inputs = {
            "query": new_idea,
            "content_type": "Novel",
            "word_limit": wlimit,
            "uploaded_text": uploaded_text,
            "jump_to_suggest": True
        }

        for event in novel_app.stream(st.session_state.inputs):
            st.session_state.messages.append(event)
            if "plot_idea" in str(event):
                st.session_state.awaiting_clarification = "suggest"
                break
            if "clarify_part" in str(event):
                st.session_state.awaiting_clarification = "clarify"
                break

    if st.session_state.awaiting_clarification == "suggest":
        with st.form(key="suggest_form"):
            user_reply = st.radio("Do you accept this plot suggestion?", ["accept", "give another suggestion"])
            submit = st.form_submit_button("Submit")

            if submit:
                if user_reply == "accept":
                    st.session_state.inputs["plot_idea"] = st.session_state.latest_plot
                    st.session_state.inputs["jump_to_suggest"] = False
                    st.session_state.run_next = True
                    st.session_state.awaiting_clarification = False
                    st.rerun()
                else:
                    st.session_state.run_next = False
                    for event in novel_app.stream(st.session_state.inputs):
                        st.session_state.messages.append(event)
                        if "plot_idea" in str(event):
                            st.session_state.awaiting_clarification = "suggest"
                            break

    elif st.session_state.awaiting_clarification == "clarify":
        with st.form(key="clarify_form"):
            user_reply = st.radio("Is this final part okay?", ["yes", "no"])
            submit = st.form_submit_button("Submit")

            if submit:
                st.session_state.inputs["user_input"] = user_reply
                if user_reply == "yes":
                    st.session_state.awaiting_clarification = False
                else:
                    for next_event in novel_app.stream(st.session_state.inputs):
                        st.session_state.messages.append(next_event)
                        if "clarify_part" in next_event:
                            st.session_state.awaiting_clarification = "clarify"
                            break

    if st.session_state.get("run_next", False):
        st.session_state.run_next = False

        for event in novel_app.stream(st.session_state.inputs):
            st.session_state.messages.append(event)
            if "clarify_part" in event:
                st.session_state.awaiting_clarification = "clarify"
                st.session_state.rerun_needed = True
                break

        if st.session_state.rerun_needed:
            st.session_state.rerun_needed = False
            st.rerun()

    st.subheader("📖 Latest Novel Output:")

    latest_plot = ""
    latest_story = ""

    for m in reversed(st.session_state.messages):
        for k, v in m.items():
            if isinstance(v, dict) and "plot_idea" in v:
                latest_plot = v["plot_idea"]
                st.session_state.latest_plot = latest_plot
                break
            if isinstance(v, dict) and "story" in v:
                latest_story = v["story"]
                break
        if latest_plot or latest_story:
            break

    # ✅ 👉 Combine all messages for download
    
    for m in st.session_state.messages:
        for k, v in m.items():
            if isinstance(v, dict):
                if "plot_idea" in v:
                    all_content.append(f"[Plot Idea]\n{v['plot_idea']}")
                if "story" in v:
                    all_content.append(f"[Story Part]\n{v['story']}")
    combined_text = "\n\n".join(all_content) if all_content else "No parts yet."

    # ✅ Always show the current conversation download button
    st.download_button("⬇️ Download Current Conversation", combined_text, file_name="novel_conversation.txt")

    if st.session_state.awaiting_clarification == "suggest" and latest_plot:
        st.write(latest_plot)
    elif latest_story:
        st.write(latest_story)
    else:
        st.info("Upload your last part and describe the next plot!")

    # ✅ Final download button stays the same!
    
from fpdf import FPDF
from io import BytesIO

# ✅ Build the PDF
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

pdf.set_font("Times", 'B', 16)
pdf.cell(0, 10, "Your Novel Conversation", ln=True, align='C')
pdf.ln(10)

pdf.set_font("Times", '', 12)
for part in all_content:
    pdf.multi_cell(0, 10, part)
    pdf.ln(5)

# ✅ ✅ Correct: get bytes instead of passing BytesIO directly
pdf_bytes = pdf.output(dest='S').encode('latin-1')
pdf_buffer = BytesIO(pdf_bytes)

# ✅ Add your download button
st.download_button(
    "📄 Download Styled PDF",
    pdf_buffer,
    file_name="novel_conversation.pdf",
    mime="application/pdf"
)

if not st.session_state.awaiting_clarification:
        if latest_story:
            combined_text = "\n\n".join(all_content) if all_content else "No parts yet."

# ✅ Always show the current conversation download button
            st.download_button("⬇️ Download Current Conversation", combined_text, file_name="novel_conversation.txt")
