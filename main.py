from flask import Flask, render_template_string

app = Flask(__name__)

# Giao diện chính siêu gọn, tích hợp sẵn hình ảnh và nút Discord
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Arial', sans-serif; text-align: center; background: #f4f6f9; padding: 50px 20px; margin: 0; }
        .box { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }
        h1 { color: #333; }
        .logo { width: 100px; height: 100px; border-radius: 50%; margin-bottom: 20px; object-fit: cover; }
        
        /* Nút Discord hỗ trợ */
        .discord-btn { 
            position: fixed; bottom: 20px; right: 20px; background: #5865F2; 
            color: white; padding: 12px 20px; border-radius: 25px; 
            text-decoration: none; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            font-size: 14px; z-index: 1000;
        }
    </style>
</head>
<body>
    <div class="box">
        <img src="https://img.freepik.com/premium-vector/d-letter-logo-luxury-gold-color_755034-846.jpg" class="logo" alt="Logo">
        <h1>doithecaouytinok.com</h1>
        <p>Hệ thống đang được nâng cấp để phục vụ bạn tốt hơn.</p>
        <p>Vui lòng quay lại sau ít phút!</p>
    </div>
    <a href="https://discord.gg/x4PqVMxhH" class="discord-btn" target="_blank">🎧 Hỗ trợ Discord</a>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run()
    
