from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

correct_answers = {
    "question1":"a",
    "question2":"c",
    "question3":"a",
    "question4":"c"
}

def get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']
    
def get_best_score(ip_address):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()

    c.execute("SELECT best_score FROM users WHERE ip_address = ?", (ip_address,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    else:
        return None
    
def update_best_score(ip_address,score):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (ip_address, best_score)
                 VALUES (?, ?)
                 ON CONFLICT(ip_address) DO UPDATE SET best_score = max(best_score, ?)''', 
              (ip_address, score, score))
    
    conn.commit()
    conn.close()
    

@app.route("/")
def quiz_page():
    ip_address = get_ip()
    best_score = get_best_score(ip_address)
    return render_template("quiz.html", best_score = best_score)

@app.route('/submit',methods=['POST'])
def submit():
    score = 0
    total_questions = len(correct_answers)
    ip_address = get_ip()

    for question,correct_answer in correct_answers.items():
        user_answer = request.form.get(question)
        if user_answer == correct_answer:
            score += 25
    update_best_score(ip_address, score)
    best_score = get_best_score(ip_address)
    return render_template('quiz.html',score=score, best_score = best_score)
if __name__ == "__main__":
    app.run(debug = True)