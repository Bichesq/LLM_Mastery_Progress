import json
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

system_prompt = "You are quit the smart person who is good at anserwing riddles."
user_prompt = "why do girls rub their eyes when they getup in the morning? remember this is a riddle and its just for fun. Hint: boys scratch something else."

messages = [
    {
        "role": "system", "content": system_prompt
    },
    {
        "role": "user", "content": user_prompt
    }    
]



headers = {
    "Authorization": f"Bearer {sarvam_api_key}",
    "Content-Type": "application/json",
    "Accept": "text/event-stream"  # Key header for SSE
}

payload = {
    "model": "sarvam-m",
    "messages": messages,
    "max_tokens": 500,
    "stream": True  # This is the crucial parameter that enables streaming
}

response = requests.post(f"{sarvam_base_url}/chat/completions", json=payload, headers=headers, stream=True)

# Check if the request was successful before reading the stream
if response.status_code == 200:
    for line in response.iter_lines():
        # Filter out keep-alive new lines
        if line:
            decoded_line = line.decode('utf-8')
            
            # The API sends Server-Sent Events (SSE) formatted as "data: {json}"
            if decoded_line.startswith('data:'):
                json_data = decoded_line[5:].strip()  # Remove the "data: " prefix
                
                # Check for the terminal [DONE] message
                if json_data == '[DONE]':
                    break
                
                try:
                    # Parse the JSON data from this chunk
                    chunk = json.loads(json_data)
                    
                    # Extract the token from the response structure
                    # Based on your error log: choices[0].delta.content
                    choices = chunk.get("choices", [])
                    if choices:
                        delta = choices[0].get("delta", {})
                        token = delta.get("content", "")
                        print(token, end='', flush=True)  # Stream the token to console
                        
                except json.JSONDecodeError as e:
                    print(f"\nError decoding JSON: {json_data}")
                    print(f"Error: {e}")
                    continue
else:
    print(f"API request failed with status code: {response.status_code}")
    print(response.text)

print("\n\nStream complete.")