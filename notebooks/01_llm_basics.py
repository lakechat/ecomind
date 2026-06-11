from dotenv import load_dotenv
load_dotenv()

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize the LLM (free via NVIDIA NIM!)
# Options: "meta/llama-3.1-70b-instruct", "meta/llama-3.1-8b-instruct",
#          "nvidia/nemotron-4-340b-instruct", etc.
# Browse all available models at https://build.nvidia.com
#llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct", temperature=0.7)
llm = ChatNVIDIA(model="deepseek-ai/deepseek-v4-flash", temperature=0.7)

# Simple call
response = llm.invoke([HumanMessage(content="What's the carbon footprint of a cheeseburger?")])
print(response.content)

# With system prompt
response = llm.invoke([
    SystemMessage(content="You are a sustainability expert. Give concise, factual answers."),
    HumanMessage(content="What's the carbon footprint of a cheeseburger?")
])
print(response.content)