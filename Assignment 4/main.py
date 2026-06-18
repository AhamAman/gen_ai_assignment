from dotenv import load_dotenv
from mem0 import Memory
import os

load_dotenv()

# Fetch environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "google_genai",
        "config": {
            "api_key": GEMINI_API_KEY, 
            "model": "text-embedding-004"
        },
    },
    "llm": {
        "provider": "google_genai",
        "config": {
            "api_key": GEMINI_API_KEY, 
            "model": "gemini-2.5-flash"
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333},
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URL,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD,
        },
    },
}

# Initialize the memory client with Gemini settings
mem_client = Memory.from_config(config)