import requests
import os

current_dir = os.path.dirname(__file__) 
img_path = os.path.join(current_dir, 'img', 'top.jpg') 
tg_bot_token = '8011530044:AAGCl0SIGzX5N2paXH2xHvCmzDUCJj3U9To'

TG_BOT_TOKEN = tg_bot_token  
TG_CHAT_ID = ''
FILE_PATH = img_path


def get_latest_chat_id():
    """Get chat_id"""
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates'
    response = requests.get(url)
    result = response.json()

    if not result.get('ok') or not result.get('result'):
        raise Exception(f"[x] Get chat_id fail: {result}")

    latest_message = result['result'][-1]['message']
    chat_id = latest_message['chat']['id']
    print(f"[✓] Get chat_id: {chat_id}")
    return chat_id


def upload_file(file_path, chat_id):
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendDocument'
    files = {'document': open(file_path, 'rb')}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    result = response.json()

    if not result.get('ok'):
        raise Exception(f"[x] Upload file fail: {result}")

    # file_id = result['result']['document']['file_id']
    result_data = result['result']
    if 'document' in result_data:
        file_info = result_data['document']
    else:
        raise Exception(f"Document info is not exist :r{result}")

    file_id = file_info['file_id']
    file_name = result['result']['document'].get('file_name', 'unknown')
    print(f"[✓] Upload file success, file_id: {file_id}")
    return file_id, file_name


def get_file_url(file_id):
    get_file_url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/getFile?file_id={file_id}'
    response = requests.get(get_file_url)
    result = response.json()

    if not result.get('ok'):
        raise Exception(f"[x] Get file_path fail: {result}")

    file_path = result['result']['file_path']
    file_url = f'https://api.telegram.org/file/bot{TG_BOT_TOKEN}/{file_path}'
    return file_url


if __name__ == '__main__':
    if not TG_BOT_TOKEN:
        raise Exception("Please set TG_BOT_TOKEN")

    if not TG_CHAT_ID:
        TG_CHAT_ID = get_latest_chat_id()

    file_id, file_name = upload_file(FILE_PATH, TG_CHAT_ID)
    file_url = get_file_url(file_id)
    print(f"[✓] File url:\n{file_url}")
