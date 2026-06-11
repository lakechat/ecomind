"""Run this to verify your environment is correctly set up."""
import os
from dotenv import load_dotenv

load_dotenv()

def check(name, condition, hint=""):
    status = "✅" if condition else "❌"
    print(f"{status} {name}")
    if not condition and hint:
        print(f"   💡 {hint}")

    return condition

all_good = True

# Check API keys
all_good &= check(
    "NVIDIA NIM API key",
    os.getenv("NVIDIA_API_KEY", "").startswith("nvapi-"),
    "Set NVIDIA_API_KEY in .env — get yours free at https://build.nvidia.com"
)
all_good &= check(
    "LangSmith API key",
    os.getenv("LANGCHAIN_API_KEY", "").startswith("lsv2_"),
    "Set LANGCHAIN_API_KEY in .env"
)
all_good &= check(
    "LangSmith tracing enabled",
    os.getenv("LANGCHAIN_TRACING_V2") == "true",
    "Set LANGCHAIN_TRACING_V2=true in .env"
)

# Check imports
try:
    import langchain
    all_good &= check("Langchain installed", True)
except ImportError:
    all_good &= check("LangChain installed", False, "pip install langchain")

try:
    import langgraph
    all_good &= check("LangGraph installed", True)
except ImportError:
    all_good &= check("LangGraph installed", False, "pip install langgraph")

try:
    from langchain_nvidia_ai_endpoints import ChatNVIDIA
    all_good &= check("NVIDIA AI Endpoints installed", True)
except ImportError:
    all_good &= check("NVIDIA AI Endpoints installed", False, "pip install langchain-nvidia-ai-endpoints")

try:
    import chromadb
    all_good &= check("ChromaDB installed", True)
except ImportError:
    all_good &= check("ChromaDB installed", False, "pip install chromadb")

try:
    import streamlit
    all_good &= check("Streamlit installed", True)
except ImportError:
    all_good &= check("Streamlit installed", False, "pip install streamlit")

try:
    import sqlalchemy
    all_good &= check("SQLAlchemy installed", True)
except ImportError:
    all_good &= check("SQLAlchemy installed", False, "pip install sqlalchemy")

try:
    import numpy
    all_good &= check("NumPy installed", True)
except ImportError:
    all_good &= check("NumPy installed", False, "pip install numpy")

# Check database connection
try:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        all_good &= check("Database connection", False, "DATABASE_URL is missing in .env")
    else:
        import sqlalchemy
        engine = sqlalchemy.create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))
        all_good &= check("Database connection", True)
except Exception as e:
    all_good &= check("Database connection", False, f"Check DATABASE_URL in .env and ensure your database is running. Error: {e}")

# Quick LLM test
try:
    from langchain_nvidia_ai_endpoints import ChatNVIDIA
    # Use max_tokens for better compatibility across versions
    llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct", max_tokens=50)
    response = llm.invoke("Hello, world!")
    all_good &= check("LLM test", True)
except Exception as e:
    all_good &= check("LLM test", False, f"Check your NVIDIA_API_KEY and ensure you have access to the model. Error: {e}")

# Quick Embedding test
try:
    from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
    embed = NVIDIAEmbeddings(model="nvidia/nv-embedqa-e5-v5")
    embed.embed_query("test")
    all_good &= check("Embeddings test", True)
except Exception as e:
    all_good &= check("Embeddings test", False, f"Check if the embedding model name is correct. Error: {e}")

print("\n" + ("🎉 All checks passed! You're ready to start." if all_good
    else "⚠️  Some checks failed. Fix the issues above before proceeding."))
