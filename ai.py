import requests
from typing import Optional
from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import json


load_dotenv()

BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "4cf128db-61c5-45ea-8695-3922a57bbbeb"


def ask_ai(question, profile):
    
    TWEAKS = {
    "TextInput-YGbVg": {
        "input_value": question
    },
    "TextInput-zaT4t": {
        "input_value": profile
    }
    }

    result = run_flow_from_json(flow="Ask AI.json",
                                input_value="message",
                                session_id="", # provide a session id if you want to use session state
                                fallback_to_env_vars=True, # False by default
                                tweaks=TWEAKS)
    return result[0].outputs[0].results["text"].data["text"]





def get_macros(profile, goals):
    TWEAKS = {
    "TextInput-iIo3v": {
        "input_value": goals
    },
    "TextInput-UZEh1": {
        "input_value": profile
    },

    }

    return run_flow("",tweaks=TWEAKS, endpoint=FLOW_ID)

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  api_key: Optional[str] = None) -> dict:
    
    api_url = f"{BASE_API_URL}/api/v1/run/macros"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]


# result = get_macros("height: 196 cm, weight: 81 kg, gender: male, very active", "gain muscles and loose belly fat ")
result2 = ask_ai("Make personalised plan for me based on my profile and goals",
                 "height: 196 cm, weight: 81 kg, gender: male, very active, goals: gain muscles and loose belly fat ")
# print(result)
print(result2)