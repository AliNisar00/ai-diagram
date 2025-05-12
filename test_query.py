import requests
import base64

def query_llava(prompt, image_path):
    # Load and encode image to base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Send request to Ollama
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llava:7b",
        "prompt": prompt,
        "images": [encoded_image],
        "stream": False
    })

    # Handle response
    response.raise_for_status()
    return response.json()['response']

# Test usage
result = query_llava("What is in this image?", "sample_image2.jpg")
print("Response from LLaVA:", result)
