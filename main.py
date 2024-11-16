from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from actions import get_weather

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

functions = [
    {
        "name": "get_weather",
        "description": "Get the weather information for a specific location and date.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get the weather for."
                },
                "date": {
                    "type": "string",
                    "description": "The date for the weather forecast, in YYYY-MM-DD format."
                }
            },
            "required": ["location", "date"]
        }
    }
]

def run():
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "What's the weather forecast for Paris today?"}],
        functions=functions,
        function_call="auto"
        )

    if response.choices[0].finish_reason == "function_call":
        function_call = response.choices[0].message.function_call
        arguments = json.loads(function_call.arguments)
        
    
        location = arguments['location']
        date = arguments['date']
        weather_info = get_weather(location, date)
        
        # Print or use the weather information
        print("Weather Info:", weather_info)
    else:
        # If no function call is made, print the model's response
        print("Response:", response.choices[0].message.content)