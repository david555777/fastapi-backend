import base64
import openai
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# 👇  сюда свой фронтенд-домен
origins = [
    "https://ai-instagram-helper-git-main-ihor555s-projects.vercel.app",
    "http://localhost:3000",  # на случай локальной отладки
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 👈 тут список разрешённых доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_image(image: UploadFile = File(...)) -> Dict[str, str]:
    contents = await image.read()
    base64_image = base64.b64encode(contents).decode("utf-8")

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
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
        return {
            "caption": result,
            "hashtags": ""  # выделить отдельно
        }

    except Exception as e:
        return {"status": "error", "detail": str(e)}
