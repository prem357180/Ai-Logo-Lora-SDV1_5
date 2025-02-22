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
    response = requests.post(MODEL_URL, headers=headers, json=payload)

    if response.status_code == 200:
        # Hugging Face returns a JSON with an image URL
        image_url = response.json()[0]['generated_image_url']
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            image = Image.open(BytesIO(image_response.content))
            file_path = "generated_logo.png"
            image.save(file_path)
            return file_path
        else:
            return None
    else:
        return None

# FastAPI endpoint for API access
@app.get("/generate/{prompt}")
def generate_api(prompt: str):
    file_path = generate_logo(prompt)
    if file_path:
        return FileResponse(file_path, media_type="image/png")
    return {"error": "Failed to generate image"}

# Gradio UI function
def gradio_ui(prompt):
    file_path = generate_logo(prompt)
    if file_path:
        return Image.open(file_path)
    return None

# Launch Gradio Interface
gr_interface = gr.Interface(fn=gradio_ui, inputs="text", outputs="image", title="AI Logo Generator")

# Serve Gradio with FastAPI
@app.get("/")
def home():
    return RedirectResponse(url="/gradio")

app = gr.mount_gradio_app(app, gr_interface, path="/gradio")
