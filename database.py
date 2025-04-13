import sqlite3

# Connect to DB
def create_connection():
    conn = sqlite3.connect("logbook.db", check_same_thread=False)
    return conn

# Create table if not exists
def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logbook (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
        activity TEXT,
        status TEXT
    )''')
    conn.commit()
    conn.close()

# Insert data
def insert_log(date, time, activity, status):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO logbook (date, time, activity, status) VALUES (?, ?, ?, ?)",
              (date, time, activity, status))
    conn.commit()
    conn.close()

# Fetch all logs
def get_all_logs():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM logbook")
    data = c.fetchall()
    conn.close()
    return data

# Filter by date and/or status
def filter_logs(date=None, status=None):
    conn = create_connection()
    c = conn.cursor()
    query = "SELECT * FROM logbook WHERE 1=1"
    params = []

    if date:
        query += " AND date=?"
        params.append(date)
    if status:
        query += " AND status=?"
        params.append(status)

    c.execute(query, params)
    data = c.fetchall()
    conn.close()
    return data
