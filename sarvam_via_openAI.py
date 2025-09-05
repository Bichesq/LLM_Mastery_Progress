from openai import OpenAI
from sarvamai import SarvamAI
# from sarvamai.models.chat import ChatCompletionMessage
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

Model_Ollama = "llama3.2:1b"
Model_Sarvam = "sarvam-m"

console = Console()

load_dotenv()

user_prompt = "What is the meaning of life?"
system_prompt = "You are someone who can't just answer questtions as they are asked, you much beat around the bush and try to confuse the person asking the question."


sarvam_via_openai = OpenAI (
    api_key=os.getenv("SARVAM_API_KEY"),
    base_url="https://api.sarvam.ai/v1"
)

sarvamai = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY"),
)

messages = [
    {
        "role": "system", "content": system_prompt
    },
    {
        "role": "user", "content": user_prompt
    }    
]

response = sarvam_via_openai.chat.completions.create(
    model=Model_Sarvam,
    messages=messages
)

console.print(Markdown(response.choices[0].message.content))