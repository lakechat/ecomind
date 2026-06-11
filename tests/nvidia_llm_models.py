import requests
api_key = "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"
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get("https://integrate.api.nvidia.com/v1/models", headers=headers)
for model in response.json()["data"]:
    print(model["id"])