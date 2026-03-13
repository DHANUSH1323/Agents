import requests
import json

ollama_url = "http://127.0.0.1:11434/api/chat"

def getWeather(city):
    data = {
        "Chennai": "20°C",
        "Mumbai": "25°C",
        "Delhi": "22°C",
        "Kolkata": "23°C",
        "Bangalore": "24°C",
        "Hyderabad": "26°C",
        "Ahmedabad": "27°C",
        "Jaipur": "28°C",
        "Lucknow": "29°C",
        "Pune": "30°C",
    }
    return data.get(city, "Unknown city")

tools = {
    "getWeather": getWeather
}

messages = [
    {
        "role": "system",
        "content": "You are an agent. If the user asks about weather, respond exactly in this format: CALL_TOOL:getWeather:<city>. Otherwise answer normally."
    },
    {
        "role": "user",
        "content": "Whats the weather in Chennai?"
    }
]

response = requests.post(
    ollama_url, 
    json={
        "model":"qwen2.5:3b",
        "messages":messages,
        "stream": False
    })

print("STATUS:", response.status_code)
print("RAW TEXT:")
print(response.text)
print("-" * 50)

data = response.json()
assistantResponse = response.json()["message"]["content"]
print("ASSISTANT RESPONSE:", assistantResponse)

if assistantResponse.startswith("CALL_TOOL:getWeather:"):
    city = assistantResponse.split(":", 2)[2].strip()
    result = getWeather(city)

    messages.append({"role": "assistant", "content": assistantResponse})
    messages.append({"role": "user", "content": f"Tool result: {result}. Answer the user using this result only."})

    final = requests.post(
        ollama_url,
        json={
            "model": "qwen2.5:3b",
            "messages": messages,
            "stream": False
        }
    )

    print("FINAL RAW TEXT:")
    print(final.text)
    print("-" * 50)

    final_data = final.json()
    print("FINAL ANSWER:", final_data["message"]["content"])
else:
    print("FINAL ANSWER:", assistantResponse)