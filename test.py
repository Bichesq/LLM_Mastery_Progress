import requests
import ollama 
from bs4 import BeautifulSoup
from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI


# Constants

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2:1b"
ollama_via_openai = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1",
)
console = Console()

# Create a messages list using the same format that we used for OpenAI

messages = [
    {
        "role": "user", "content": "Describe some of the business applications of Generative AI"
    },
    {
        "role": "system", "content": "You are a helpful assistant. answer in markdown format."
    }
]

payload = {
    "model": MODEL,
    "messages": messages,
    "stream": False
}

# response = ollama.chat(
#     model=MODEL, 
#     messages=messages
# )

# print(response['message']['content'])

response = ollama_via_openai.chat.completions.create(
    model=MODEL,
    messages=messages
)
console.print(Markdown(response.choices[0].message.content))