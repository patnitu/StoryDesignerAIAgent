from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage


class NodeFactory:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def start_node(self, state):
        print("\n▶️ Node: start_node")
        return {}

    def generate_story(self, state):
        print("\n▶️ Node: generate_story")
        print(f"   Query: {state.query}, Type: {state.content_type}, Words: ~{state.word_limit}")

        if state.story:
            prompt = (
                f"Rewrite a different version of this {state.content_type} "
                f"using the same idea:\n\n"
                f"ORIGINAL VERSION:\n{state.story}\n\n"
                f"Keep it about {state.word_limit} words. Make it fresh and different."
            )
        elif state.uploaded_text.strip():
            prompt = (
                f"Continue this {state.content_type}.\n\n"
                f"EXISTING TEXT:\n{state.uploaded_text}\n\n"
                f"NEW INSTRUCTION:\n{state.query}\n\n"
                f"Make the new section about {state.word_limit} words."
            )
        else:
            prompt = (
                f"Write a {state.content_type} based on this idea: {state.query}. "
                f"Keep it about {state.word_limit} words. Be clear and creative."
            )

        response = self.llm.invoke(prompt)

        return {
            "story": response.content.strip(),
            "messages": state.messages + [AIMessage(content=response.content.strip())],
        }

    def refine_story(self, state):
        print("\n▶️ Node: refine_story")
        story_text = state.story or ""
        prompt = (
            f"Refine this {state.content_type} for clarity, consistency and flow (~{state.word_limit} words):\n\n{story_text}"
        )
        response = self.llm.invoke(prompt)
        return {
            "story": response.content.strip(),
            "messages": state.messages + [AIMessage(content=response.content.strip())],
        }

    def clarify_story(self, state):
        print("\n▶️ Node: clarify_story — asking user if output is okay.")
        clarification = AIMessage(
            content=f"📜 Here’s the refined {state.content_type} draft:\n\n{state.story}\n\nIs this okay? (yes/no)"
        )
        return {
            "story": state.story,  # ✅ keep the current version in state!
            "messages": state.messages + [clarification],
        }

    def final_script(self, state):
        print("\n✅ Node: final_script — Final output returned.")
        return {
            "story": state.story,
            "messages": state.messages + [AIMessage(content=f"✅ FINAL:\n\n{state.story}")],
        }
