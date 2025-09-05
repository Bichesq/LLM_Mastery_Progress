import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr # oh yeah!
from sarvamai import SarvamAI

load_dotenv(override=True)

shivaay_api_key = os.getenv("OPENAI_API_KEY")
shivaay_base_url="https://api.futurixai.com/api/shivaay/v1"
sarvam_api_key = os.getenv("SARVAM_API_KEY")
sarvam_base_url = "https://api.sarvam.ai/v1"

sarvam = SarvamAI(
    api_subscription_key=sarvam_api_key,
)


sarvam_via_openai = OpenAI(
    api_key=sarvam_api_key,
    base_url=sarvam_base_url,
)

# shivaay_via_openai = OpenAI(
#     api_key=shivaay_api_key,
#     base_url=shivaay_base_url,
# )

ticket_prices = {
    "New Delhi": 1000,
    "Bangaluru": 7000,
    "Mumbai": 3000
}

def get_ticket_price(destination_city):
    print (f"Tool get_ticket_price called with {destination_city}")
    return ticket_prices.get(destination_city, "I'm sorry, we don't fly to that destination.")

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. \
        Call this whenever you need the ticket price, for example whenever \
            a customer asks 'How much is the ticket to this city?'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The name of the destination city"
            }
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": price_function}]

# We have to write that function handle_tool_call:

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get('destination_city')
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "price": price}),
        "tool_call_id": tool_call.id
    }
    return response, city

system_message = "You are a helpful assistant for an Airline called FlightAI."
system_message += "Give short, courteous answers, no more than 1 sentence."
system_message += "Always be accurate. If you don't know the answer, say so."

def Chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = sarvam_via_openai.chat.completions.create(
        model="sarvam-m",
        messages=messages,
        tools=tools
    )

    if response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = sarvam_via_openai.chat.completions.create(
            model="sarvam-m",
            messages=messages
        )
    return response.choices[0].message.content

gr.ChatInterface(fn=Chat, type='messages').launch(share=True, inbrowser=True)

