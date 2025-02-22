import requests
import gradio as gr
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse

from dotenv import load_dotenv
import os

load_dotenv()

from io import BytesIO
from PIL import Image

# Hugging Face API settings
API_TOKEN = os.getenv("API_KEY")   
MODEL_URL = "https://api-inference.huggingface.co/models/Shakker-Labs/FLUX.1-dev-LoRA-Logo-Design"

headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}

# Initialize FastAPI
app = FastAPI()

# Function to generate logo using Hugging Face API
def generate_logo(prompt):
    payload = {"inputs": prompt+" logo"}
    response = requests.post(MODEL_URL, headers=headers, json=payload)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save("generated_logo.png")
        return "generated_logo.png"
    else:
        return f"Error: {response.text}"

# FastAPI endpoint for API access
@app.get("/generate/{prompt}")
def generate_api(prompt: str):
    file_path = generate_logo(prompt)
    return FileResponse(file_path, media_type="image/png")

# Gradio UI function
def gradio_ui(prompt):
    file_path = generate_logo(prompt)
    return Image.open(file_path)

# Launch Gradio Interface
gr_interface = gr.Interface(fn=gradio_ui, inputs="text", outputs="image", title="AI Logo Generator")

# Serve Gradio with FastAPI
@app.get("/")
def home():
    return RedirectResponse(url="/gradio")
app = gr.mount_gradio_app(app, gr_interface, path="/gradio")

# uvicorn app:app --host 127.0.0.1 --port 8000
