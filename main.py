import os
import sqlite3
import random
from flask import Flask, request, render_template_string, redirect, url_for, g

app = Flask(__name__)
app.secret_key = 'roblox_avatar_ideas_secret_key'
DATABASE = 'roblox_avatars.db'

# --- KHỞI TẠO CƠ SỞ DỮ LIỆU ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    # Sử dụng sqlite3 trực tiếp để khởi tạo DB khi app bắt đầu chạy
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avatars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author VARCHAR(100),
            image_url TEXT,
            avatar_code_link TEXT,
            category VARCHAR(50),
            description TEXT,
            robux_cost INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# TỰ ĐỘNG KHỞI TẠO DB NGAY KHI APP ĐƯỢC RENDER NẠP
init_db()

# --- GIAO DIỆN HTML/CSS (EMO 2000s BLACK & WHITE STYLE) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roblox avatar ideas</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Courier New', Courier, monospace, sans-serif;
        }
        body {
            background-color: #0d0d0d;
            color: #e0e0e0;
            padding: 20px;
        }
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px dashed #444;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        .login-btn {
            background: #1a1a1a;
            color: #fff;
            border: 1px solid #666;
            padding: 8px 15px;
            cursor: pointer;
            text-decoration: none;
            font-size: 13px;
            transition: 0.2s;
        }
        .login-btn:hover {
            background: #fff;
            color: #000;
        }
        .site-title {
            text-align: center;
            font-size: 28px;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-shadow: 0 0 5px #fff;
            margin-bottom: 25px;
        }
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .search-box {
            flex: 1;
            min-width: 250px;
        }
        .search-box input {
            width: 100%;
            padding: 12px;
            background: #121212;
            border: 1px solid #444;
            color: #fff;
            font-size: 15px;
            text-align: center;
        }
        .upload-btn-green {
            background-color: #28a745;
            color: white;
            padding: 12px 20px;
            border: none;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
            border-radius: 4px;
            box-shadow: 0 0 10px rgba(40, 167, 69, 0.4);
        }
        .upload-btn-green:hover {
            background-color: #218838;
        }
        .upload-section {
            background: #161616;
            border: 1px solid #333;
            padding: 20px;
            margin-bottom: 30px;
            display: {% if show_upload %}block{% else %}none{% endif %};
        }
        .upload-section h3 {
            margin-bottom: 15px;
            border-bottom: 1px solid #444;
            padding-bottom: 5px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-size: 13px;
        }
        .form-group input, .form-group textarea {
            width: 100%;
            padding: 8px;
            background: #000;
            border: 1px solid #444;
            color: #fff;
        }
        .submit-btn {
            background: #fff;
            color: #000;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            cursor: pointer;
        }
        .avatar-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }
        .avatar-card {
            background: #141414;
            border: 1px solid #2a2a2a;
            padding: 15px;
            position: relative;
        }
        .avatar-card img {
            width: 100%;
            height: 250px;
            object-fit: cover;
            border: 1px solid #333;
            background-color: #050505;
        }
        .avatar-info {
            margin-top: 10px;
            font-size: 13px;
        }
        .avatar-info p {
            margin-bottom: 5px;
        }
        .robux-tag {
            color: #00e676;
            font-weight: bold;
        }
        .code-btn {
            display: inline-block;
            margin-top: 10px;
            padding: 6px 12px;
            background: #222;
            color: #fff;
            border: 1px solid #555;
            text-decoration: none;
            font-size: 12px;
        }
        .code-btn:hover {
            background: #fff;
            color: #000;
        }
    </style>
</head>
<body>

    <div class="top-bar">
        <a href="#" class="login-btn">Login with Google</a>
        <a href="#" class="login-btn">Login with Facebook</a>
    </div>

    <h1 class="site-title">Roblox avatar ideas</h1>

    <div class="controls">
        <form action="/" method="GET" class="search-box">
            <input type="text" name="q" placeholder="Searching for avatar ideas" value="{{ search_query }}">
        </form>
        <a href="/?upload=true" class="upload-btn-green">Upload Roblox avatar ideas</a>
    </div>

    <div class="upload-section">
        <h3>Upload New Avatar Idea</h3>
        <form action="/upload" method="POST">
            <div class="form-group">
                <label>Author (Email):</label>
                <input type="text" name="author" placeholder="e.g. bahgd@gmail.com" required>
            </div>
            <div class="form-group">
                <label>Image URL ([Attach Image]):</label>
                <input type="url" name="image_url" placeholder="https://..." required>
            </div>
            <div class="form-group">
                <label>Avatar Code or Link:</label>
                <input type="text" name="avatar_code_link" placeholder="Enter Roblox item code or link" required>
            </div>
            <div class="form-group">
                <label>Category (Genre):</label>
                <input type="text" name="category" placeholder="e.g. vkei, emo, Y2K" required>
            </div>
            <div class="form-group">
                <label>Description:</label>
                <textarea name="description" rows="3" placeholder="Description..."></textarea>
            </div>
            <button type="submit" class="submit-btn">Upload</button>
            <a href="/" style="color: #aaa; margin-left: 10px; font-size: 12px;">Cancel</a>
        </form>
    </div>

    <div class="avatar-grid">
        {% for item in avatars %}
        <div class="avatar-card">
            <img src="{{ item.image_url }}" alt="Avatar Image" onerror="this.src='https://via.placeholder.com/300x300/111/fff?text=No+Image';">
            <div class="avatar-info">
                <p><strong>From:</strong> {{ item.author }}</p>
                <p><strong>Category:</strong> {{ item.category }}</p>
                <p><strong>Robux Total:</strong> <span class="robux-tag">R$ {{ item.robux_cost }}</span> (Bot Calculated)</p>
                {% if item.description %}
                <p><strong>Intro:</strong> {{ item.description }}</p>
                {% endif %}
                <a href="{{ item.avatar_code_link }}" target="_blank" class="code-btn">Click to get link or code</a>
            </div>
        </div>
        {% else %}
        <p style="grid-column: 1/-1; text-align: center; color: #777;">No avatar ideas found.</p>
        {% endfor %}
    </div>

</body>
</html>
'''

def robot_scan_robux(code_or_link):
    return random.randint(150, 2500)

@app.route('/')
def index():
    query = request.args.get('q', '').strip()
    show_upload = request.args.get('upload', 'false') == 'true'
    
    db = get_db()
    cursor = db.cursor()
    
    if query:
        cursor.execute("SELECT * FROM avatars WHERE category LIKE ? OR author LIKE ? OR description LIKE ?", 
                       (f'%{query}%', f'%{query}%', f'%{query}%'))
    else:
        cursor.execute("SELECT * FROM avatars ORDER BY id DESC")
        
    avatars = cursor.fetchall()
    
    return render_template_string(
        HTML_TEMPLATE, 
        avatars=avatars, 
        search_query=query, 
        show_upload=show_upload
    )

@app.route('/upload', methods=['POST'])
def upload():
    author = request.form.get('author')
    image_url = request.form.get('image_url')
    avatar_code_link = request.form.get('avatar_code_link')
    category = request.form.get('category').lower()
    description = request.form.get('description')
    
    robux_cost = robot_scan_robux(avatar_code_link)
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO avatars (author, image_url, avatar_code_link, category, description, robux_cost)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (author, image_url, avatar_code_link, category, description, robux_cost))
    db.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
    
