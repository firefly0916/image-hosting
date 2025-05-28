import os
import requests
from dotenv import load_dotenv
load_dotenv(".env")

class TelegramBot:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = f'https://api.telegram.org/bot{self.bot_token}'

    def send_file_to_telegram(self, file_stream, file_name=None) -> tuple:
        """
        Upload a file to Telegram and return its file_id, file name, file_url, and message_id.
        :param file_stream: A file-like object (e.g., opened in binary mode).
        :param file_name: The original file name from the user upload.
        :return: A tuple containing (file_id, file_name, file_url, message_id).
        """
        if not file_stream or not hasattr(file_stream, 'read'):
            raise ValueError("Invalid file stream provided.")

        # Use provided file_name or fallback to file_stream.name
        if not file_name:
            file_name = getattr(file_stream, 'name', 'unknown')
        if not file_name or file_name == 'unknown':
            raise ValueError("File stream must have a valid 'name' attribute or file_name parameter.")
        print(f"[INFO] File name: {file_name}")
        url = f'{self.base_url}/sendDocument'
        files = {'document': (file_name, file_stream)}
        data = {'chat_id': self.get_chat_id()}
        response = requests.post(url, files=files, data=data)
        result = response.json()
        if not result.get('ok'):
            raise Exception(f"Upload failed: {result}")
        doc = result['result'].get('document')
        if doc:
            file_id = doc['file_id']
            file_name_return = doc.get('file_name', file_name)
        else:
            # 兼容 sticker 类型
            sticker = result['result'].get('sticker')
            if sticker:
                file_id = sticker['file_id']
                # 优先用传入的 file_name（即用户原始文件名），否则 fallback
                file_name_return = file_name if file_name else f"sticker_{file_id}.webp"
            else:
                raise Exception(f"Document info missing: {result}")
        message_id = result['result'].get('message_id')
        ret_url = self.get_file_url(file_id)
        print(f"[✓] File uploaded successfully: {file_id}")
        print(f"[✓] File name: {file_name_return}")
        print(f"[✓] File URL: {ret_url}")
        print(f"[✓] Message ID: {message_id}")
        return file_id, file_name_return, ret_url, message_id

    def get_file_url(self, file_id):
        url = f'{self.base_url}/getFile?file_id={file_id}'
        response = requests.get(url)
        result = response.json()
        if not result.get('ok'):
            raise Exception(f"Get file info failed: {result}")
        file_path = result['result']['file_path']
        return f'https://api.telegram.org/file/bot{self.bot_token}/{file_path}'

    def get_chat_id(self):
        chat_id = os.getenv('TG_CHAT_ID')
        if not chat_id:
            raise ValueError("TG_CHAT_ID is not set in environment variables.")
        print(f"[✓] Get chat_id: {chat_id}")
        return chat_id

    def delete_message(self, chat_id, message_id):
        url = f'{self.base_url}/deleteMessage'
        data = {'chat_id': chat_id, 'message_id': message_id}
        response = requests.post(url, data=data)
        result = response.json()
        if not result.get('ok'):
            raise Exception(f"Delete message failed: {result}")
        return True

# Example usage:
# bot = TelegramBot(TG_BOT_TOKEN)
# bot.send_file_to_telegram('path/to/file')
if __name__ == "__main__":
    TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
    if not TG_BOT_TOKEN:
        raise ValueError("TG_BOT_TOKEN is not set in environment variables.")
    else:
        print(f"[INFO] TG_BOT_TOKEN is set. {TG_BOT_TOKEN}")
    bot = TelegramBot(TG_BOT_TOKEN)
    bot.send_file_to_telegram(open('README.md', 'rb'))
    print("Telegram bot initialized successfully.")