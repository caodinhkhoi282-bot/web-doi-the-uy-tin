from flask import Flask, render_template_string, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = "doitheuytin_sieucap"

# --- ĐƯỜNG DẪN FILE LƯU TRỮ TRÊN SERVER ---
USERS_FILE = "database_users.txt"
CARDS_FILE = "database_cards.txt"
ORDERS_FILE = "database_orders.txt"

# Các loại thẻ lớn, nổi tiếng toàn quốc được ƯU TIÊN GIỮ LẠI KHÔNG XÓA KHI ĐẦY BỘ NHỚ
PRIORITY_CARD_TYPES = ["viettel", "garena", "zing"]

# --- HÀM TỰ ĐỘNG ĐỌC VÀ GHI FILE (CÓ THUẬT TOÁN LỌC ƯU TIÊN) ---
def load_data():
    global USERS, CARDS_SUBMITTED, BUY_ORDERS
    
    # Đọc dữ liệu tài khoản
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                USERS = json.load(f)
        except: USERS = {}
    else: USERS = {}

    # Đọc dữ liệu thẻ cào đã gửi
    if os.path.exists(CARDS_FILE):
        try:
            with open(CARDS_FILE, "r", encoding="utf-8") as f:
                CARDS_SUBMITTED = json.load(f)
        except: CARDS_SUBMITTED = []
    else: CARDS_SUBMITTED = []

    # Đọc dữ liệu đơn mua thẻ
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                BUY_ORDERS = json.load(f)
        except: BUY_ORDERS = []
    else: BUY_ORDERS = []

def save_users():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(USERS, f, ensure_ascii=False)

def save_cards():
    global CARDS_SUBMITTED
    # THUẬT TOÁN LỌC ƯU TIÊN CHỐNG TRÀN BỘ NHỚ
    if len(CARDS_SUBMITTED) > 200:
        # Tách riêng thẻ ưu tiên (Viettel, Garena, Zing) và thẻ thường
        priority_cards = [c for c in CARDS_SUBMITTED if c.get('type') in PRIORITY_CARD_TYPES]
        normal_cards = [c for c in CARDS_SUBMITTED if c.get('type') not in PRIORITY_CARD_TYPES]
        
        # Cắt bớt thẻ thường cũ hơn để dọn chỗ, chỉ giữ lại những thẻ thường mới nhất
        max_normal_allowed = 200 - len(priority_cards)
        if max_normal_allowed > 0:
            normal_cards = normal_cards[-max_normal_allowed:]
        else:
            normal_cards = [] # Nếu thẻ ưu tiên quá nhiều, tạm thời xóa hết thẻ thường cũ
            
        # Gộp lại danh sách (Thẻ lớn toàn quốc luôn được bảo vệ an toàn)
        CARDS_SUBMITTED = priority_cards + normal_cards
        
    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(CARDS_SUBMITTED, f, ensure_ascii=False)

def save_orders():
    global BUY_ORDERS
    if len(BUY_ORDERS) > 100:
        BUY_ORDERS = BUY_ORDERS[-100:]
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(BUY_ORDERS, f, ensure_ascii=False)

# Khởi tạo dữ liệu hệ thống
load_data()

CARD_TYPES = {
    "viettel": {"name": "Viettel (Ưu tiên)", "color": "#E51F27"},
    "garena": {"name": "Garena (Ưu tiên)", "color": "#FF0000"},
    "zing": {"name": "Zing Card (Ưu tiên)", "color": "#81C784"},
    "vinaphone": {"name": "Vinaphone", "color": "#00A4E4"},
    "mobifone": {"name": "Mobifone", "color": "#0054A5"},
    "gate": {"name": "Gate", "color": "#FF9800"},
    "vcoin": {"name": "Vcoin", "color": "#0288D1"}
}
DENOMINATIONS = [10000, 20000, 50000, 100000, 200000, 500000]

# --- CSS STYLE (NÚT DISCORD TRÒN ĐEN CỐ ĐỊNH) ---
BASE_CSS = """
<style>
    body { background-color: #f4f6f9; color: #333; font-family: Arial, sans-serif; margin: 0; padding: 0; padding-bottom: 60px; }
    .navbar { background-color: #ffffff; border-bottom: 1px solid #e0e0e0; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .navbar a { color: #d32f2f; text-decoration: none; font-weight: bold; margin-left: 15px; }
    .logo-container { display: flex; align-items: center; justify-content: center; text-decoration: none; gap: 10px; margin: 20px 0; }
    .logo-img { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .container { max-width: 700px; margin: 25px auto; padding: 20px; border-radius: 12px; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    h2 { color: #222; border-left: 5px solid #2196F3; padding-left: 10px; font-size: 18px; margin-bottom: 20px; }
    .form-group { margin-bottom: 15px; }
    label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px; }
    input, select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 14px; margin-bottom: 5px; }
    button { background-color: #2196F3; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 15px; margin-top: 15px; }
    .card-item { border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px 10px; text-align: center; cursor: pointer; font-weight: bold; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); text-decoration: none; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th, td { border: 1px solid #e0e0e0; padding: 12px; text-align: left; font-size: 13px; }
    th { background-color: #f8f9fa; }
    .badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .bg-warning { background-color: #ffc107; color: #fff; }
    .bg-success { background-color: #28a745; color: #fff; }
    .bg-danger { background-color: #dc3545; color: #fff; }
    .discord-fixed-btn { position: fixed; bottom: 25px; right: 25px; background-color: #111; color: #fff; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; text-decoration: none; font-size: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 9999; transition: 0.3s; }
    .discord-fixed-btn:hover { transform: scale(1.1); }
</style>
<a href="https://discord.gg/x4PqVMxhH" class="discord-fixed-btn" target="_blank" title="Hỗ trợ Discord">💬</a>
"""

LOGIN_HTML = BASE_CSS + """
<div class="container" style="max-width: 450px; margin-top: 40px;">
    <div class="logo-container"><img src="https://img.freepik.com/premium-vector/d-letter-logo-luxury-gold-color_755034-846.jpg" class="logo-img"></div>
    <h2 style="text-align: center; border: none;">ĐĂNG NHẬP / ĐĂNG KÝ TỰ ĐỘNG</h2>
    <form method="POST" action="/login">
        <div class="form-group"><label>Tên đăng nhập:</label><input type="text" name="username" required></div>
        <div class="form-group"><label>Mật khẩu:</label><input type="password" name="password" required></div>
        <div class="form-group"><label>Số điện thoại / Email:</label><input type="text" name="contact" placeholder="Nhập SĐT hoặc Email"></div>
        <button type="submit">VÀO TRANG ĐỔI THẺ</button>
    </form>
</div>
"""

DASHBOARD_HTML = BASE_CSS + """
<div class="navbar">
    <b style="font-size: 18px; color: #2196F3;">doithecaouytinok.com</b>
    <div>
        <span>Xin chào: <b>{{ username }}</b> | Số dư: <b style="color:#28a745;">{{ balance }}đ</b></span>
        <a href="/logout">Đăng xuất</a>
    </div>
</div>
<div class="container">
    <h2>1. GỬI THẺ CÀO (ĐỔI THÀNH TIỀN)</h2>
    <form method="POST" action="/submit-card">
        <div class="form-group">
            <label>Loại thẻ:</label>
            <select name="card_type">{% for key, val in card_types.items() %}<option value="{{ key }}">{{ val.name }}</option>{% endfor %}</select>
        </div>
        <div class="form-group">
            <label>Mệnh giá thẻ:</label>
            <select name="amount">{% for d in denominations %}<option value="{{ d }}">{{ d }}đ</option>{% endfor %}</select>
        </div>
        <div class="form-group"><label>Số Seri:</label><input type="text" name="serial" required></div>
        <div class="form-group"><label>Mã số sau lớp bạc:</label><input type="text" name="code" required></div>
        <button type="submit" style="background-color: #28a745;">GỬI THẺ DUYỆT</button>
    </form>
</div>
<div class="container">
    <h2>2. CHỌN LOẠI THẺ CẦN MUA</h2>
    <div class="card-grid">
        {% for key, val in card_types.items() %}
        <a href="/buy/{{ key }}" class="card-item" style="background-color: {{ val.color }};"><div style="font-size: 18px;">💳</div>{{ val.name }}</a>
        {% endfor %}
    </div>
</div>
<div class="container">
    <h2>3. LỊCH SỬ GỬI THẺ & MUA THẺ</h2>
    <h3>Thẻ bạn đã gửi:</h3>
    <table>
        <tr><th>Loại thẻ</th><th>Mệnh giá</th><th>Trạng thái</th></tr>
        {% for c in my_cards %}
        <tr>
            <td>{{ c.type.upper() }}</td><td>{{ c.amount }}đ</td>
            <td><span class="badge {% if c.status=='Chờ duyệt' %}bg-warning{% elif c.status=='Thành công' %}bg-success{% else %}bg-danger{% endif %}">{{ c.status }}</span></td>
        </tr>
        {% endfor %}
    </table>
</div>
"""

BUY_DETAIL_HTML = BASE_CSS + """
<div class="navbar"><b style="font-size:18px;">doithecaouytinok.com</b></div>
<div class="container">
    <h2>MUA THẺ: {{ card_info.name.upper() }}</h2>
    <form method="POST" action="/process-buy">
        <input type="hidden" name="card_type" value="{{ card_type }}">
        <div class="form-group">
            <label>Chọn mệnh giá cần mua:</label>
            <select name="amount">{% for d in denominations %}<option value="{{ d }}">{{ d }}đ</option>{% endfor %}</select>
        </div>
        <button type="submit">XÁC NHẬN THANH TOÁN MUA THẺ</button>
    </form>
    <br><a href="/dashboard"> Quay lại trang chủ</a>
</div>
"""

ADMIN_HTML = BASE_CSS + """
<div class="container" style="max-width: 950px;">
    <h2>TRANG QUẢN TRỊ BẢO MẬT (ADMIN)</h2>
    
    <div style="background: #eef2f7; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
        <h3>🔍 QUAN SÁT TÀI KHOẢN (LƯU TRỮ AN TOÀN)</h3>
        <form method="GET" action="/secret-admin-panel">
            <input type="text" name="search_user" placeholder="Nhập tên tài khoản..." value="{{ search_keyword }}">
            <button type="submit" style="background: #444; width: auto; padding: 10px 20px;">Tìm kiếm</button>
            {% if search_keyword %}<a href="/secret-admin-panel" style="margin-left:10px;">Xóa bộ lọc</a>{% endif %}
        </form>
        {% if search_result %}
        <div style="margin-top: 15px; background: white; padding: 15px; border-radius: 6px; border: 1px dashed #2196F3;">
            <p>📌 Tài khoản: <b>{{ search_result.username }}</b></p>
            <p>📞 Liên hệ: {{ search_result.contact }}</p>
            <p>💰 Số dư hiện tại: <b style="color:red; font-size:16px;">{{ search_result.balance }}đ</b></p>
        </div>
        {% elif search_keyword %}
        <p style="color: red; margin-top:10px;">❌ Không có tài khoản "{{ search_keyword }}"</p>
        {% endif %}
    </div>

    <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 30px; border: 1px solid #ffeeba;">
        <h3>🎁 GIFT TIỀN CỨU TRỢ NGƯỜI CHƠI</h3>
        <form method="POST" action="/admin/gift">
            <div style="display: flex; gap: 10px;">
                <input type="text" name="gift_username" placeholder="Tên tài khoản nhận..." required>
                <input type="number" name="gift_amount" placeholder="Số tiền..." required>
            </div>
            <button type="submit" style="background: #ff9800; margin-top: 5px;">XÁC NHẬN GIFT TIỀN 🚀</button>
        </form>
    </div>

    <h3>🚨 CHI TIẾT THẺ KHÁCH ĐÃ GỬI (ƯU TIÊN VIETTEL, GARENA, ZING)</h3>
    <table>
        <tr><th>Tài khoản</th><th>Loại</th><th>Mệnh giá</th><th>Số Seri</th><th>Mã Thẻ (Code)</th><th>Trạng thái</th><th>Hành động</th></tr>
        {% for c in all_cards %}
        <tr>
            <td><b>{{ c.username }}</b></td>
            <td>
                {% if c.type in ["viettel", "garena", "zing"] %}
                    <span style="color: #ff9800; font-weight: bold;">🔥 {{ c.type.upper() }}</span>
                {% else %}
                    {{ c.type.upper() }}
                {% endif %}
            </td>
            <td>{{ c.amount }}đ</td>
            <td style="color: #0054A5; font-weight: bold;">{{ c.serial }}</td>
            <td style="color: #E51F27; font-weight: bold;">{{ c.code }}</td>
            <td><span class="badge {% if c.status=='Chờ duyệt' %}bg-warning{% elif c.status=='Thành công' %}bg-success{% else %}bg-danger{% endif %}">{{ c.status }}</span></td>
            <td>
                {% if c.status == 'Chờ duyệt' %}
                <a href="/admin/approve/{{ c.id }}" style="color:green; font-weight:bold;">[ĐÚNG]</a> | 
                <a href="/admin/reject/{{ c.id }}" style="color:red; font-weight:bold;">[LỖI]</a>
                {% else %}-{% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
    <br><a href="/dashboard">Xem trang với tư cách khách hàng</a>
</div>
"""

@app.route('/')
def index():
    load_data()
    if 'username' in session: return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    load_data()
    username = request.form['username'].strip()
    password = request.form['password']
    contact = request.form.get('contact', 'Không có')
    if username not in USERS:
        USERS[username] = {'password': password, 'contact': contact, 'balance': 0}
        save_users()
    session['username'] = username
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    load_data()
    if 'username' not in session: return redirect(url_for('index'))
    user = session['username']
    my_cards = [c for c in CARDS_SUBMITTED if c['username'] == user]
    my_orders = [o for o in BUY_ORDERS if o['username'] == user]
    return render_template_string(DASHBOARD_HTML, username=user, balance=USERS.get(user, {'balance':0})['balance'], my_cards=my_cards, my_orders=my_orders, card_types=CARD_TYPES, denominations=DENOMINATIONS)

@app.route('/submit-card', methods=['POST'])
def submit_card():
    load_data()
    if 'username' not in session: return redirect(url_for('index'))
    CARDS_SUBMITTED.append({
        'id': len(CARDS_SUBMITTED) + 1, 'username': session['username'],
        'type': request.form['card_type'], 'amount': int(request.form['amount']),
        'serial': request.form['serial'].strip(), 'code': request.form['code'].strip(), 'status': 'Chờ duyệt'
    })
    save_cards()
    return redirect(url_for('dashboard'))

@app.route('/secret-admin-panel')
def admin_panel():
    load_data()
    search_keyword = request.args.get('search_user', '').strip()
    search_result = None
    if search_keyword in USERS:
        search_result = USERS[search_keyword]
        search_result['username'] = search_keyword
    
    return render_template_string(ADMIN_HTML, all_cards=CARDS_SUBMITTED, all_orders=BUY_ORDERS, search_keyword=search_keyword, search_result=search_result)

@app.route('/admin/gift', methods=['POST'])
def admin_gift():
    load_data()
    target_user = request.form['gift_username'].strip()
    gift_amount = int(request.form['gift_amount'])
    
    if target_user in USERS:
        USERS[target_user]['balance'] += gift_amount
    else:
        USERS[target_user] = {'password': '123', 'contact': 'Admin Gift', 'balance': gift_amount}
    
    save_users()
    return f"<script>alert('Đã xử lý Gift xong!'); window.location='/secret-admin-panel';</script>"

@app.route('/admin/approve/<int:card_id>')
def admin_approve(card_id):
    load_data()
    card = next((c for c in CARDS_SUBMITTED if c['id'] == card_id), None)
    if card and card['status'] == 'Chờ duyệt':
        card['status'] = 'Thành công'
        if card['username'] in USERS:
            USERS[card['username']]['balance'] += card['amount']
        save_users()
        save_cards()
    return redirect(url_for('admin_panel'))

@app.route('/admin/reject/<int:card_id>')
def admin_reject(card_id):
    load_data()
    card = next((c for c in CARDS_SUBMITTED if c['id'] == card_id), None)
    if card and card['status'] == 'Chờ duyệt':
        card['status'] = 'Thẻ lỗi/Sai mã'
        save_cards()
    return redirect(url_for('admin_panel'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
                      
