import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils.telegram_utils import TelegramBot
from app.db.database import Database
from dotenv import load_dotenv
from datetime import datetime
import uuid
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()

load_dotenv()
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
CUSTOM_DOMAIN = os.getenv('CUSTOM_DOMAIN', 'localhost')

tg_bot = TelegramBot(TG_BOT_TOKEN)
db = Database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请改成具体前端地址
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_id, file_name, url, message_id = tg_bot.send_file_to_telegram(file_stream=file.file)
        print(f"[INFO] File url: {url}")
        print(f"[INFO] Telegram file_id: {file_id}, file_name: {file_name}")

        # Extract current date information
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        # Generate UUID
        file_uuid = str(uuid.uuid4())

        custom_url = f"https://example.com/files/{year}/{month}/{day}/{file_uuid}"

        db.insert_file_record(file_name, url, year, month, day, file_uuid, custom_url, file_id, message_id)

        return {"message": "Upload successful", "url": url}
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"error": str(e)}

@app.get("/files")
def get_files():
    return db.get_all_records()

@app.get("/find/{year}/{month}/{day}/{uuid}")
def find_file_record(year: int, month: int, day: int, uuid: str):
    try:
        # Fetch the binary content of the file
        content = db.get_record_content(year, month, day, uuid)

        # Return the content as a streaming response
        return StreamingResponse(
            iter([content]),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={uuid}"}
        )
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"error": str(e)}
    

@app.delete("/files/{file_id}")
def delete_file(file_id: int):
    try:
        record = db.get_file_record(file_id)
        if not record:
            raise HTTPException(status_code=404, detail="File not found in database")
        # record: (id, filename, url, file_id, message_id, upload_time)
        tg_file_id = record[3]
        tg_message_id = record[4]
        chat_id = tg_bot.get_chat_id()
        if tg_message_id:
            try:
                tg_bot.delete_message(chat_id, tg_message_id)
            except Exception as e:
                print(f"[WARN] Telegram message delete failed: {e}")
        db.delete_file_record(file_id)
        return JSONResponse(content={"message": "Deleted (db+telegram)"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
