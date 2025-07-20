from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List, Any
from novel_nodes import NovelNodeFactory

class NovelState(BaseModel):
    query: str = ""
    plot_idea: str = ""
    story: str = ""
    uploaded_text: str = ""
    user_input: str = ""
    messages: List[Any] = []
    word_limit: int = 500
    jump_to_suggest: bool = True  # ✅ NEW: controls whether to run suggest_plot

class NovelDesignerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.node_factory = NovelNodeFactory(llm)

    def build_graph(self):
        graph = StateGraph(NovelState)

        graph.add_node("start_node", self.node_factory.start_node)
        graph.add_node("analyze_part", self.node_factory.analyze_part)
        graph.add_node("suggest_plot", self.node_factory.suggest_plot)
        graph.add_node("generate_part", self.node_factory.generate_part)
        graph.add_node("refine_part", self.node_factory.refine_part)
        graph.add_node("clarify_part", self.node_factory.clarify_part)
        graph.add_node("final_output", self.node_factory.final_output)

        graph.set_entry_point("start_node")

        # ✅ Conditional branch on start_node to skip suggest_plot if accepted
        graph.add_conditional_edges("start_node", self.start_branch)
        graph.add_edge("analyze_part", "suggest_plot")
        graph.add_edge("suggest_plot", "generate_part")
        graph.add_edge("generate_part", "refine_part")
        graph.add_edge("refine_part", "clarify_part")
        graph.add_conditional_edges("clarify_part", self.clarify_branch)

        return graph.compile()

    def start_branch(self, state):
        print("🔀 Start Branch: jump_to_suggest =", state.jump_to_suggest)
        if state.jump_to_suggest:
            return "analyze_part"
        else:
            return "generate_part"

    def clarify_branch(self, state):
        print("🔀 Clarify Branch:", state.user_input)
        if "yes" in state.user_input.lower():
            return "final_output"
        else:
            return "refine_part"
