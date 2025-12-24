from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY  
)

llm = Ollama(model="llama3")

prompt1 = ChatPromptTemplate.from_messages(
    [
        ("user", "write me an essay about {topic} with 100 words")
    ]
)

prompt2 = ChatPromptTemplate.from_messages(
    [
        ("user", "write me a poem about {topic} with 100 words")
    ]
)

# Gemini Essay Route
add_routes(
    app,
    prompt1 | model,
    path="/essay"
)

# Ollama Poem Route
add_routes(
    app,
    prompt2 | llm,
    path="/poem"
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
