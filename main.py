from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class BioRequest(BaseModel):
    name: str
    profession: str
    experience: str
    tone: str
    style_notes: str

@app.post("/generate")
def generate_bio(req: BioRequest):
    prompt = f"""
    Create a compelling and personalized freelancer bio using the following information:
    Name: {req.name}
    Profession: {req.profession}
    Experience: {req.experience}
    Tone: {req.tone}
    Additional Notes: {req.style_notes}
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://huggingface.co/spaces/your-username/bio",
        "X-Title": "Freelancer AI Bio Generator"
    }

    json_data = {
        "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that writes great freelancer bios."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=json_data)

    if response.status_code == 200:
        return {"bio": response.json()["choices"][0]["message"]["content"]}
    else:
        return {"error": response.text}
