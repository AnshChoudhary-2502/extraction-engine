from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Centralized configuration for easy optimization
CONFIG = {
    "model_name": "llama-3.1-8b-instant",
    "temperature": 0.1,  # Lower temperature for more consistent extraction
    "max_retries": 2
}

model = ChatGroq(
    model=CONFIG["model_name"],
    temperature=CONFIG["temperature"],
    max_retries=CONFIG["max_retries"],
    
)
