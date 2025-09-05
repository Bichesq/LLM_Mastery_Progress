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

# Base prices for different routes (departure -> destination)
route_prices = {
    ("Chandigarh", "Mumbai"): 350,
    ("Chandigarh", "Delhi"): 200,
    ("Chandigarh", "New Delhi"): 200,
    ("Chandigarh", "Bangalore"): 450,
    ("Chandigarh", "Bengaluru"): 450,
    ("Chandigarh", "Bangaluru"): 450,
    ("Delhi", "Mumbai"): 300,
    ("Delhi", "Bangalore"): 400,
    ("Delhi", "Bengaluru"): 400,
    ("Delhi", "Bangaluru"): 400,
    ("New Delhi", "Mumbai"): 300,
    ("New Delhi", "Bangalore"): 400,
    ("New Delhi", "Bengaluru"): 400,
    ("New Delhi", "Bangaluru"): 400,
    ("Mumbai", "Delhi"): 300,
    ("Mumbai", "New Delhi"): 300,
    ("Mumbai", "Bangalore"): 350,
    ("Mumbai", "Bengaluru"): 350,
    ("Mumbai", "Bangaluru"): 350,
    ("Mumbai", "Chandigarh"): 350,
    ("Bangalore", "Mumbai"): 350,
    ("Bangalore", "Delhi"): 400,
    ("Bangalore", "New Delhi"): 400,
    ("Bangalore", "Chandigarh"): 450,
    ("Bengaluru", "Mumbai"): 350,
    ("Bengaluru", "Delhi"): 400,
    ("Bengaluru", "New Delhi"): 400,
    ("Bengaluru", "Chandigarh"): 450,
    ("Bangaluru", "Mumbai"): 350,
    ("Bangaluru", "Delhi"): 400,
    ("Bangaluru", "New Delhi"): 400,
    ("Bangaluru", "Chandigarh"): 450,
}

def get_ticket_price(departure_city, destination_city, travel_date):
    print(f"🔧 Tool get_ticket_price called with: departure='{departure_city}', destination='{destination_city}', date='{travel_date}'")

    # Normalize city names (handle common variations)
    def normalize_city(city):
        city = city.strip().title()
        if city.lower() in ['delhi', 'new delhi']:
            return 'Delhi'
        elif city.lower() in ['bangalore', 'bengaluru', 'bangaluru']:
            return 'Bangalore'
        elif city.lower() == 'mumbai':
            return 'Mumbai'
        elif city.lower() == 'chandigarh':
            return 'Chandigarh'
        return city

    departure_normalized = normalize_city(departure_city)
    destination_normalized = normalize_city(destination_city)

    # Check if route exists
    route = (departure_normalized, destination_normalized)
    price = route_prices.get(route)

    if price:
        return f"The ticket from {departure_normalized} to {destination_normalized} on {travel_date} costs ${price}. Prices are subject to change."
    else:
        available_destinations = set()
        for dep, dest in route_prices.keys():
            if dep == departure_normalized:
                available_destinations.add(dest)

        if available_destinations:
            return f"Sorry, we don't have flights from {departure_normalized} to {destination_normalized}. We fly from {departure_normalized} to: {', '.join(sorted(available_destinations))}."
        else:
            return f"Sorry, we don't have flights departing from {departure_normalized}."

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a ticket from departure city to destination city on a specific date. Call this whenever a customer asks about ticket prices between cities.",
    "parameters": {
        "type": "object",
        "properties": {
            "departure_city": {
                "type": "string",
                "description": "The name of the departure city (e.g., 'Chandigarh', 'Delhi', 'Mumbai', 'Bangalore')"
            },
            "destination_city": {
                "type": "string",
                "description": "The name of the destination city (e.g., 'Mumbai', 'Delhi', 'Bangalore', 'Chandigarh')"
            },
            "travel_date": {
                "type": "string",
                "description": "The travel date in YYYY-MM-DD format (e.g., '2025-09-30')"
            }
        },
        "required": ["departure_city", "destination_city", "travel_date"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": price_function}]

def detect_price_request(text):
    """Detect if the user is asking for a price"""
    import re
    price_keywords = ['price', 'cost', 'fare', 'ticket', 'much', 'expensive', 'cheap']
    return any(keyword in text.lower() for keyword in price_keywords)

def extract_travel_info(text):
    """Extract travel information from user message"""
    import re

    # Common city patterns
    cities = ['chandigarh', 'delhi', 'mumbai', 'bangalore', 'bengaluru', 'bangaluru', 'new delhi']

    # Look for "from X to Y" pattern
    from_to_pattern = r'from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+?)(?:\s+on\s+|\s+for\s+|\s+|$)'
    match = re.search(from_to_pattern, text.lower())

    departure_city = None
    destination_city = None
    travel_date = None

    if match:
        departure_city = match.group(1).strip().title()
        destination_city = match.group(2).strip().title()

    # Look for date patterns
    date_patterns = [
        r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
        r'(\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})',  # 30th September 2025
        r'(\w+\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4})'  # September 30th, 2025
    ]

    for pattern in date_patterns:
        date_match = re.search(pattern, text)
        if date_match:
            travel_date = date_match.group(1)
            break

    return departure_city, destination_city, travel_date

def parse_function_call_from_text(text):
    """Parse function call from text if model outputs it as text instead of tool call"""
    import re

    # Look for get_ticket_price function calls in text
    pattern = r'get_ticket_price\s*\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']\s*\)'
    match = re.search(pattern, text)

    if match:
        departure_city = match.group(1)
        destination_city = match.group(2)
        travel_date = match.group(3)
        print(f"🔍 Detected function call in text: departure='{departure_city}', destination='{destination_city}', date='{travel_date}'")
        return get_ticket_price(departure_city, destination_city, travel_date)

    return None

def contains_price_info(text):
    """Check if the response contains price information without using tools"""
    import re
    price_patterns = [
        r'\$\d+',  # $250
        r'₹\d+',   # ₹250
        r'\d+\s*dollars?',  # 250 dollars
        r'\d+\s*rupees?',   # 250 rupees
    ]

    return any(re.search(pattern, text, re.IGNORECASE) for pattern in price_patterns)

def handle_tool_call(message):
    """Handle function tool calls"""
    print(f"🛠️ Handling tool call: {message.tool_calls}")

    if not message.tool_calls:
        print("❌ No tool calls found in message")
        return None

    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)

    departure_city = arguments.get('departure_city')
    destination_city = arguments.get('destination_city')
    travel_date = arguments.get('travel_date')

    print(f"📨 Extracted parameters: departure='{departure_city}', destination='{destination_city}', date='{travel_date}'")

    price_response = get_ticket_price(departure_city, destination_city, travel_date)

    tool_response = {
        "role": "tool",
        "content": price_response,
        "tool_call_id": tool_call.id
    }
    return tool_response

system_message = """You are a helpful assistant for an Airline called FlightAI.
Give short, courteous answers, no more than 1-2 sentences.
Always be accurate. If you don't know the answer, say so.

CRITICAL: When customers ask about ticket prices, you MUST ALWAYS use the get_ticket_price function.
DO NOT make up prices or guess. ONLY provide prices by calling the get_ticket_price function.

To call the function, you need:
- departure_city: where they're flying from
- destination_city: where they're flying to
- travel_date: their travel date in YYYY-MM-DD format

If they don't provide all three pieces of information, ask them for the missing details.
We serve routes between Chandigarh, Delhi, Mumbai, and Bangalore.

NEVER provide a price without calling the get_ticket_price function first."""

def Chat(message, history):
    """Main chat function with tool calling"""
    print(f"\n=== NEW MESSAGE ===")
    print(f"📩 User: {message}")
    
    # Convert Gradio history format to OpenAI format
    openai_history = []
    for human_msg, ai_msg in history:
        openai_history.append({"role": "user", "content": human_msg})
        openai_history.append({"role": "assistant", "content": ai_msg})
    
    # Build messages list
    messages = [
        {"role": "system", "content": system_message},
        *openai_history,
        {"role": "user", "content": message}
    ]
    
    print("📤 Sending messages to API...")
    
    try:
        # First API call - with tools enabled
        response = shivaay_via_openai.chat.completions.create(
            model="shivaay",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # Explicitly enable tool choice
            max_tokens=300
        )
        
        message_response = response.choices[0].message
        finish_reason = response.choices[0].finish_reason
        
        print(f"✅ API Response - Finish reason: {finish_reason}")
        print(f"📝 Message content: {message_response.content}")
        print(f"🔧 Tool calls: {message_response.tool_calls}")
        
        # Check if tool calling is required
        if finish_reason == "tool_calls" and message_response.tool_calls:
            print("🔄 Tool call detected! Processing...")
            
            # Add the assistant's tool call request to messages
            messages.append({
                "role": "assistant",
                "content": message_response.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    } for tool_call in message_response.tool_calls
                ]
            })
            
            # Handle the tool call and get the response
            tool_response = handle_tool_call(message_response)
            if tool_response:
                messages.append(tool_response)
                
                print("📤 Sending tool response back to API...")
                
                # Second API call - send the tool response back to the model
                second_response = shivaay_via_openai.chat.completions.create(
                    model="shivaay",
                    messages=messages,
                    tools=tools,  # Keep tools available
                    max_tokens=300
                )
                
                final_response = second_response.choices[0].message.content
                print(f"🎯 Final response: {final_response}")
                return final_response
            else:
                return "I encountered an error processing your request."
        
        # If no tool calls, check if this was a price request that should have used tools
        final_response = message_response.content

        # Check if user asked for price but model didn't use tools
        if detect_price_request(message) and not message_response.tool_calls:
            print("🚨 Price request detected but no tool calls made!")

            # Try to parse function call from text as fallback
            if final_response and "get_ticket_price" in final_response:
                print("🔄 Attempting to parse function call from text...")
                function_result = parse_function_call_from_text(final_response)
                if function_result:
                    print(f"✅ Successfully parsed and executed function call")
                    return function_result

            # Check if model provided price without using tools (hallucination)
            if contains_price_info(final_response):
                print("⚠️ Model provided price without using tools - attempting to extract info and call function")
                departure, destination, date = extract_travel_info(message)

                if departure and destination and date:
                    print(f"🔧 Extracted info: {departure} -> {destination} on {date}")
                    actual_price = get_ticket_price(departure, destination, date)
                    return actual_price
                else:
                    return "I need to check our system for accurate pricing. Could you please specify your departure city, destination city, and travel date?"

        print(f"🎯 Direct response: {final_response}")
        return final_response if final_response else "I don't have a response for that."
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return f"I'm having trouble connecting to the service. Error: {str(e)}"

# Test function to verify tool calling works
def test_tool_calling():
    """Test if tool calling works with specific prompts"""
    test_prompts = [
        "How much is a ticket from Chandigarh to Mumbai on 2025-09-30?",
        "What's the price for a flight from Delhi to Bangalore on 2025-10-15?",
        "Tell me the cost of a ticket from Mumbai to Delhi on 2025-11-01",
        "I want to know the fare from Chandigarh to Bangalore on 2025-12-25"
    ]

    for prompt in test_prompts:
        print(f"\n🧪 Testing: {prompt}")
        try:
            response = shivaay_via_openai.chat.completions.create(
                model="shivaay",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                tools=tools,
                tool_choice="auto",
                max_tokens=100
            )

            finish_reason = response.choices[0].finish_reason
            tool_calls = response.choices[0].message.tool_calls
            content = response.choices[0].message.content

            print(f"   Finish reason: {finish_reason}")
            print(f"   Content: {content}")
            print(f"   Tool calls: {bool(tool_calls)}")
            if tool_calls:
                print(f"   Function called: {tool_calls[0].function.name}")
                print(f"   Arguments: {tool_calls[0].function.arguments}")

        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    print("🔍 Testing tool calling support...")
    test_tool_calling()
    
    print("\n" + "="*50)
    print("🚀 Starting Gradio interface...")
    
    demo = gr.ChatInterface(
        fn=Chat,
        title="✈️ FlightAI Assistant with Tool Calling",
        description="Ask me about ticket prices! I can check prices between Chandigarh, Delhi, Mumbai, and Bangalore. Please provide departure city, destination city, and travel date.",
        examples=[
            "How much is a ticket from Chandigarh to Mumbai on 2025-09-30?",
            "What's the price from Delhi to Bangalore on 2025-10-15?",
            "Tell me the cost from Mumbai to Delhi on 2025-11-01"
        ],
        theme="soft"
    )
    
    demo.launch(share=True, inbrowser=True)