import os
from flask import Flask, render_template_string, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = "doitheuytin_sieucap"

# =================================================================
# 🔗 THÔNG TIN SUPABASE CỦA BẠN
# =================================================================
SUPABASE_URL = "https://crtdwvzaccycikgxyriu.supabase.co"
SUPABASE_KEY = "sb_secret_ycV2N5g9jsxpP0OsFHduRQ_N_cJEqA9"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_USERNAME = "DINH_KHOI28215"
DISCORD_LINK = "https://discord.gg/j6Y9vB5cn"

CARD_TYPES = {
    "viettel": {"name": "Viettel (Ưu tiên)", "color": "#E51F27"},
    "garena": {"name": "Garena (Ưu tiên)", "color": "#FF0000"},
    "zing": {"name": "Zing Card (Ưu tiên)", "color": "#81C784"},
    "vinaphone": {"name": "Vinaphone", "color": "#00A4E4"},
    "mobifone": {"name": "Mobifone", "color": "#0054A5"}
}
DENOMINATIONS = [10000, 20000, 50000, 100000, 200000, 500000]

BASE_CSS = """
<style>
    body { background-color: #f4f6f9; color: #333; font-family: Arial, sans-serif; margin: 0; padding: 0; padding-bottom: 80px; }
    .navbar { background-color: #ffffff; border-bottom: 1px solid #e0e0e0; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .navbar-brand { display: flex; align-items: center; gap: 10px; text-decoration: none; }
    .brand-logo { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid #dfb76c; }
    .brand-name { font-size: 18px; color: #2196F3; font-weight: bold; }
    .navbar a.logout-btn { color: #d32f2f; text-decoration: none; font-weight: bold; margin-left: 15px; }
    .container { max-width: 750px; margin: 25px auto; padding: 20px; border-radius: 12px; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .auth-box { border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; background: #fafafa; margin-bottom: 20px; }
    h2 { color: #222; border-left: 5px solid #2196F3; padding-left: 10px; font-size: 18px; margin-bottom: 20px; }
    h3 { margin-top: 0; color: #333; font-size: 16px; border-bottom: 2px solid #ddd; padding-bottom: 8px; }
    .form-group { margin-bottom: 15px; }
    label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px; }
    input, select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 14px; margin-bottom: 5px; }
    button { background-color: #2196F3; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 15px; margin-top: 15px; }
    .card-item { text-align: center; color: white; font-weight: bold; text-decoration: none; padding: 15px; border-radius: 8px; transition: 0.2s; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th, td { border: 1px solid #e0e0e0; padding: 12px; text-align: left; font-size: 13px; }
    th { background-color: #f8f9fa; }
    .badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .bg-warning { background-color: #ffc107; color: #fff; }
    .bg-success { background-color: #28a745; color: #fff; }
    .bg-danger { background-color: #dc3545; color: #fff; }
    .btn-close { color: #dc3545; text-decoration: none; font-weight: bold; font-size: 14px; margin-left: 10px; cursor: pointer; }
    .btn-close:hover { text-decoration: underline; }
    .discord-support-btn { position: fixed; bottom: 20px; right: 20px; background-color: #5865F2; color: white; text-decoration: none; padding: 12px 20px; border-radius: 50px; font-weight: bold; font-size: 14px; box-shadow: 0 4px 15px rgba(88,101,242,0.4); display: flex; align-items: center; gap: 8px; z-index: 9999; transition: 0.2s; }
    .discord-support-btn:hover { background-color: #4752c4; transform: scale(1.05); color: white; }
</style>
"""

LOGO_HTML_TAG = """
<div class="navbar-brand">
    <img src="https://img.freepik.com/premium-vector/d-letter-logo-luxury-gold-color_755034-846.jpg" class="brand-logo" alt="Logo">
    <span class="brand-name">doithecaouytinok.com</span>
</div>
"""

DISCORD_BUTTON_TAG = """
<a class="discord-support-btn" href="{{ discord_link }}" target="_blank">
    <span>💬</span> Hỗ Trợ Discord
</a>
"""

LOGIN_HTML = BASE_CSS + """
<div class="navbar">
    """ + LOGO_HTML_TAG + """
</div>
<div class="container" style="max-width: 500px; margin-top: 20px;">
    <h2 style="text-align: center; border: none; margin-bottom: 30px;">HỆ THỐNG ĐỔI THẺ CAO ĐIỆN TỬ</h2>
    {% if msg %}<div style="color: red; font-weight: bold; text-align: center; margin-bottom: 15px;">{{ msg }}</div>{% endif %}
    <div class="auth-box">
        <h3>🔑 ĐĂNG NHẬP TÀI KHOẢN</h3>
        <form method="POST" action="/login">
            <div class="form-group"><label>Tên đăng nhập:</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Mật khẩu:</label><input type="password" name="password" required></div>
            <button type="submit" style="background-color: #2196F3;">ĐĂNG NHẬP</button>
        </form>
    </div>
    <div class="auth-box" style="background-color: #f1f8e9;">
        <h3 style="color: #2e7d32; border-bottom-color: #c8e6c9;">📝 ĐĂNG KÝ TÀI KHOẢN MỚI</h3>
        <form method="POST" action="/register">
            <div class="form-group"><label>Tên đăng nhập mới:</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Mật khẩu:</label><input type="password" name="password" required></div>
            <div class="form-group"><label>Số điện thoại / Email liên hệ:</label><input type="text" name="contact" placeholder="Nhập SĐT hoặc Email để nhận thẻ qua Gmail" required></div>
            <button type="submit" style="background-color: #4caf50;">TẠO TÀI KHOẢN MỚI</button>
        </form>
    </div>
</div>
""" + DISCORD_BUTTON_TAG

DASHBOARD_HTML = BASE_CSS + """
<div class="navbar">
    """ + LOGO_HTML_TAG + """
    <div>
        <span>Xin chào: <b>{{ username }}</b> | Số dư: <b style="color:#28a745;">{{ balance }}đ</b></span>
        <a href="/logout" class="logout-btn">Đăng xuất</a>
    </div>
</div>

{% if msg %}<div class="container" style="color: blue; font-weight: bold; text-align: center; margin-bottom: 10px; border: 1px solid blue; padding: 10px;">{{ msg }}</div>{% endif %}
{% if error %}<div class="container" style="color: red; font-weight: bold; text-align: center; margin-bottom: 10px; border: 1px solid red; padding: 10px;">{{ error }}</div>{% endif %}

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
    <h2>2. CHỌN LOẠI THẺ CẦN MUA (ADMIN DUYỆT GỬI QUA GMAIL)</h2>
    <div class="card-grid">
        {% for key, val in card_types.items() %}
        <a href="/buy/{{ key }}" class="card-item" style="background-color: {{ val.color }};">
            <div style="font-size: 20px; margin-bottom: 5px;">🛒</div>
            Mua {{ val.name }}
        </a>
        {% endfor %}
    </div>
</div>

<div class="container">
    <h2>3. LỊCH SỬ ĐỔI THẺ (NẠP TIỀN VÀO WEB)</h2>
    <table>
        <tr><th>Loại thẻ</th><th>Mệnh giá</th><th>Thông tin thẻ</th><th>Trạng thái</th></tr>
        {% for c in deposit_cards %}
        <tr>
            <td>{{ c.type.upper() }}</td><td>{{ c.amount }}đ</td>
            <td>S: {{ c.serial }} <br> M: {{ c.code }}</td>
            <td><span class="badge {% if c.status=='Chờ duyệt' %}bg-warning{% elif c.status=='Thành công' %}bg-success{% else %}bg-danger{% endif %}">{{ c.status }}</span></td>
        </tr>
        {% endfor %}
    </table>
</div>

<div class="container">
    <h2>4. ĐƠN ĐẶT MUA THẺ CỦA BẠN (ĐỢI ADMIN GỬI QUA GMAIL)</h2>
    <table>
        <tr><th>Loại thẻ mua</th><th>Mệnh giá</th><th>Trạng thái đơn hàng</th></tr>
        {% for c in buy_cards %}
        <tr>
            <td><b style="color:blue;">{{ c.type.upper() }}</b></td><td>{{ c.amount }}đ</td>
            <td>
                <span class="badge {% if c.status=='Chờ xử lý' %}bg-warning{% elif c.status=='Đã gửi thẻ' %}bg-success{% else %}bg-danger{% endif %}">
                    {{ c.status }}
                </span>
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
""" + DISCORD_BUTTON_TAG

BUY_CARD_HTML = BASE_CSS + """
<div class="navbar">
    """ + LOGO_HTML_TAG + """
    <div>
        <span>Xin chào: <b>{{ username }}</b> | Số dư: <b style="color:#28a745;">{{ balance }}đ</b></span>
        <a href="/dashboard" style="color: #2196F3; text-decoration: none; font-weight: bold; margin-left: 15px;">Quay lại</a>
    </div>
</div>
<div class="container" style="max-width: 500px;">
    <h2>🛒 ĐẶT MUA THẺ CÀO</h2>
    <p>Bạn đang chọn đặt mua: <b style="color: {{ card_info.color }}; font-size: 16px;">{{ card_info.name }}</b></p>
    <p style="color: #ef6c00; font-size: 13px;">⚠️ <i>Sau khi bạn xác nhận mua, Admin sẽ kiểm tra và gửi mã thẻ trực tiếp vào liên hệ/Gmail đăng ký tài khoản của bạn.</i></p>
    
    <form method="POST" action="/process-buy/{{ card_key }}">
        <div class="form-group">
            <label>Chọn mệnh giá cần mua:</label>
            <select name="buy_amount">
                {% for d in denominations %}
                <option value="{{ d }}">{{ d }}đ</option>
                {% endfor %}
            </select>
        </div>
        <button type="submit" style="background-color: {{ card_info.color }};">XÁC NHẬN ĐẶT MUA</button>
    </form>
</div>
""" + DISCORD_BUTTON_TAG

ADMIN_HTML = """
<head><meta name="robots" content="noindex, nofollow"></head>
""" + BASE_CSS + """
<div class="navbar">
    """ + LOGO_HTML_TAG + """
    <div>
        <span style="font-weight:bold; color:red;">[QUẢN TRỊ VIÊN]</span>
        <a href="/logout" class="logout-btn">Đăng xuất</a>
    </div>
</div>
<div class="container" style="max-width: 950px; margin-top:20px;">
    <h2>🔒 TRANG QUẢN TRỊ ADMIN</h2>
    
    <div style="background: #eef2f7; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #ccc;">
        <h3>🔍 TRA CỨU SỐ DƯ TÀI KHOẢN</h3>
        <form method="GET" action="/secret-admin-panel">
            <div style="display: flex; gap: 10px;">
                <input type="text" name="search_user" placeholder="Nhập chính xác tên tài khoản..." value="{{ search_keyword }}" required>
                <button type="submit" style="background: #2196F3; width: auto; padding: 0 25px;">Tìm Kiếm</button>
            </div>
        </form>
        
        {% if search_keyword %}
            <div style="margin-top: 15px; background: white; padding: 15px; border-radius: 6px; border: 1px dashed #2196F3; position: relative;">
                <div style="position: absolute; top: 10px; right: 15px;">
                    <a href="/secret-admin-panel" class="btn-close">❌ Đóng kết quả</a>
                </div>
                {% if search_result %}
                    <p style="margin: 5px 0;">👤 Tên tài khoản: <b style="color:#2196F3; font-size:16px;">{{ search_result.username }}</b></p>
                    <p style="margin: 5px 0;">💰 Số dư tài khoản: <b style="color:#28a745; font-size:16px;">{{ search_result.balance }}đ</b></p>
                    <p style="margin: 5px 0;">📞 Thông tin liên hệ/Gmail: <b style="color:red;">{{ search_result.contact }}</b></p>
                {% else %}
                    <p style="color: red; margin: 0; font-weight: bold;">❌ Không tìm thấy người dùng: "{{ search_keyword }}"</p>
                {% endif %}
            </div>
        {% endif %}
    </div>

    <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 30px;">
        <h3>🎁 GIFT TIỀN HỆ THỐNG</h3>
        <form method="POST" action="/admin/gift">
            <input type="text" name="gift_username" placeholder="Tên tài khoản..." required>
            <input type="number" name="gift_amount" placeholder="Số tiền..." required>
            <button type="submit" style="background: #ff9800; margin-top: 5px;">XÁC NHẬN GIFT</button>
        </form>
    </div>
    
    <h3>🚨 DANH SÁCH THẺ CHỜ DUYỆT (KHI KHÁCH ĐỔI THẺ VÀO WEB)</h3>
    <table>
        <tr><th>Tài khoản</th><th>Loại</th><th>Mệnh giá</th><th>Seri</th><th>Mã</th><th>Trạng thái</th><th>Hành động</th></tr>
        {% for c in all_cards %}
        <tr>
            <td>{{ c.username }}</td><td>{{ c.type.upper() }}</td><td>{{ c.amount }}đ</td><td>{{ c.serial }}</td><td>{{ c.code }}</td>
            <td><span class="badge bg-warning">{{ c.status }}</span></td>
            <td>
                <a href="/admin/approve/{{ c.id }}" style="color:green; font-weight:bold;">[ĐÚNG - CỘNG TIỀN]</a> | 
                <a href="/admin/reject/{{ c.id }}" style="color:red; font-weight:bold;">[LỖI]</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    
    <br><br>
    <h3 style="color:#ef6c00;">🛒 ĐƠN KHÁCH ĐẶT MUA THẺ (BẠN HÃY GỬI GMAIL RỒI BẤM DUYỆT)</h3>
    <table style="border: 2px solid #ef6c00;">
        <tr style="background-color: #ffe0b2;"><th>Người mua</th><th>Liên hệ / Gmail nhận</th><th>Thẻ đặt mua</th><th>Mệnh giá</th><th>Trạng thái</th><th>Hành động xử lý bằng tay</th></tr>
        {% for b in all_bought_cards %}
        <tr>
            <td><b>{{ b.username }}</b></td>
            <td><b style="color:red;">{{ b.contact_info }}</b></td>
            <td><span class="badge bg-danger">{{ b.type.upper() }}</span></td>
            <td><b>{{ b.amount }}đ</b></td>
            <td><span class="badge bg-warning">{{ b.status }}</span></td>
            <td>
                <a href="/admin/complete-buy/{{ b.id }}" style="background:#28a745; color:white; padding:4px 8px; text-decoration:none; font-weight:bold; border-radius:4px;">
                    ✓ ĐÃ GỬI GMAIL XONG
                </a>
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
""" + DISCORD_BUTTON_TAG

@app.route('/')
def index():
    if 'username' in session: return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_HTML, msg=request.args.get('msg', ''), discord_link=DISCORD_LINK)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].strip()
    password = request.form['password']
    res = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
    if res.data:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('index', msg="Sai tài khoản hoặc mật khẩu!"))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'].strip()
    password = request.form['password']
    contact = request.form.get('contact', 'Không có').strip()
    
    check_exist = supabase.table("users").select("username").eq("username", username).execute()
    if check_exist.data:
        return redirect(url_for('index', msg="Tên đăng nhập này đã tồn tại!"))
    
    supabase.table("users").insert({"username": username, "password": password, "contact": contact, "balance": 0}).execute()
    session['username'] = username
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session: return redirect(url_for('index'))
    user = session['username']
    
    user_data = supabase.table("users").select("balance").eq("username", user).execute()
    balance = user_data.data[0]['balance'] if user_data.data else 0
    
    card_data = supabase.table("cards").select("*").eq("username", user).order("id", desc=True).execute()
    deposit_cards = [c for c in card_data.data if not c['type'].startswith("Mua")]
    buy_cards = [c for c in card_data.data if c['type'].startswith("Mua")]
    
    return render_template_string(DASHBOARD_HTML, username=user, balance=balance, deposit_cards=deposit_cards, buy_cards=buy_cards, card_types=CARD_TYPES, denominations=DENOMINATIONS, discord_link=DISCORD_LINK, msg=request.args.get('msg'), error=request.args.get('error'))

@app.route('/submit-card', methods=['POST'])
def submit_card():
    if 'username' not in session: return redirect(url_for('index'))
    supabase.table("cards").insert({
        'username': session['username'], 'type': request.form['card_type'],
        'amount': int(request.form['amount']), 'serial': request.form['serial'].strip(),
        'code': request.form['code'].strip(), 'status': 'Chờ duyệt'
    }).execute()
    return redirect(url_for('dashboard', msg="Gửi thẻ thành công! Vui lòng chờ Admin duyệt."))

@app.route('/buy/<string:card_key>')
def buy_card_page(card_key):
    if 'username' not in session: return redirect(url_for('index'))
    if card_key not in CARD_TYPES: return redirect(url_for('dashboard'))
    
    user = session['username']
    user_data = supabase.table("users").select("balance").eq("username", user).execute()
    balance = user_data.data[0]['balance'] if user_data.data else 0
    
    return render_template_string(BUY_CARD_HTML, username=user, balance=balance, card_key=card_key, card_info=CARD_TYPES[card_key], denominations=DENOMINATIONS, discord_link=DISCORD_LINK)

@app.route('/process-buy/<string:card_key>', methods=['POST'])
def process_buy(card_key):
    if 'username' not in session: return redirect(url_for('index'))
    user = session['username']
    buy_amount = int(request.form['buy_amount'])
    
    user_data = supabase.table("users").select("balance", "contact").eq("username", user).execute()
    if not user_data.data: return redirect(url_for('dashboard'))
    
    current_balance = user_data.data[0]['balance']
    user_contact = user_data.data[0]['contact'] or "Không có Gmail"
    
    if current_balance < buy_amount:
        return redirect(url_for('dashboard', error=f"Thất bại: Số dư tài khoản không đủ để đặt mua thẻ {buy_amount}đ!"))
        
    # Trừ tiền của khách ngay lập tức
    new_balance = current_balance - buy_amount
    supabase.table("users").update({"balance": new_balance}).eq("username", user).execute()
    
    # Tạo đơn mua ở trạng thái Chờ xử lý (Không cấp seri/code tự động nữa)
    supabase.table("cards").insert({
        'username': user, 'type': f"Mua {card_key.upper()}",
        'amount': buy_amount, 'serial': user_contact, 'code': 'Chờ Admin gửi bằng tay', 'status': 'Chờ xử lý'
    }).execute()
    
    return redirect(url_for('dashboard', msg=f"Đặt mua thẻ thành công! Vui lòng đợi Admin kiểm tra và gửi mã thẻ qua Gmail của bạn."))

@app.route('/secret-admin-panel')
def admin_panel():
    if 'username' not in session or session['username'] != ADMIN_USERNAME: return "Từ chối", 403
    search_keyword = request.args.get('search_user', '').strip()
    search_result = None
    if search_keyword:
        user_query = supabase.table("users").select("username", "balance", "contact").eq("username", search_keyword).execute()
        if user_query.data: search_result = user_query.data[0]
        
    # Thẻ nạp chờ duyệt
    all_cards = supabase.table("cards").select("*").eq("status", "Chờ duyệt").order(
