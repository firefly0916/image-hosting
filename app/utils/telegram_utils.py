import os
import requests
from dotenv import load_dotenv
load_dotenv(".env")

class TelegramBot:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = f'https://api.telegram.org/bot{self.bot_token}'

    def send_file_to_telegram(self, file_stream) -> tuple:
        """
        Upload a file to Telegram and return its file_id, file name, file_url, and message_id.
        :param file_stream: A file-like object (e.g., opened in binary mode).
        :return: A tuple containing (file_id, file_name, file_url, message_id).
        """
        if not file_stream or not hasattr(file_stream, 'read'):
            raise ValueError("Invalid file stream provided.")

        url = f'{self.base_url}/sendDocument'
        files = {'document': file_stream}
        data = {'chat_id': self.get_chat_id()}
        response = requests.post(url, files=files, data=data)
        result = response.json()
        if not result.get('ok'):
            raise Exception(f"Upload failed: {result}")
        doc = result['result'].get('document')
        if not doc:
            raise Exception(f"Document info missing: {result}")
        file_id = doc['file_id']
        message_id = result['result'].get('message_id')
        ret_url = self.get_file_url(file_id)  # Ensure the file is uploaded and we can get its URL
        print(f"[✓] File uploaded successfully: {file_id}")
        print(f"[✓] File name: {doc.get('file_name', 'unknown')}")
        print(f"[✓] File URL: {ret_url}")
        print(f"[✓] Message ID: {message_id}")
        return file_id, doc.get('file_name', 'unknown'), ret_url, message_id

    def get_file_url(self, file_id):
        url = f'{self.base_url}/getFile?file_id={file_id}'
        response = requests.get(url)
        result = response.json()
        if not result.get('ok'):
            raise Exception(f"Get file info failed: {result}")
        file_path = result['result']['file_path']
        return f'https://api.telegram.org/file/bot{self.bot_token}/{file_path}'

    def get_chat_id(self):
        url = f'{self.base_url}/getUpdates'
        response = requests.get(url)
        result = response.json()

        if not result.get('ok') or not result.get('result'):
            raise Exception(f"[x] Get chat_id fail: {result}")

        latest_message = result['result'][-1]['message']
        chat_id = latest_message['chat']['id']
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