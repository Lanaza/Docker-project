import os
import time
import psycopg2
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "taskdb")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except psycopg2.OperationalError as e:
            retries -= 1
            time.sleep(2)
            if retries == 0:
                raise e

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id SERIAL PRIMARY KEY,
            page_url VARCHAR(255) NOT NULL,
            action_type VARCHAR(100) NOT NULL,
            user_agent TEXT,
            ip_address VARCHAR(45),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def log_interaction(page_url, action_type):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        user_agent = request.headers.get('User-Agent')
        ip_address = request.remote_addr
        cur.execute(
            'INSERT INTO interactions (page_url, action_type, user_agent, ip_address) VALUES (%s, %s, %s, %s);',
            (page_url, action_type, user_agent, ip_address)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erreur enregistrement interaction : {e}")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Mon Site Vitrine Client</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; }
        .card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px; margin: 0 auto; text-align: center; }
        button { background-color: #1F4E78; color: white; border: none; padding: 12px 24px; border-radius: 4px; cursor: pointer; margin: 10px 5px; font-size: 1rem; }
        button:hover { background-color: #2E75B6; }
        .status { margin-top: 20px; font-size: 0.9em; color: #28a745; font-weight: bold; display: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Bienvenue sur notre site client</h1>
        <p>Découvrez nos services ou contactez-nous directement ci-dessous.</p>
        
        <div>
            <button onclick="trackAction('clic_bouton_interet')">Je suis intéressé</button>
            <button onclick="trackAction('clic_bouton_contact')">Nous contacter</button>
        </div>

        <div id="confirmation" class="status">Action enregistrée en base de données !</div>
    </div>

    <script>
        function trackAction(action) {
            fetch('/api/track', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: action })
            }).then(() => {
                const msg = document.getElementById('confirmation');
                msg.style.display = 'block';
                setTimeout(() => { msg.style.display = 'none'; }, 2000);
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    init_db()
    log_interaction('/', 'page_view')
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/track', methods=['POST'])
def track():
    init_db()
    data = request.get_json() or {}
    action = data.get('action', 'unknown_action')
    log_interaction('/', action)
    return jsonify({"status": "success"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)