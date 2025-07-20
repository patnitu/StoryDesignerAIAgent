from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

class NovelNodeFactory:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def start_node(self, state):
        print("▶️ Node: start_node")
        return {}

    def analyze_part(self, state):
        print("▶️ Node: analyze_part")
        if state.uploaded_text.strip():
            summary = f"📝 Here's a summary of your existing novel:\n\n{state.uploaded_text[:300]}..."
        else:
            summary = "📖 Starting fresh — no existing novel part uploaded."
        return {"messages": state.messages + [AIMessage(content=summary)]}

    def suggest_plot(self, state):
        print("▶️ Node: suggest_plot")
        base = f"📚 Based on your idea: {state.query}."
        if state.uploaded_text.strip():
            base += f"\nExisting part: {state.uploaded_text[:200]}..."
        prompt = base + "\nSuggest a compelling next plot twist or continuation."
        response = self.llm.invoke(prompt)
        return {
            "plot_idea": response.content.strip(),
            "messages": state.messages + [AIMessage(content=response.content.strip())]
        }

    def generate_part(self, state):
        print("▶️ Node: generate_part")
        prompt = (
            f"Expand this plot idea into a new novel section (~{state.word_limit} words):\n\n"
            f"{state.plot_idea}"
        )
        response = self.llm.invoke(prompt)
        return {
            "story": response.content.strip(),
            "messages": state.messages + [AIMessage(content=response.content.strip())]
        }

    def refine_part(self, state):
        print("▶️ Node: refine_part")
        prompt = f"Refine this novel section for flow and style:\n\n{state.story}"
        response = self.llm.invoke(prompt)
        return {
            "story": response.content.strip(),
            "messages": state.messages + [AIMessage(content=response.content.strip())]
        }

    def clarify_part(self, state):
        print("▶️ Node: clarify_part")
        clarification = AIMessage(
            content=f"✅ Here's the refined novel part:\n\n{state.story}\n\nIs this good? (yes/no)"
        )
        return {"messages": state.messages + [clarification]}

    def final_output(self, state):
        print("🎉 Node: final_output")
        return {
            "story": state.story,
            "messages": state.messages + [AIMessage(content=f"✅ FINAL OUTPUT:\n\n{state.story}")]
        }
