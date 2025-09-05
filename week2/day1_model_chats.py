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

# sarvam_via_openai = OpenAI(
#     api_key=sarvam_api_key,
#     base_url=sarvam_base_url,
# )

# Let's make a conversation between sarvam-m and llama3.2:1b

ollama_model = "llama3.2:1b"
sarvam_model = "sarvam-m"

# sarvam_system = "You are a chatbot who is very argumentative; \
# you disagree with anything in the conversation and you challenge everything, in a snarky way."
sarvam_system = "You are Jesus Christ."

# ollama_system = "You are a very polite, courteous chatbot. You try to agree with \
# everything the other person says, or find common ground. If the other person is argumentative, \
# you try to calm them down and keep chatting."
ollama_system = "You are God the Father."



def call_sarvam():
    messages = [{"role": "system", "content": sarvam_system}]
    for sarvam_mg, ollama_mg in zip(sarvam_messages, ollama_messages):
        messages.append({"role": "user", "content": ollama_mg})
        messages.append({"role": "assistant", "content": sarvam_mg}) 
    messages.append({"role": "user", "content": ollama_messages[-1]})       
    completion = sarvam.chat.completions(messages=messages)    
    return completion.choices[0].message.content

# call_sarvam()

def call_ollama():
    messages = [{"role": "system", "content": ollama_system}]
    for ollama_mg, sarvam_mg in zip(ollama_messages, sarvam_messages):
        messages.append({"role": "user", "content": sarvam_mg})
        messages.append({"role": "assistant", "content": ollama_mg})
    # messages.append({"role": "user", "content": sarvam_messages[-1]})
    message = ollama_via_openai.chat.completions.create(
        model=ollama_model,
        messages=messages
    )
    return message.choices[0].message.content

# call_ollama()

sarvam_messages = ["Hello, Father."]
ollama_messages = ["Hello, Son. How are you?"]

print(f"Sarvam:\n{sarvam_messages[0]}\n")
print(f"Ollama:\n{ollama_messages[0]}\n")

for i in range(5):
    sarvam_next = call_sarvam()
    print(f"Sarvam:\n{sarvam_next}\n")
    sarvam_messages.append(sarvam_next)
    
    ollama_next = call_ollama()
    print(f"Ollama:\n{ollama_next}\n")
    ollama_messages.append(ollama_next)