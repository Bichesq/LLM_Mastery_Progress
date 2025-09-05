import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from sarvamai import SarvamAI

load_dotenv(override=True)

console = Console()

sarvam_api_key = os.getenv("SARVAM_API_KEY")
ollama_api_key = "ollama"
ollama_base_url = "http://localhost:11434/v1"
sarvam_base_url = "https://api.sarvam.ai/v1"

sarvam = SarvamAI(
    api_subscription_key=sarvam_api_key,
)

ollama_via_openai = OpenAI(
    api_key=ollama_api_key,
    base_url=ollama_base_url,
)

system_prompt = "You are an helpful assistant, but who always tries to come across like a polititian"
user_prompt = "How many letter word are there in your response to this question: who is the most Indian Person that has ever lived?"

messages = [
    {
        "role": "system", "content": system_prompt
    },
    {
        "role": "user", "content": user_prompt
    }    
]

# response = ollama_via_openai.chat.completions.create(
#     model="llama3.2:1b",
#     messages=messages,
#     temperature=0.6
# )

response = sarvam.chat.completions(
    messages=messages,
    temperature=0.6,
)

console.print(Markdown(response.choices[0].message.content))