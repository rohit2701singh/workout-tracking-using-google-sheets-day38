import os
import requests
from datetime import datetime

APP_ID = os.environ.get("APP_ID_NUTRITIONIX")
API_KEY = os.environ.get("API_KEY_NUTRITIONIX")
SHEETY_AUTH_TOKEN = "Bearer roxxxxxxxxxxxgh"
SHEETY_API = "https://api.sheety.co/xxxxxxxxxxxxxxa/workoutTracking/workouts"

# ----------using nutritionix api--------------

exercise_endpoint = " https://trackapi.nutritionix.com/v2/natural/exercise"
header_nutritionix = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_input = input("Tell me which exercises you did (e.g. 20 km cycling, 30 km running, 50 pushup): ")
params = {
    "query": exercise_input,
    "gender": "male",
    "weight_kg": 56,
    "height_cm": 158,
    "age": 24,
}

response = requests.post(url=exercise_endpoint, json=params, headers=header_nutritionix)
nutrition_data = response.json()
print(nutrition_data)

# ----------using sheets api--------------

header_sheety = {
    "Authorization": SHEETY_AUTH_TOKEN,
    "Content-Type": "application/json"     # do not forget this
}

for exercise in nutrition_data["exercises"]:
    new_row_entry = {
        "workout": {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "exercise": exercise["user_input"].title(),
            "duration": exercise["duration_min"],   # 20 km cycling converted into possible time taken: 50 minutes
            "calories": exercise["nf_calories"],
        }
    }
    post_response = requests.post(url=SHEETY_API, json=new_row_entry, headers=header_sheety)
    # print(post_response.text)

get_response = requests.get(url=SHEETY_API, headers=header_sheety)
data = get_response.json()
# print(data)
