import requests
import os

TG_BOT_TOKEN = '8011530044:AAGCl0SIGzX5N2paXH2xHvCmzDUCJj3U9To' 

def send_file_to_telegram(file_path):
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendDocument'
    with open(file_path, 'rb') as f:
        files = {'document': f}
        data = {'chat_id': get_chat_id()}
        response = requests.post(url, files=files, data=data)
    result = response.json()
    if not result.get('ok'):
        raise Exception(f"Upload failed: {result}")
    doc = result['result'].get('document')
    if not doc:
        raise Exception(f"Document info missing: {result}")
    file_id = doc['file_id']
    return file_id, doc.get('file_name', 'unknown')

def get_file_url(file_id):
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/getFile?file_id={file_id}'
    response = requests.get(url)
    result = response.json()
    if not result.get('ok'):
        raise Exception(f"Get file info failed: {result}")
    file_path = result['result']['file_path']
    return f'https://api.telegram.org/file/bot{TG_BOT_TOKEN}/{file_path}'

def get_chat_id():
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates'
    response = requests.get(url)
    result = response.json()

    if not result.get('ok') or not result.get('result'):
        raise Exception(f"[x] Get chat_id fail: {result}")

    latest_message = result['result'][-1]['message']
    chat_id = latest_message['chat']['id']
    print(f"[✓] Get chat_id: {chat_id}")
    return chat_id
