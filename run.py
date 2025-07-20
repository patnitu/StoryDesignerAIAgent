from langchain_openai import ChatOpenAI
from config import Config
from agent import StoryDesignerAgent

def main():
    llm = ChatOpenAI(
        model=Config.MODEL_NAME,
        api_key=Config.OPENAI_API_KEY
    )

    agent = StoryDesignerAgent(llm)
    app = agent.build_graph()

    query = "There is a boy and a girl who fall in love, but their parents disagree. The climax is dramatic."
    inputs = {"query": query}

    print("\n🎬 Starting Story Designer Agent...\n")

    for event in app.stream(inputs):
        print("EVENT:", event)

        if "clarify_story" in event:
            user_reply = input("\nUSER → Is this story acceptable? (yes/no): ")
            inputs["user_input"] = user_reply

if __name__ == "__main__":
    main()
