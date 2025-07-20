from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List, Any

from nodes import NodeFactory


class AgentState(BaseModel):
    query: str = ""
    story: str = ""
    messages: List[Any] = []
    user_input: str = ""
    content_type: str = ""
    word_limit: int = 100
    uploaded_text: str = ""


class StoryDesignerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.node_factory = NodeFactory(llm)

    def build_graph(self):
        graph = StateGraph(AgentState)

        graph.add_node("start_node", self.node_factory.start_node)
        graph.add_node("generate_story", self.node_factory.generate_story)
        graph.add_node("refine_story", self.node_factory.refine_story)
        graph.add_node("clarify_story", self.node_factory.clarify_story)
        graph.add_node("final_script", self.node_factory.final_script)

        graph.set_entry_point("start_node")

        graph.add_edge("start_node", "generate_story")
        graph.add_edge("generate_story", "refine_story")
        graph.add_edge("refine_story", "clarify_story")

        def clar_branch(state):
            user = state.user_input.lower().strip()
            print(f"Branch: User said: {user}")
            if "yes" in user:
                return "final_script"
            elif "no" in user:
                return "generate_story"
            else:
                return "clarify_story"

        graph.add_conditional_edges("clarify_story", clar_branch)

        return graph.compile()
