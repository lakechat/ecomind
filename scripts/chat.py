"""Interactive terminal chat with EcoMind (for testing)."""

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from src.agent.graph import agent

def main():
    print("EcoMind - Your Sustainability Assistant")
    print("Type 'quit' to exit.\n")

    messages = []

    while True:
        user_input = input("Uou: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            print("Goodbye")

        if not user_input:
            continue

        messages.append(HumanMessage(content = user_input))

        #Run the agent
        result = agent.invoke({"messages": messages})

        # Get the last assistant message
        assistant_message = result["messages"][-1]
        print(f"\nEcoMind: {assistant_message.content}\n")

        #Update our message history
        messages = result["messages"]

if __name__ == "__main__":
    main()