import requests
import gradio as gr
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from dotenv import load_dotenv
import os
from io import BytesIO
from PIL import Image

# Load environment variables
load_dotenv()

# Hugging Face API settings
API_TOKEN = os.getenv("API_KEY")
MODEL_URL = "https://api-inference.huggingface.co/models/Shakker-Labs/FLUX.1-dev-LoRA-Logo-Design"

headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}

# Initialize FastAPI
app = FastAPI()

# Function to generate logo using Hugging Face API
def generate_logo(prompt):
    payload = {"inputs": prompt + " logo"}
    
    try:
        response = requests.post(MODEL_URL, headers=headers, json=payload, timeout=30)
        
        # Check for valid response
        if response.status_code != 200:
            return None, f"Error: {response.status_code} - {response.text}"

        # Try to parse JSON response
        try:
            data = response.json()
            if not isinstance(data, list) or "generated_image_url" not in data[0]:
                return None, "Invalid API response format."
            
            image_url = data[0]['generated_image_url']
            image_response = requests.get(image_url, timeout=30)

            if image_response.status_code == 200:
                image = Image.open(BytesIO(image_response.content))
                file_path = "generated_logo.png"
                image.save(file_path)
                return file_path, None
            else:
                return None, f"Failed to download image. Status: {image_response.status_code}"

        except requests.exceptions.JSONDecodeError:
            return None, "API returned invalid JSON."

    except requests.exceptions.RequestException as e:
        return None, f"Request failed: {str(e)}"

# FastAPI endpoint for API access
@app.get("/generate/{prompt}")
def generate_api(prompt: str):
    file_path, error = generate_logo(prompt)
    if file_path:
        return FileResponse(file_path, media_type="image/png")
    return {"error": error}

# Gradio UI function
def gradio_ui(prompt):
    file_path, error = generate_logo(prompt)
    if file_path:
        return Image.open(file_path)
    return f"Error: {error}"

# Launch Gradio Interface
gr_interface = gr.Interface(fn=gradio_ui, inputs="text", outputs="image", title="AI Logo Generator")

# Serve Gradio with FastAPI
@app.get("/")
def home():
    return RedirectResponse(url="/gradio")

app = gr.mount_gradio_app(app, gr_interface, path="/gradio")
