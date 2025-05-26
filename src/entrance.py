import os
import requests
import sqlite3
from flask import Flask, request, jsonify, render_template

current_dir = os.path.dirname(os.path.abspath(__file__))

template_dir = os.path.abspath(os.path.join(current_dir, '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

TG_BOT_TOKEN = '8011530044:AAGCl0SIGzX5N2paXH2xHvCmzDUCJj3U9To'
TG_CHAT_ID = ''
DB_PATH = os.path.join(current_dir, 'images.db')
IMG_DIR = os.path.join(current_dir, 'img')
os.makedirs(IMG_DIR, exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT NOT NULL,
            file_url TEXT NOT NULL,
            upload_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')

def get_latest_chat_id():
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates'
    response = requests.get(url)
    result = response.json()

    if not result.get('ok') or not result.get('result'):
        raise Exception(f"[x] Get chat_id fail: {result}")

    latest_message = result['result'][-1]['message']
    chat_id = latest_message['chat']['id']
    print(f"[✓] Get chat_id: {chat_id}")
    return chat_id


def upload_file(file_stream, filename, chat_id):
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendDocument'
    files = {'document': (filename, file_stream)}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    result = response.json()

    if not result.get('ok'):
        raise Exception(f"[x] Upload file fail: {result}")

    result_data = result['result']
    if 'document' in result_data:
        file_info = result_data['document']
    else:
        raise Exception(f"Document info not found in response: {result}")

    file_id = file_info['file_id']
    file_name = file_info.get('file_name', filename)
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


def save_image_to_db(file_id, file_url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO images (file_id, file_url) VALUES (?, ?)', (file_id, file_url))
    conn.commit()
    conn.close()


@app.route('/upload', methods=['POST'])
def upload_endpoint():
    global TG_CHAT_ID
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Empty filename'}), 400

    if not TG_CHAT_ID:
        try:
            TG_CHAT_ID = get_latest_chat_id()
        except Exception as e:
            return jsonify({'success': False, 'error': f'Failed to get chat_id: {str(e)}'}), 500

    try:
        file_id, file_name = upload_file(file.stream, file.filename, TG_CHAT_ID)
        file_url = get_file_url(file_id)
        save_image_to_db(file_id, file_url)
        return jsonify({'success': True, 'file_url': file_url})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
