import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr # oh yeah!
# from sarvamai import SarvamAI

load_dotenv(override=True)

shivaay_api_key = os.getenv("OPENAI_API_KEY")

shivaay_base_url="https://api.futurixai.com/api/shivaay/v1"

sarvam_api_key = os.getenv("SARVAM_API_KEY")
sarvam_base_url = "https://api.sarvam.ai/v1"

shivaay_via_openai = OpenAI(
    api_key=shivaay_api_key,
    base_url=shivaay_base_url,
)

# sarvam_via_openai = OpenAI(
#     api_key=sarvam_api_key,
#     base_url=sarvam_base_url,
# )



system_message = "You are a helpful assistant in a clothes store. You should try to gently encourage \
the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. \
For example, if the customer says 'I'm looking to buy a hat', \
you could reply something like, 'Wonderful - we have lots of hats - including several that are part of our sales event.'\
Encourage the customer to buy hats if they are unsure what to get."

def chat( message, history):
    # system_message += "\nIf the customer asks for shoes, you should respond that shoes are not on sale today, \
    # but remind the customer to look at hats!"

    relevant_system_message = system_message

    if "belt" in message.lower():
        relevant_system_message += "\nIf the customer asks for a belt, you should respond that belts are not on sale today, \
        but remind the customer to look at hats!"
    messages  = [{"role": "system", "content": relevant_system_message}] + history + [{"role": "user", "content": message}]

    print("Historty is:")
    print(history)
    print("And messages is:")
    print(messages)

    stream = shivaay_via_openai.chat.completions.create(
        model="shivaay",
        messages=messages,
        stream=True
    )

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response

gr.ChatInterface(fn=chat, type='messages').launch(share=True, inbrowser=True)