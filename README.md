# AI Logo Generator

## About
This is an AI-powered logo generation service using a LoRA fine-tuned Stable Diffusion model. The model is deployed on **Render** and accessible via FastAPI and Gradio.

## Live Demo
- Note :- This will not load / can give 502 Bad Gateway error wait for 30-50 sec then reload you can able to access it.
- Try it out here: [AI Logo Generator](https://ai-logo-lora-sdv1-5.onrender.com)

## Important Note
- The API has **limited free calls**, so the website may not always produce the desired output.
- If the model fails to generate an image, it may be due to **exhausted inference credits**.
- **Render's free tier suspends the service after 15 minutes of inactivity**. If the service is suspended and receives a request, it will **wake up with a cold start delay (~30+ seconds)** before responding.

## Usage
1. Visit the **Live Demo** link.
2. Enter a prompt describing the logo you want.
3. Click **Submit** to generate the logo.

## API Endpoint
You can also use the API directly:
```bash
GET https://ai-logo-lora-sdv1-5.onrender.com/generate/{prompt}
```
Example:
```bash
GET https://ai-logo-lora-sdv1-5.onrender.com/generate/aeroplane-blue-logo
```

## Running Locally
To run this project locally, clone the repo and install dependencies:
```bash
git clone https://github.com/prem357180/Ai-Logo-Lora-SDV1_5.git
cd Ai-Logo-Lora-SDV1_5
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

---
If you find this useful, consider **starring** ⭐ the repo!

