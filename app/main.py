import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.utils.telegram_utils import TelegramBot
from app.db.database import Database
from dotenv import load_dotenv
load_dotenv()

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

tg_bot = TelegramBot(TG_BOT_TOKEN)
db = Database()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请改成具体前端地址
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_id, file_name, url = tg_bot.send_file_to_telegram(file_stream=file.file)
        print(f"[INFO] File url: {url}")
        print(f"[INFO] Telegram file_id: {file_id}, file_name: {file_name}")

        db.insert_file_record(file_name, url)

        return {"message": "Upload successful", "url": url}
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"error": str(e)}
