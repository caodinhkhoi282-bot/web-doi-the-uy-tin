from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Giao diện HTML & CSS (Đã được thiết kế responsive, trực quan)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Center - Resource Manager</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background-color: #191b1d;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: #25282a;
            padding: 40px 30px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
            width: 100%;
            max-width: 400px;
            border: 1px solid #3a3f44;
        }
        h2 {
            text-align: center;
            margin-bottom: 25px;
            color: #f5f5f5;
            font-size: 24px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #bbbbbb;
            font-size: 14px;
        }
        input[type="text"], select {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #3a3f44;
            background-color: #121314;
            color: #ffffff;
            border-radius: 6px;
            font-size: 15px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus, select:focus {
            border-color: #0084ff;
            outline: none;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #0084ff;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.1s;
            margin-top: 10px;
        }
        button:hover {
            background-color: #0066cc;
        }
        button:active {
            transform: scale(0.98);
        }
        .result {
            margin-top: 20px;
            padding: 12px;
            background-color: rgba(40, 167, 69, 0.1);
            border: 1px solid #28a745;
            color: #28a745;
            border-radius: 6px;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
        }
        .footer {
            margin-top: 25px;
            text-align: center;
            font-size: 11px;
            color: #666;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>Game Resource</h2>
    
    <form method="POST">
        <div class="form-group">
            <label for="player_id">Enter ID/NAME</label>
            <input type="text" id="player_id" name="player_id" placeholder="Nhập ID hoặc tên người chơi..." required>
        </div>
        
        <div class="form-group">
            <label for="robux_amount">Choose the number of Game Coins</label>
            <select id="robux_amount" name="robux_amount">
                <option value="50">50 Coins</option>
                <option value="300">300 Coins</option>
                <option value="500">500 Coins</option>
                <option value="10000">10k Coins</option>
                <option value="100000">100k Coins</option>
            </select>
        </div>
        
        <button type="submit">Send to player</button>
    </form>

    {% if message %}
        <div class="result">{{ message }}</div>
    {% endif %}
    
    <div class="footer">
        Hệ thống mô phỏng vận chuyển vật phẩm game nội bộ.
    </div>
</div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        robux_amount = request.form.get('robux_amount')
        
        # Ghi nhận log lên hệ thống Render (giúp bạn theo dõi trong mục "Logs" trên Render dashboard)
        print(f"[LOG] Yêu cầu chuyển {robux_amount} Coins cho người chơi: {player_id}")
        
        # Thông báo phản hồi lại trên giao diện web
        message = f"Gửi yêu cầu thành công! Đang xử lý {robux_amount} Coins đến '{player_id}'."
        
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    # Render yêu cầu chạy ứng dụng qua cổng (Port) được cấp phát động qua biến môi trường
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
