import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr # oh yeah!
from sarvamai import SarvamAI

load_dotenv(override=True)

ollama_api_key = "ollama"
ollama_base_url = "http://localhost:11434/v1"
ollama_model = "llama3.2:1b"
sarvam_model = "sarvam-m"
sarvam_api_key = os.getenv("SARVAM_API_KEY")
sarvam_base_url = "https://api.sarvam.ai/v1"
shivaay_base_url="https://api.futurixai.com/api/shivaay/v1"
shivaay_api_key = os.getenv("SHIVAAI_API_KEY")

ollama_via_openai = OpenAI(
    api_key=ollama_api_key,
    base_url=ollama_base_url,
)

sarvam = SarvamAI(
    api_subscription_key=sarvam_api_key,
)

system_prompt = "You are a helpful assistant"

def message_prompt (prompt):
    messages = [
        {
            "role": "system", "content": system_prompt
        },
        {
            "role": "user", "content": prompt
        }    
    ]
    response = sarvam.chat.completions(messages=messages)
    return response.choices[0].message.content

gr.Interface(fn=message_prompt, inputs=[gr.Textbox(label="Your message")], outputs=[gr.Markdown(label="Assistant's response")], flagging_mode="never").launch(share=True, inbrowser=True)

