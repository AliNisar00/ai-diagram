import requests
import base64
import os

def query_llava(prompt, image_path, model_name="llava:7b", host="http://localhost:11434"):
    """
    Sends an image and prompt to the LLaVA model running via Ollama.
    
    :param prompt: Instructional text for LLaVA.
    :param image_path: Path to the image file.
    :param model_name: Model name served by Ollama.
    :param host: Base URL of the Ollama server.
    :return: Textual response from the model.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")
    
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    try:
        response = requests.post(
            f"{host}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "images": [encoded_image],
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()['response']
    except requests.RequestException as e:
        print(f"[Error] Failed to query LLaVA: {e}")
        return None

# Only run the following when executed directly (not on import)
if __name__ == "__main__":
    test_prompt = "What is in this image?"
    test_image = "test_image2.jpg"
    result = query_llava(test_prompt, test_image)
    if result:
        print("Response from LLaVA:", result)
