from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем CORS для твоего фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # лучше указать домен Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend работает"}

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    # Здесь будет логика обработки с OpenAI
    contents = await file.read()
    # Пример ответа
    return {"caption": "AI сгенерировал описание", "hashtags": ["#ai", "#instagram"]}
