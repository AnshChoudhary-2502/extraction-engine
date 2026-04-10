from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API_KEY_ANSH=os.getenv("GROQ_API_KEY_ANSH")
MISTRAL_API_KEY=os.getenv("MISTRAL_API_KEY")
GROQ_API_KEY_KHUSHI=os.getenv("GROQ_API_KEY_KHUSHI")

# Centralized configuration for easy optimization
CONFIG1 = {
    "model_name": "llama-3.1-8b-instant",
    "temperature": 0.1,
    "max_retries": 2,
    "api_key": GROQ_API_KEY_KHUSHI
}
CONFIG2 = {
    "model_name": "llama-3.1-8b-instant",
    "temperature": 0.1,
    "max_retries": 2,
    "api_key": GROQ_API_KEY_ANSH
}
CONFIG3 = {
    "model_name": "mistral-large-latest",
    "temperature": 0.1,
    "max_retries": 2,
    "api_key": MISTRAL_API_KEY
}

model1 = ChatGroq(
    model=CONFIG1["model_name"],
    temperature=CONFIG1["temperature"],
    max_retries=CONFIG1["max_retries"],
    api_key=CONFIG1["api_key"]
)

model2 = ChatGroq(
    model=CONFIG2["model_name"],
    temperature=CONFIG2["temperature"],
    max_retries=CONFIG2["max_retries"],
    api_key=CONFIG2["api_key"]
)

model3 = ChatMistralAI(
    model=CONFIG3["model_name"],
    temperature=CONFIG3["temperature"],
    top_p=0.9,
    api_key=CONFIG3["api_key"]
)

# Task-specific aliases
extraction_model = model1
search_model = model2
answer_model = model3
