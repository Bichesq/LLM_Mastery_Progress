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

user_prompt = "Describe how you will go about creating  and AI based class-notes generator for students in MCA, that is tailored to their semester exams. "
system_prompt = "You are highly trained Teacher, with masters in Computer Applications and ten years of teaching experience. You are especially skilled in creating lesson notes with the content and structure that will get the students to Ace their exams. You base you lesson notes on past exam questions."



# ollama_via_openai = OpenAI(
#     api_key="ollama",
#     base_url="http://localhost:11434/v1",
# )

# sarvam_via_openai = OpenAI (
#     api_key=os.getenv("SARVAM_API_KEY"),
#     base_url="https://sarvan"
# )

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

# response = ollama_via_openai.chat.completions.create(
#     model=Model_Sarvam,
#     messages=messages
# )

response_sarvamai = sarvamai.chat.completions(
    messages=messages
)

print(response_sarvamai.choices[0].message.content)