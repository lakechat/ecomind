"""LangGraph agent definition for EcoMind"""

import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from src.agent.prompts import SYSTEM_PROMPT

# --- State Definition ---
class AgentState(TypedDict):
    """The state that flows through our grpaph"""
    messages: Annotated[list[BaseMessage], add_messages]

# --- Node Functions ---
def chatbot_node(state: AgentState) -> AgentState:
    """The main chatbot node - sends messages to the LLM and returns the response."""
    llm = ChatNVIDIA(
        model = "nvidia/nemotron-3-ultra-550b-a55b",
        temperature = 0.7,
        max_tokens = 1024,
        api_key=os.getenv("NVIDIA_API_KEY"),
    )

    # prepend system message to the conversation
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]

    #Call the LLM
    response = llm.invoke(messages)
    #Return updatd state (add_messages annotation handles appending)
    return {"messages": [response]}


# --- Graph Construction ---
def build_graph():
    """Build and compile the LangGraph agent."""
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("chatbot", chatbot_node)

    # Add edges
    graph.add_edge(START, "chatbot")
    graph.add_edge("chatbot", END)

    #Compile
    return graph.compile()

# Singleton for reuse
agent = build_graph()




