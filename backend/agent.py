import requests
import json

def vc_scout(goal):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": goal
        },
        stream=True
    )

    result = ""

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            result += data.get("response", "")

    return result