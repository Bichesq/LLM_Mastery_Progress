import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)

shivaay_api_key = os.getenv("OPENAI_API_KEY")
shivaay_base_url = "https://api.futurixai.com/api/shivaay/v1"

shivaay_via_openai = OpenAI(
    api_key=shivaay_api_key,
    base_url=shivaay_base_url,
)

def test_api_parameters():
    """Test different parameter names to see what Shivaay supports"""
    
    test_cases = [
        {"name": "tools", "params": {"tools": [{"type": "function", "function": {"name": "test", "parameters": {}}}]}},
        {"name": "functions", "params": {"functions": [{"name": "test", "parameters": {}}]}},
        {"name": "tool_choice", "params": {"tool_choice": "auto"}},
        {"name": "function_call", "params": {"function_call": "auto"}}
    ]
    
    for test_case in test_cases:
        try:
            print(f"Testing parameter: {test_case['name']}")
            response = shivaay_via_openai.chat.completions.create(
                model="shivaay",
                messages=[{"role": "user", "content": "Hello"}],
                **test_case['params'],
                max_tokens=10
            )
            print(f"✅ {test_case['name']} is supported!")
            print(f"   Response: {response.choices[0].finish_reason}")
        except Exception as e:
            print(f"❌ {test_case['name']} failed: {e}")
        print()

# Also let's check the API documentation pattern by making a raw request
def check_api_documentation():
    """Check what the API expects by looking at possible patterns"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {shivaay_api_key}",
        "Content-Type": "application/json"
    }
    
    # Test different payload structures
    test_payloads = [
        {
            "model": "shivaay",
            "messages": [{"role": "user", "content": "Hello"}],
            "tools": [{"type": "function", "function": {"name": "test", "description": "test", "parameters": {}}}]
        },
        {
            "model": "shivaay", 
            "messages": [{"role": "user", "content": "Hello"}],
            "functions": [{"name": "test", "description": "test", "parameters": {}}]
        }
    ]
    
    for i, payload in enumerate(test_payloads):
        try:
            response = requests.post(
                f"{shivaay_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )
            print(f"Test {i+1} - Status: {response.status_code}")
            print(f"Response: {response.text}")
            if response.status_code == 200:
                data = response.json()
                print(f"Finish reason: {data['choices'][0]['finish_reason']}")
        except Exception as e:
            print(f"Test {i+1} failed: {e}")
        print()

if __name__ == "__main__":
    print("Testing Shivaay API parameters...")
    test_api_parameters()
    
    print("\nChecking API documentation patterns...")
    check_api_documentation()