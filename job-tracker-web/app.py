import os 
import psycopg2
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token 
import bcrypt 

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "changethislater")
jwt = JWTManager(app)

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        dbname=os.environ.get("DB_NAME", "jobtracker"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres")
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS applications(
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(100),
        date_submitted DATE,
        company_name VARCHAR(100),
        job_title VARCHAR(100),
        salary VARCHAR(50),
        response VARCHAR(50)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def init_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        """, (data["username"], data["password"]))
        conn.commit()
        return jsonify({"message": "User created."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = %s",
            (data["username"],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and bcrypt.checkpw(data["password"].encode("utf-8"), user[1].encode("utf-8")):  
        token = create_access_token(identity=str(user[0]))
        return jsonify({"access_token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/applications", methods=["GET"])
@jwt_required()
def get_applications():
    user_id = get_jwt_identity()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, date_submitted, company_name, job_title, salary, response
        FROM applications
        WHERE user_id = %s
        ORDER BY date_submitted DESC
        """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        "id": r[0],
        "date_submitted": str(r[1]),
        "company_name": r[2],
        "job_title": r[3],
        "salary": r[4],
        "response": r[5]
    }for r in rows])

@app.route("/applications", methods=["POST"])
@jwt_required()
def add_application():
    user_id = get_jwt_identity()
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
            INSERT INTO applications (user_id, date_submitted, company_name, job_title, salary, response)
            VALUES (%s, CURRENT_DATE, %s, %s, %s, %s)
            """, (user_id, data["company_name"], data["job_title"], data["salary"], data["response"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Application added."}), 201

@app.route("/applications/<int:app_id>", methods=["PUT"])
@jwt_required()
def update_application(app_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
            UPDATE applications
            SET response = %s
            WHERE id = %s AND user_id = %s
        """, (data["response"], app_id, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Status updated."})

@app.route("/applications/<int:app_id>", methods=["DELETE"])
@jwt_required()
def delete_application(app_id):
    user_id = get_jwt_identity()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
            DELETE FROM applications 
            WHERE id = %s AND user_id = %s
            """, (app_id, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Application deleted."})

if __name__ == "__main__":
    init_db()
    init_users()
    app.run(host="0.0.0.0", port=5000, debug=True)