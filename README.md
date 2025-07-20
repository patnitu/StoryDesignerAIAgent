# 🎬 StoryDesigner AI ✨

**StoryDesigner AI** is an AI-powered creative writing assistant that helps you design quick stories, poems, jokes, and full-length novels with an interactive suggestion and clarification loop.

Built with **LangChain**, **OpenAI**, and **Streamlit**, it allows writers and hobbyists to:
- ✅ Generate short stories, poems, or jokes instantly
- ✅ Develop longer novels step-by-step
- ✅ Accept or refine AI-suggested plot ideas
- ✅ Clarify and rewrite sections with human feedback
- ✅ Download drafts or entire conversation history anytime

---

## 🚀 **Live Demo**

👉 [Try it now on Streamlit](YOUR_STREAMLIT_APP_URL)

---

## 🧩 **Features**

- ✍️ **Quick Story Mode:**  
  Generate short stories, poems, or jokes in seconds.

- 📚 **Novel Designer Mode:**  
  Build complex stories one part at a time. Accept, reject, or refine AI plot suggestions. Review and download your full creative conversation.

- 💾 **Downloads:**  
  Download your final story or your entire conversation as a `.txt` file.

- 🔐 **Secure:**  
  Uses your own OpenAI API key via `Streamlit secrets` — no keys exposed in code.

---

## ⚙️ **How it works**

1️⃣ Choose **Quick Story/Poem/Joke** or **Novel Designer** mode  
2️⃣ Describe your idea  
3️⃣ Let the AI generate content  
4️⃣ Accept or ask for new suggestions  
5️⃣ Download your work!

---

## 🛠️ **Tech Stack**

- **Python** 🐍  
- **Streamlit** – interactive UI  
- **LangChain** – handles AI workflows  
- **OpenAI** – large language model generation

---

## 🚀 **Run Locally**

```bash
# Clone the repo
git clone https://github.com/YOUR_GITHUB/StoryDesignerAI.git
cd StoryDesignerAI

# Create a virtual environment & activate
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key in a `.env` or Streamlit secrets:
export OPENAI_API_KEY="YOUR_API_KEY"

# Run the app
streamlit run Streamlit_app.py
