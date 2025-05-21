import base64
import openai
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Подставь адрес фронта в проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_image(image: UploadFile = File(...)) -> Dict[str, str]:
    contents = await image.read()
    base64_image = base64.b64encode(contents).decode("utf-8")

    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": "Что изображено на этом фото? Сгенерируй короткий caption и хештеги на русском." },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    result = response.choices[0].message.content

    # Можно выделить caption и хештеги отдельно
    return {
        "caption": result,
        "hashtags": ""  # Либо выдели через регулярку, если надо отдельно
    }
