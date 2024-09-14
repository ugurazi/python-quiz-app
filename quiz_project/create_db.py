import sqlite3

def create_db():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
              (ip_address TEXT PRIMARY KEY, best_score REAL)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
