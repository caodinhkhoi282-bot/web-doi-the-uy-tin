from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "doitheuytin_sieucap"

# CƠ SỞ DỮ LIỆU GIẢ LẬP
USERS = {}       
CARDS_SUBMITTED = []  # Danh sách thẻ khách gửi nạp
BUY_ORDERS = []       # Danh sách đơn khách ĐẶT MUA THẺ -> Đợi bạn gửi

# DANH SÁCH ĐẦY ĐỦ CÁC LOẠI THẺ CÓ HÌNH ẢNH (Dùng Logo bằng CSS cho nhẹ và không lỗi link)
CARD_TYPES = {
    "viettel": {"name": "Viettel", "color": "#E51F27"},
    "vinaphone": {"name": "Vinaphone", "color": "#00A4E4"},
    "mobifone": {"name": "Mobifone", "color": "#0054A5"},
    "garena": {"name": "Garena", "color": "#FF0000"},
    "zing": {"name": "Zing Card", "color": "#81C784"},
    "gate": {"name": "Gate", "color": "#FF9800"},
    "vcoin": {"name": "Vcoin", "color": "#0288D1"}
}
DENOMINATIONS = [10000, 20000, 50000, 100000, 200000, 500000]

BASE_CSS = """
<style>
    body { background-color: #f4f6f9; color: #333; font-family: Arial, sans-serif; margin: 0; padding: 0; }
    .navbar { background-color: #ffffff; border-bottom: 1px solid #e0e0e0; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .navbar a { color: #d32f2f; text-decoration: none; font-weight: bold; margin-left: 15px; }
    .logo { font-size: 22px; color: #2196F3; font-weight: bold; text-decoration: none; }
    .container { max-width: 700px; margin: 25px auto; padding: 20px; border-radius: 12px; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    h2 { color: #222; border-left: 5px solid #2196F3; padding-left: 10px; font-size: 18px; margin-bottom: 20px; }
    .form-group { margin-bottom: 15px; }
    label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px; }
    input, select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 14px; }
    button { background-color: #2196F3; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
    button:hover { background-color: #1e88e5; }
    
    /* Giao diện lưới chọn thẻ */
    .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 15px; margin-top: 15px; }
    .card-item { border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px 10px; text-align: center; cursor: pointer; font-weight: bold; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); text-decoration: none; transition: transform 0.2s; }
    .card-item:hover { transform: scale(1.05); }
    
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th, td { border: 1px solid #e0e0e0; padding: 12px; text-align: left; font-size: 13px; }
    th { background-color: #f8f9fa; }
    .badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .bg-warning { background-color: #ffc107; color: #fff; }
    .bg-success { background-color: #28a745; color: #fff; }
    .bg-danger { background-color: #dc3545; color: #fff; }
</style>
"""

LOGIN_HTML = BASE_CSS + """
<div class="container" style="max-width: 450px; margin-top: 80px;">
    <div class="logo" style="text-align:center; margin-bottom:20px; font-size:26px;">doitheuytin.ok.com</div>
    <h2>ĐĂNG NHẬP / ĐĂNG KÝ TỰ ĐỘNG</h2>
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
    <a href="/dashboard" class="logo">ĐỔI THẺ UY TÍN/a>
    <div>
        <span>Xin chào: <b>{{ username }}</b> | Số dư: <b style="color:#28a745;">{{ balance }}đ</b></span>
        <a href="/logout">Đăng xuất</a>
    </div>
</div>

<!-- MỤC 1: NẠP THẺ -->
<div class="container">
    <h2>1. GỬI THẺ CÀO (ĐỔI THÀNH TIỀN)</h2>
    <form method="POST" action="/submit-card">
        <div class="form-group">
            <label>Loại thẻ:</label>
            <select name="card_type">
                {% for key, val in card_types.items() %}<option value="{{ key }}">{{ val.name }}</option>{% endfor %}
            </select>
        </div>
        <div class="form-group">
            <label>Mệnh giá thẻ:</label>
            <select name="amount">
                {% for d in denominations %}<option value="{{ d }}">{{ d }}đ</option>{% endfor %}
            </select>
        </div>
        <div class="form-group"><label>Số Seri:</label><input type="text" name="serial" placeholder="Nhập số seri" required></div>
        <div class="form-group"><label>Mã số sau lớp bạc:</label><input type="text" name="code" placeholder="Nhập mã thẻ" required></div>
        <button type="submit" style="background-color: #28a745;">GỬI THẺ DUYỆT</button>
    </form>
</div>

<!-- MỤC 2: MUA THẺ VỚI HÌNH ẢNH -->
<div class="container">
    <h2>2. CHỌN LOẠI THẺ CẦN MUA</h2>
    <p style="font-size: 13px; color: #666;">Bấm vào logo loại thẻ bạn muốn mua bên dưới:</p>
    <div class="card-grid">
        {% for key, val in card_types.items() %}
        <a href="/buy/{{ key }}" class="card-item" style="background-color: {{ val.color }};">
            <div style="font-size: 18px; margin-bottom: 5px;">💳</div>
            {{ val.name }}
        </a>
        {% endfor %}
    </div>
</div>

<!-- MỤC 3: THEO DÕI LỊCH SỬ -->
<div class="container">
    <h2>3. LỊCH SỬ GỬI THẺ & MUA THẺ</h2>
    <h3>Thẻ đã gửi đổi tiền:</h3>
    <table>
        <tr><th>Loại thẻ</th><th>Mệnh giá</th><th>Trạng thái</th></tr>
        {% for c in my_cards %}
        <tr>
            <td>{{ c.type.upper() }}</td><td>{{ c.amount }}đ</td>
            <td><span class="badge {% if c.status=='Chờ duyệt' %}bg-warning{% elif c.status=='Thành công' %}bg-success{% else %}bg-danger{% endif %}">{{ c.status }}</span></td>
        </tr>
        {% endfor %}
    </table>

    <h3 style="margin-top:25px;">Thẻ đã đặt mua:</h3>
    <table>
        <tr><th>Loại thẻ cần mua</th><th>Mệnh giá</th><th>Trạng thái nhận hàng</th></tr>
        {% for o in my_orders %}
        <tr>
            <td>{{ o.type.upper() }}</td><td>{{ o.amount }}đ</td>
            <td><span class="badge {% if o.status=='Đang xử lý' %}bg-warning{% else %}bg-success{% endif %}">{{ o.status }}</span></td>
        </tr>
        {% endfor %}
    </table>
</div>
"""

BUY_DETAIL_HTML = BASE_CSS + """
<div class="navbar"><a href="/dashboard" class="logo">doitheuytin.ok.com</a></div>
<div class="container">
    <h2>MUA THẺ: {{ card_info.name.upper() }}</h2>
    <div style="background: {{ card_info.color }}; color: white; padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 20px; font-weight: bold;">
        Hệ thống đang sẵn hàng mệnh giá dưới đây
    </div>
    <form method="POST" action="/process-buy">
        <input type="hidden" name="card_type" value="{{ card_type }}">
        <div class="form-group">
            <label>Chọn mệnh giá cần mua:</label>
            <select name="amount">
                {% for d in denominations %}<option value="{{ d }}">{{ d }}đ</option>{% endfor %}
            </select>
        </div>
        <p style="color: #666; font-size: 13px;">*Sau khi bấm Thanh toán, tiền số dư của bạn sẽ bị trừ. Admin sẽ nhận được thông báo để gửi mã thẻ qua tài khoản của bạn.</p>
        <button type="submit">XÁC NHẬN THANH TOÁN MUA THẺ</button>
    </form>
    <br><a href="/dashboard"> Quay lại trang chủ</a>
</div>
"""

ADMIN_HTML = BASE_CSS + """
<div class="container" style="max-width: 950px;">
    <h2>TRANG QUẢN TRỊ BẢO MẬT (ADMIN)</h2>
    
    <h3>🚨 1. KHÁCH ĐỔI THẺ (CẦN BẠN DUYỆT ĐỂ CỘNG TIỀN CHO KHÁCH)</h3>
    <table>
        <tr><th>Tài khoản</th><th>Loại</th><th>Mệnh giá</th><th>Mã / Seri</th><th>Hành động</th></tr>
        {% for c in all_cards %}
        <tr>
            <td>{{ c.username }}</td><td>{{ c.type.upper() }}</td><td>{{ c.amount }}đ</td><td>Mã: {{ c.code }} <br> Seri: {{ c.serial }}</td>
            <td>
                {% if c.status == 'Chờ duyệt' %}
                <a href="/admin/approve/{{ c.id }}" style="color:green; font-weight:bold;">[ĐÚNG - CỘNG TIỀN]</a> | 
                <a href="/admin/reject/{{ c.id }}" style="color:red; font-weight:bold;">[THẺ LỖI]</a>
                {% else %}{{ c.status }}{% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>

    <h3 style="margin-top:40px;">🛒 2. KHÁCH MUA THẺ (BẠN CẦN GỬI THẺ QUA ĐIỆN THOẠI/ZALO CHO HỌ)</h3>
    <p style="color: blue;">*Khách đã trả bằng số dư trên web rồi. Bạn hãy lấy mã thẻ thật gửi cho họ qua thông tin SĐT/Tài khoản dưới đây, xong bấm "Đã Gửi Thẻ".</p>
    <table>
        <tr><th>Tài khoản</th><th>Liên hệ (SĐT/Email)</th><th>Loại thẻ mua</th><th>Mệnh giá</th><th>Trạng thái</th><th>Hành động</th></tr>
        {% for o in all_orders %}
        <tr>
            <td>{{ o.username }}</td><td>{{ o.contact }}</td><td>{{ o.type.upper() }}</td><td>{{ o.amount }}đ</td><td>{{ o.status }}</td>
            <td>
                {% if o.status == 'Đang xử lý' %}
                <a href="/admin/ship-order/{{ o.id }}" style="background:green; color:white; padding:4px 8px; border-radius:4px; text-decoration:none;">ĐÃ GỬI THẺ XONG ✔</a>
                {% else %}Hoàn thành{% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
    <br><a href="/dashboard">Xem trang với tư cách khách hàng</a>
</div>
"""

# --- CÁC ĐƯỜNG DẪN ĐIỀU HƯỚNG ---

@app.route('/')
def index():
    if 'username' in session: return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    contact = request.form.get('contact', 'Không có')
    if username not in USERS:
        USERS[username] = {'password': password, 'contact': contact, 'balance': 0}
    session['username'] = username
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session: return redirect(url_for('index'))
    user = session['username']
    my_cards = [c for c in CARDS_SUBMITTED if c['username'] == user]
    my_orders = [o for o in BUY_ORDERS if o['username'] == user]
    return render_template_string(DASHBOARD_HTML, username=user, balance=USERS[user]['balance'], my_cards=my_cards, my_orders=my_orders, card_types=CARD_TYPES, denominations=DENOMINATIONS)

@app.route('/submit-card', methods=['POST'])
def submit_card():
    if 'username' not in session: return redirect(url_for('index'))
    CARDS_SUBMITTED.append({
        'id': len(CARDS_SUBMITTED) + 1, 'username': session['username'],
        'type': request.form['card_type'], 'amount': int(request.form['amount']),
        'serial': request.form['serial'], 'code': request.form['code'], 'status': 'Chờ duyệt'
    })
    return redirect(url_for('dashboard'))

@app.route('/buy/<card_type>')
def buy_detail(card_type):
    if card_type not in CARD_TYPES: return redirect(url_for('dashboard'))
    return render_template_string(BUY_DETAIL_HTML, card_type=card_type, card_info=CARD_TYPES[card_type], denominations=DENOMINATIONS)

@app.route('/process-buy', methods=['POST'])
def process_buy():
    if 'username' not in session: return redirect(url_for('index'))
    user = session['username']
    card_type = request.form['card_type']
    amount = int(request.form['amount'])
    
    if USERS[user]['balance'] >= amount:
        USERS[user]['balance'] -= amount  # Trừ tiền tài khoản web của khách
        BUY_ORDERS.append({
            'id': len(BUY_ORDERS) + 1, 'username': user, 'contact': USERS[user]['contact'],
            'type': card_type, 'amount': amount, 'status': 'Đang xử lý'
        })
        return "<script>alert('Thanh toán thành công! Đơn hàng đã chuyển tới Admin. Vui lòng đợi nhận mã thẻ.'); window.location='/dashboard';</script>"
    return "<script>alert('Tài khoản của bạn không đủ số dư để mua mệnh giá này! Hãy nạp thêm thẻ.'); window.location='/dashboard';</script>"

# --- KHU VỰC QUẢN LÝ CỦA ADMIN ---
@app.route('/secret-admin-panel')
def admin_panel():
    return render_template_string(ADMIN_HTML, all_cards=CARDS_SUBMITTED, all_orders=BUY_ORDERS)

@app.route('/admin/approve/<int:card_id>')
def admin_approve(card_id):
    card = next((c for c in CARDS_SUBMITTED if c['id'] == card_id), None)
    if card and card['status'] == 'Chờ duyệt':
        card['status'] = 'Thành công'
        USERS[card['username']]['balance'] += card['amount']
    return redirect(url_for('admin_panel'))

@app.route('/admin/reject/<int:card_id>')
def admin_reject(card_id):
    card = next((c for c in CARDS_SUBMITTED if c['id'] == card_id), None)
    if card and card['status'] == 'Chờ duyệt': card['status'] = 'Thẻ lỗi/Sai mã'
    return redirect(url_for('admin_panel'))

@app.route('/admin/ship-order/<int:order_id>')
def admin_ship(order_id):
    order = next((o for o in BUY_ORDERS if o['id'] == order_id), None)
    if order: order['status'] = 'Đã giao thẻ thành công ✔'
    return redirect(url_for('admin_panel'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
