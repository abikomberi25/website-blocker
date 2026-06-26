import sqlite3

conn = sqlite3.connect("block_log.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM actions")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()