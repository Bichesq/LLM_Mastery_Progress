import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

sarvam_api_key = os.getenv("SARVAM_API_KEY")

system_message = "You are a helpful assistant for an Airline called FlightAI."
system_message += "Give short, courteous answers, no more than 1 sentence."
system_message += "Always be accurate. If you don't know the answer, say so."

ticket_prices = {
    "New Delhi": 1000,
    "Bangaluru": 7000,
    "Mumbai": 3000
}

def get_ticket_price(destination_city):
    print (f"Tool get_ticket_price called with {destination_city}")
    return ticket_prices.get(destination_city, "I'm sorry, we don't fly to that destination.")

def call_sarvam_with_tools(messages, tools):
    """Call Sarvam API with tools using direct HTTP request"""
    
    headers = {
        "Content-Type": "application/json",
        # "X-API-Key": "sarvam_api_key",  # or whatever auth header Sarvam uses
        "Authorization": f"Bearer {sarvam_api_key}",  # try this if above doesn't work
    }
    
    payload = {
        "model": "sarvam-m",  # or your model name
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto"
    }

   
    
    # Try their actual API endpoint (check documentation)
    response = requests.post(
        "https://api.sarvam.ai/v1/chat/completions",  # or whatever their endpoint is
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API error: {response.status_code} - {response.text}")

# Your tool definition
tools = [{
    "type": "function",
    "function": {
        "name": "get_ticket_price",
        "description": "Get ticket price for a destination",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {"type": "string", "description": "City name"}
            },
            "required": ["destination"]
        }
    }
}]

# Example usage
try:
    result = call_sarvam_with_tools(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": "How much is the ticket price for Mumbai?"}
            ],
        tools=tools
    )
    print("Success:", result)
except Exception as e:
    print("Error:", e)