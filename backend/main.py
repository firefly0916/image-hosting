import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from telegram_utils import send_file_to_telegram, get_file_url
from database import insert_file_record, init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请改成具体前端地址
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists('temp'):
    os.makedirs('temp')

init_db()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    temp_path = os.path.join('temp', file.filename)
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    print(f"[INFO] Saved uploaded file to {temp_path}")

    try:
        file_id, file_name = send_file_to_telegram(temp_path)
        print(f"[INFO] Telegram file_id: {file_id}, file_name: {file_name}")

        url = get_file_url(file_id)
        print(f"[INFO] File url: {url}")

        insert_file_record(file_name, url)
        os.remove(temp_path)
        print(f"[INFO] Removed temp file {temp_path}")

        return {"message": "Upload successful", "url": url}
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"error": str(e)}
