from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
import os

app = Flask(__name__)
CORS(app)

DB = os.path.join(os.path.dirname(__file__), "database.db")


# ---------------- DATABASE CONNECTION ----------------
def get_db():
    return sqlite3.connect(DB)

# ---------------- CREATE TABLES ----------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT,
        score INTEGER,
        total INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recommendations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        level TEXT,
        recommended_topic TEXT,
        difficulty TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- ADD USER ----------------
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    name = data["name"]
    email = data["email"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name,email) VALUES (?,?)",(name,email))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()

    return jsonify({"user_id":user_id,"message":"User created"})


# ---------------- SUBMIT QUIZ ----------------
@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    data = request.json
    user_id = data["user_id"]
    topic = data["topic"]
    score = int(data["score"])
    total = int(data["total"])

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO quiz_attempts(user_id,topic,score,total) VALUES (?,?,?,?)",
        (user_id,topic,score,total)
    )
    conn.commit()
    conn.close()

    return jsonify({"message":"Quiz stored successfully"})


# ---------------- VIEW PROGRESS ----------------
@app.route("/progress/<int:user_id>", methods=["GET"])
def progress(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT topic,score,total,date FROM quiz_attempts WHERE user_id=?",(user_id,))
    rows = cur.fetchall()
    conn.close()

    result=[]
    for r in rows:
        percent = (r[1]/r[2])*100
        result.append({
            "topic":r[0],
            "score":r[1],
            "total":r[2],
            "percentage":round(percent,2),
            "date":r[3]
        })

    return jsonify(result)


# ---------------- ML RECOMMENDATION ----------------
def get_student_data(user_id):
    conn = get_db()
    df = pd.read_sql_query(f"SELECT score,total FROM quiz_attempts WHERE user_id={user_id}",conn)
    conn.close()

    if df.empty:
        return None

    df["percentage"] = (df["score"]/df["total"])*100
    return df


def get_level(df):
    X = df[["percentage"]]

   
    if len(X) < 3:
        avg = X["percentage"].mean()
    else:
        kmeans = KMeans(n_clusters=3, random_state=0)
        kmeans.fit(X)
        avg = X["percentage"].mean()

    if avg < 40:
        return "Beginner"
    elif avg < 75:
        return "Intermediate"
    else:
        return "Advanced"


@app.route("/recommend/<int:user_id>", methods=["GET"])
def recommend(user_id):
    df = get_student_data(user_id)

    if df is None:
        return jsonify({"msg":"No quiz data available"})

    level = get_level(df)

    # recommendation logic
    if level == "Beginner":
        topic = "Python Basics"
        difficulty = "Decrease"
    elif level == "Intermediate":
        topic = "Data Structures"
        difficulty = "Maintain"
    else:
        topic = "Neural Networks Basics"
        difficulty = "Increase"

    # store history
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO recommendations(user_id,level,recommended_topic,difficulty)
        VALUES (?,?,?,?)
    """,(user_id,level,topic,difficulty))
    conn.commit()
    conn.close()

    return jsonify({
        "student_id":user_id,
        "current_level":level,
        "recommended_topic":topic,
        "difficulty_adjustment":difficulty
    })


# ---------------- ALL STUDENTS ----------------
@app.route("/all_users")
def all_users():
    conn=get_db()
    cur=conn.cursor()
    cur.execute("SELECT * FROM users")
    data=cur.fetchall()
    conn.close()
    return jsonify(data)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
