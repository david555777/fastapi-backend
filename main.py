from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

app = FastAPI()

# Настройка CORS — замени на адрес своего фронтенда (например, https://ai-instagram-helper.vercel.app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Лучше: ["https://ai-instagram-helper.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_image(image: UploadFile = File(...)) -> Dict[str, str]:
    # Здесь можно сделать обработку изображения или использовать AI
    contents = await image.read()

    # Пример простого анализа (заглушка)
    # В реальности тут должен быть вызов OpenAI или другой логики
    return {
        "caption": "🌟 Загружено успешно! Вот ваш AI-сгенерированный текст.",
        "hashtags": "#ai #instagram #fastapi #photo #awesome"
    }
