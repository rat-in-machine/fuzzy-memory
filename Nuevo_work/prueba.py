import requests

url = "https://ia-research-dev.codingbuddy-4282826dce7d155229a320302e775459-0000.eu-de.containers.appdomain.cloud/research/llm/openai/clients"

data = {
    "model": "gpt-5",
    "uuid": "ips-dev-Imxp8Q2YtcJaReoSytJFbMnzgFmGF9W7",
    "message": {
        "role": "user",
        "content": "hi"
    },
    "prompt": None, # Prompt de sistema
    "temperature": 0,
    "language": "es",
    "user": "ips1216malaga@escuelaviewnextiadata2026.com"
}

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": "ips-dev-Imxp8Q2YtcJaReoSytJFbMnzgFmGF9W7"
}

try:
    with requests.post(url, json=data, headers=headers, stream=True) as response:
        response.raise_for_status()

        print("OPENAI response:")
        print(f"{response.json()}")

except requests.exceptions.RequestException as e:
    print("Error al realizar la solicitud:", e)