from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <!-- Ẩn thanh URL trên mobile -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>Roblox - Gửi Robux</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
        body {
            background: #1a1a2e;
            color: #fff;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 20px 10px;
        }
        .container {
            max-width: 800px;
            width: 100%;
            background: #2d2d44;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
            overflow: hidden;
            border: 1px solid #3a3a5a;
        }
        .header {
            background: #1b1b2f;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #3a3a5a;
            flex-wrap: wrap;
            gap: 8px;
        }
        .logo {
            font-size: 24px;
            font-weight: 700;
            color: #00bfff;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .logo i { color: #fff; }
        .balance {
            background: #1f1f3a;
            padding: 6px 18px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: 600;
            border: 1px solid #3a3a5a;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .balance i { color: #ffd700; }
        .balance span { color: #fff; }
        .nav {
            background: #22223b;
            padding: 10px 20px;
            display: flex;
            gap: 20px;
            border-bottom: 1px solid #3a3a5a;
            flex-wrap: wrap;
        }
        .nav a {
            color: #aaa;
            text-decoration: none;
            font-weight: 500;
            font-size: 15px;
            padding: 6px 12px;
            border-radius: 8px;
            transition: 0.2s;
        }
        .nav a:hover, .nav a.active {
            background: #3a3a5a;
            color: #fff;
        }
        .content { padding: 20px; }
        .search-section {
            background: #1f1f3a;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #3a3a5a;
        }
        .search-section h2 {
            font-size: 20px;
            margin-bottom: 12px;
            color: #eee;
        }
        .search-box {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .search-box input {
            flex: 1;
            background: #0d0d1a;
            border: 1px solid #3a3a5a;
            border-radius: 30px;
            padding: 12px 18px;
            color: #fff;
            font-size: 16px;
            outline: none;
            min-width: 200px;
        }
        .search-box input:focus { border-color: #00bfff; }
        .search-box button {
            background: #00bfff;
            border: none;
            color: #000;
            font-weight: 700;
            padding: 12px 24px;
            border-radius: 30px;
            cursor: pointer;
            font-size: 16px;
            transition: 0.2s;
        }
        .search-box button:hover { background: #00a0d0; }
        .user-result {
            background: #1a1a30;
            border-radius: 12px;
            padding: 16px;
            margin-top: 16px;
            border: 1px solid #3a3a5a;
            display: none;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
        }
        .user-result .avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: #3a3a5a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            color: #fff;
        }
        .user-result .info { flex: 1; }
        .user-result .info .name { font-size: 18px; font-weight: 600; }
        .user-result .info .id { color: #aaa; font-size: 13px; }
        .user-result .send-btn {
            background: #00c853;
            border: none;
            color: #000;
            font-weight: 700;
            padding: 8px 20px;
            border-radius: 30px;
            cursor: pointer;
            font-size: 14px;
        }
        .send-form {
            background: #1f1f3a;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #3a3a5a;
            margin-top: 20px;
            display: none;
        }
        .send-form label {
            display: block;
            margin-bottom: 6px;
            font-weight: 500;
            color: #ccc;
        }
        .send-form input {
            width: 100%;
            background: #0d0d1a;
            border: 1px solid #3a3a5a;
            border-radius: 30px;
            padding: 12px 18px;
            color: #fff;
            font-size: 16px;
            margin-bottom: 16px;
            outline: none;
        }
        .send-form input:focus { border-color: #00bfff; }
        .send-form .actions {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        .send-form .actions button {
            padding: 10px 28px;
            border-radius: 30px;
            border: none;
            font-weight: 700;
            cursor: pointer;
            font-size: 16px;
            transition: 0.2s;
        }
        .send-form .actions .confirm { background: #00c853; color: #000; }
        .send-form .actions .cancel { background: #b71c1c; color: #fff; }
        .send-form .actions button:active { transform: scale(0.97); }
        .toast {
            background: #1a1a30;
            border: 1px solid #3a3a5a;
            border-radius: 30px;
            padding: 14px 24px;
            color: #fff;
            font-size: 15px;
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: none;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            z-index: 999;
            text-align: center;
            max-width: 90%;
        }
        .toast.success { border-color: #00c853; }
        .toast.error { border-color: #b71c1c; }
        .toast i { margin-right: 10px; }
        @media (max-width: 600px) {
            .header { flex-direction: column; align-items: stretch; text-align: center; }
            .balance { justify-content: center; }
            .nav { justify-content: center; }
            .search-box button { width: 100%; }
            .user-result { flex-direction: column; align-items: stretch; text-align: center; }
            .send-form .actions { flex-direction: column; }
        }
    </style>
</head>
<body>

<div class="toast" id="toast"><i class="fas fa-check-circle"></i> <span id="toastMsg">Thành công</span></div>

<div class="container">
    <div class="header">
        <div class="logo"><i class="fab fa-roblox"></i> Roblox</div>
        <div class="balance"><i class="fas fa-coins"></i> <span id="balanceDisplay">5,684,000</span> RB</div>
    </div>

    <div class="nav">
        <a href="#" class="active"><i class="fas fa-home"></i> Trang chủ</a>
        <a href="#"><i class="fas fa-users"></i> Bạn bè</a>
        <a href="#"><i class="fas fa-gift"></i> Quà tặng</a>
        <a href="#"><i class="fas fa-cog"></i> Cài đặt</a>
    </div>

    <div class="content">
        <div class="search-section">
            <h2><i class="fas fa-search"></i> Tìm người chơi</h2>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Nhập tên hoặc ID..." autocomplete="off">
                <button id="searchBtn"><i class="fas fa-arrow-right"></i> Tìm</button>
            </div>
            <div class="user-result" id="userResult">
                <div class="avatar" id="avatarDisplay"><i class="fas fa-user"></i></div>
                <div class="info">
                    <div class="name" id="userName">Tên</div>
                    <div class="id" id="userId">ID: 123456789</div>
                </div>
                <button class="send-btn" id="sendBtn"><i class="fas fa-paper-plane"></i> Gửi Robux</button>
            </div>
        </div>

        <div class="send-form" id="sendForm">
            <h3 style="margin-bottom:12px; color:#eee;"><i class="fas fa-paper-plane"></i> Gửi Robux</h3>
            <label>Người nhận: <span id="receiverName" style="color:#00bfff;">---</span></label>
            <label>Số Robux:</label>
            <input type="number" id="amountInput" placeholder="Nhập số lượng..." min="1" max="5684000">
            <div class="actions">
                <button class="confirm" id="confirmSend"><i class="fas fa-check"></i> Xác nhận gửi</button>
                <button class="cancel" id="cancelSend"><i class="fas fa-times"></i> Hủy</button>
            </div>
        </div>
    </div>
</div>

<script>
    const mockUsers = [
        { id: 123456789, name: "KhoiPro", avatar: "👨‍💻" },
        { id: 987654321, name: "RobloxMaster", avatar: "🎮" },
        { id: 555555555, name: "GameThủ", avatar: "🕹️" },
        { id: 111111111, name: "DevPro", avatar: "💻" },
        { id: 222222222, name: "HackerX", avatar: "🤖" }
    ];

    let currentUser = null;
    let balance = 5684000;

    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const userResult = document.getElementById('userResult');
    const userName = document.getElementById('userName');
    const userId = document.getElementById('userId');
    const avatarDisplay = document.getElementById('avatarDisplay');
    const sendBtn = document.getElementById('sendBtn');
    const sendForm = document.getElementById('sendForm');
    const receiverName = document.getElementById('receiverName');
    const amountInput = document.getElementById('amountInput');
    const confirmSend = document.getElementById('confirmSend');
    const cancelSend = document.getElementById('cancelSend');
    const balanceDisplay = document.getElementById('balanceDisplay');
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toastMsg');

    function showToast(message, type = 'success') {
        toast.className = 'toast ' + type;
        toastMsg.textContent = message;
        toast.style.display = 'block';
        clearTimeout(toast._timer);
        toast._timer = setTimeout(() => { toast.style.display = 'none'; }, 3000);
    }

    function updateBalance() {
        balanceDisplay.textContent = balance.toLocaleString();
    }

    function searchUser(query) {
        query = query.trim().toLowerCase();
        if (!query) { showToast('Vui lòng nhập tên hoặc ID.', 'error'); return null; }
        const found = mockUsers.find(u =>
            u.name.toLowerCase().includes(query) ||
            String(u.id).includes(query)
        );
        if (!found) { showToast('Không tìm thấy người chơi.', 'error'); return null; }
        return found;
    }

    function displayUser(user) {
        currentUser = user;
        userName.textContent = user.name;
        userId.textContent = 'ID: ' + user.id;
        avatarDisplay.innerHTML = user.avatar || '<i class="fas fa-user"></i>';
        userResult.style.display = 'flex';
        sendForm.style.display = 'none';
    }

    function handleSearch() {
        const query = searchInput.value;
        const user = searchUser(query);
        if (user) displayUser(user);
        else {
            userResult.style.display = 'none';
            sendForm.style.display = 'none';
        }
    }

    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keydown', e => { if (e.key === 'Enter') handleSearch(); });

    sendBtn.addEventListener('click', function() {
        if (!currentUser) { showToast('Chưa chọn người nhận.', 'error'); return; }
        receiverName.textContent = currentUser.name;
        amountInput.value = '';
        sendForm.style.display = 'block';
        amountInput.focus();
    });

    cancelSend.addEventListener('click', function() {
        sendForm.style.display = 'none';
    });

    confirmSend.addEventListener('click', function() {
        if (!currentUser) { showToast('Không có người nhận.', 'error'); return; }
        const amount = parseInt(amountInput.value);
        if (!amount || amount <= 0) { showToast('Nhập số Robux hợp lệ.', 'error'); return; }
        if (amount > balance) { showToast('Số dư không đủ! Bạn có ' + balance.toLocaleString() + ' RB.', 'error'); return; }
        balance -= amount;
        updateBalance();
        showToast(`✅ Đã gửi ${amount.toLocaleString()} RB đến ${currentUser.name} (mô phỏng)`, 'success');
        sendForm.style.display = 'none';
        userResult.style.display = 'none';
        currentUser = null;
        searchInput.value = '';
    });

    updateBalance();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
