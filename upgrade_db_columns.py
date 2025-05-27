import sqlite3

# 路径根据你的实际情况调整
DB_PATH = 'app/db/db.db'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

try:
    c.execute('ALTER TABLE files ADD COLUMN file_id TEXT;')
    print('file_id 字段已添加')
except Exception as e:
    print('file_id 字段可能已存在:', e)

try:
    c.execute('ALTER TABLE files ADD COLUMN message_id TEXT;')
    print('message_id 字段已添加')
except Exception as e:
    print('message_id 字段可能已存在:', e)

conn.commit()
conn.close()
print('数据库结构升级完成')
