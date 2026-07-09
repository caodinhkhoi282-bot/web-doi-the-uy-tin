import os
from flask import Flask, render_template_string, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = "doitheuytin_sieucap"

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

BASE_CSS = """<style>
    body { background-color: #0d0e12; color: #e0e0e0; font-family: Arial, sans-serif; margin: 0; padding-bottom: 80px; }
    .navbar { background-color: #16181f; border-bottom: 2px solid #dfb76c; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; }
    .navbar-brand { display: flex; align-items: center; gap: 10px; text-decoration: none; }
    .brand-logo { width: 40px; height: 40px; border-radius: 50%; border: 2px solid #dfb76c; }
    .brand-name { font-size: 18px; color: #dfb76c; font-weight: bold; text-transform: uppercase; }
    .navbar a.logout-btn { color: #ff5252; text-decoration: none; font-weight: bold; margin-left: 15px; }
    .container { max-width: 750px; margin: 25px auto; padding: 25px; border-radius: 12px; background: #16181f; border: 1px solid #2d313f; }
    .auth-box { border: 1px solid #383d52; border-radius: 8px; padding: 20px; background: #1c1f2b; margin-bottom: 20px; }
    h2 { color: #dfb76c; border-left: 5px solid #dfb76c; padding-left: 10px; font-size: 18px; text-transform: uppercase; }
    h3 { color: #dfb76c; font-size: 16px; border-bottom: 1px solid #383d52; padding-bottom: 8px; margin-top: 0; }
    .form-group { margin-bottom: 15px; }
    label { display: block; margin-bottom: 5px; font-size: 14px; color: #b0b5c6; font-weight: bold; }
    input, select { width: 100%; padding: 12px; border: 1px solid #383d52; border-radius: 6px; box-sizing: border-box; background: #12141d; color: #fff; }
    button { background: linear-gradient(135deg, #dfb76c, #b8934b); color: #000; border: none; padding: 12px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 15px; }
    .card-item { text-align: center; color: white; font-weight: bold; text-decoration: none; padding: 15px; border-radius: 8px; display: block; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; background: #12141d; }
    th, td { border: 1px solid #2d313f; padding: 12px; font-size: 13px; }
    th { background-color: #1c1f2b; color: #dfb76c; }
    .badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .bg-warning { background-color: #ff9800; color: #000; }
    .bg-success { background-color: #4caf50; color: #fff; }
    .bg-danger { background-color: #f44336; color: #fff; }
    .discord-support-btn { position: fixed; bottom: 20px; right: 20px; background-color: #5865F2; color: white; text-decoration: none; padding: 12px 20px; border-radius: 50px; font-weight: bold; z-index: 9999; }
    
    .popup-overlay { position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.85); display: flex; justify-content: center; align-items: center; z-index: 10000; }
    .popup-box { width: 90%; max-width: 480px; background: #16181f; border: 2px solid #dfb76c; border-radius: 12px; overflow: hidden; box-shadow: 0 0 30px rgba(223,183,108,0.3); }
    .popup-body { position: relative; width: 100%; padding-top: 58%; background-image: url('https://woulf-professor-paradox-be-immune-to-gojos-infinite-void-v0-hlq9b8meylkc1.jpg'); background-size: cover; background-position: center; }
    .popup-text-layer { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.4); padding: 12px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; text-shadow: 1px 1px 3px #000, 0 0 6px rgba(0,191,255,0.8); font-weight: bold; }
    .popup-top-left { font-size: 11px; color: #00bfff; line-height: 1.3; }
    .popup-top-center { text-align: center; font-size: 11px; color: #fff; background: rgba(0,0,0,0.6); padding: 2px; border-radius: 4px; }
    .popup-top-right { text-align: right; font-size: 11px; color: #00bfff; line-height: 1.3; display: flex; flex-direction: column; align-items: flex-end; }
    .popup-logo-mini { width: 30px; height: 30px; border-radius: 50%; border: 1px solid #dfb76c; margin-top: 3px; }
    .popup-bottom-main { font-size: 16px; color: #00bfff; text-align: center; }
    .popup-btn-close { background: #000; color: #00bfff; border-top: 1px solid #2d313f; padding: 10px; text-align: center; cursor: pointer; font-weight: bold; text-transform: uppercase; }
</style>"""

NAV_LOGO = """<div class="navbar-brand"><img src="https://img.freepik.com/premium-vector/d-letter-logo-luxury-gold-color_755034-846.jpg" class="brand-logo"><span class="brand-name">doithecaouytinok.com</span></div>"""
DISCORD_TAG = """<a class="discord-support-btn" href="{{ discord_link }}" target="_blank">💬 Hỗ Trợ Discord</a>"""

POPUP_HTML = """
<div class="popup-overlay" id="announcementPopup">
    <div class="popup-box">
        <div class="popup-body">
            <div class="popup-text-layer">
                <div style="display: flex; justify-content: space-between; width: 100%;">
                    <div class="popup-top-left">cảm ơn vì đã đăng ký ủng hộ<br>và tin tưởng web<br>đây là web chính thức của<br>đổi thẻ cào uy tín ok</div>
                    <div class="popup-top-center">những web<br>link khác đều là giả mạo!</div>
                    <div class="popup-top-right">link chính thức<br><span style="font-size:10px; color:#fff;">https://web-i-th.onrender.com</span><img src="https://img.freepik.com/premium-vector/d-letter-logo-luxury-gold-color_755034-846.jpg" class="popup-logo-mini"></div>
                </div>
                <div style="width: 100%;">
                    <div style="font-size: 11px; color: #00bfff; line-height: 1.2; margin-bottom:5px;">web hoạt động 24/7 và có khả năng thường xuyên cập nhật</div>
                    <div class="popup-bottom-main">cre: đổi thẻ uy tín ok</div>
                </div>
            </div>
        </div>
        <div class="popup-btn-close" onclick="document.getElementById('announcementPopup').style.display='none'">bỏ qua</div>
    </div>
</div>"""

LOGIN_HTML = BASE_CSS + f"<div class='navbar'>{NAV_LOGO}</div>" + """
<div class="container" style="max-width: 500px; margin-top: 40px;">
    <h2 style="text-align: center; border: none; color: #dfb76c;">HỆ THỐNG ĐỔI THẺ CAO ĐIỆN TỬ</h2>
    {% if msg %}<div style="color: #ff5252; font-weight: bold; text-align: center; margin-bottom: 15px;">{{ msg }}</div>{% endif %}
    <div class="auth-box">
        <h3>🔑 ĐĂNG NHẬP</h3>
        <form method="POST" action="/login">
            <div class="form-group"><label>Tên đăng nhập:</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Mật khẩu:</label><input type="password" name="password" required></div>
            <button type="submit">ĐĂNG NHẬP</button>
        </form>
    </div>
    <div class="auth-box" style="background-color: #1a241b; border-color: #2e4d32;">
        <h3 style="color: #81c784;">📝 ĐĂNG KÝ TÀI KHOẢN</h3>
        <form method="POST" action="/register">
            <div class="form-group"><label>Tên đăng nhập mới:</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Mật khẩu:</label><input type="password" name="password" required></div>
            <div class="form-group"><label>SĐT / Email nhận thẻ:</label><input type="text" name="contact" placeholder="Nhập Gmail nhận thẻ" required></div>
            <button type="submit" style="background: linear-gradient(135deg, #4caf50, #388e3c); color: #fff;">TẠO TÀI KHOẢN MỚI</button>
        </form>
    </div>
</div>
""" + POPUP_HTML + DISCORD_TAG
DASHBOARD_HTML = BASE_CSS + f"<div class='navbar'>{NAV_LOGO}" + """
    <div><span>Xin chào: <b style="color:#dfb76c;">{{ username }}</b> | Số dư: <b style="color:#4caf50;">{{ balance }}đ</b></span><a href="/logout" class="logout-btn">Đăng xuất</a></div>
</div>
{% if msg %}<div class="container" style="color: #64b5f6; text-align: center;">{{ msg }}</div>{% endif %}
{% if error %}<div class="container" style="color: #ff5252; text-align: center;">{{ error }}</div>{% endif %}
<div class="container">
    <h2>1. GỬI THẺ CÀO (ĐỔI THÀNH TIỀN)</h2>
    <form method="POST" action="/submit-card">
        <div class="form-group"><label>Loại thẻ:</label><select name="card_type">{% for key, val in card_types.items() %}<option value="{{ key }}">{{ val.name }}</option>{% endfor %}</select></div>
        <div class="form-group"><label>Mệnh giá:</label><select name="amount">{% for d in denominations %}<option value="{{ d }}">{{ d }}đ</option>{% endfor %}</select></div>
        <div class="form-group"><label>Số Seri:</label><input type="text" name="serial" required></div>
        <div class="form-group"><label>Mã số thẻ:</label><input type="text" name="code" required></div>
        <button type="submit" style="background: linear-gradient(135deg, #4caf50, #388e3c); color:#fff;">GỬI THẺ DUYỆT</button>
    </form>
</div>
<div class="container">
    <h2>2. CHỌN LOẠI THẺ CẦN MUA</h2>
    <div class="card-grid">
        {% for key, val in card_types.items() %}
        <a href="/buy/{{ key }}" class="card-item" style="background-color: {{ val.color }};">Mua {{ val.name }}</a>
        {% endfor %}
    </div>
</div>
<div class="container">
    <h2>3. LỊCH SỬ ĐỔI THẺ</h2>
    <table>
        <tr><th>Loại thẻ</th><th>Mệnh giá</th><th>Thông tin</th><th>Trạng thái</th></tr>
        {% for c in deposit_cards %}
        <tr><td>{{ c.get('type','').upper() }}</td><td>{{ c.get('amount',0) }}đ</td><td>S: {{ c.get('serial','') }}<br>M: {{ c.get('code','') }}</td><td><span class="badge {% if c.get('status')=='Chờ duyệt' %}bg-warning{% elif c.get('status')=='Thành công' %}bg-success{% else %}bg-danger{% endif %}">{{ c.get('status','') }}</span></td></tr>
        {% endfor %}
    </table>
</div>
<div class="container">
    <h2>4. ĐƠN ĐẶT MUA THẺ CỦA BẠN</h2>
    <table>
        <tr><th>Loại thẻ</th><th>Mệnh giá</th><th>Trạng thái</th></tr>
        {% for c in buy_cards %}
        <tr><td><b style="color:#dfb76c;">{{ c.get('type','').upper() }}</b></td><td>{{ c.get('amount',0) }}đ</td><td><span class="badge {% if c.get('status')=='Chờ xử lý' %}bg-warning{% elif c.get('status')=='Đã gửi thẻ' %}bg-success{% else %}bg-danger{% endif %}">{{ c.get('status','') }}</span></td></tr>
        {% endfor %}
    </table>
</div>
""" + POPUP_HTML + DISCORD_TAG

BUY_CARD_HTML = BASE_CSS + f"<div class='navbar'>{NAV_LOGO}" + """
    <div><span>Xin chào: <b style="color:#dfb76c;">{{ username }}</b> | Số dư: <b style="color:#4caf50;">{{ balance }}đ</b></span><a href="/dashboard" style="margin-left:15px; text-decoration:none; color:#dfb76c;">Quay lại</a></div>
</div>
<div class="container" style="max-width: 500px;">
    <h2>🛒 ĐẶT MUA THẺ CÀO</h2>
    <p>Bạn chọn: <b style="color: {{ card_info.color }};">{{ card_info.name }}</b></p>
    <form method="POST" action="/process-buy/{{ card_key }}">
        <div class="form-group"><label>Chọn mệnh giá:</label><select name="buy_amount">{% for d in denominations %}<option value="{{ d }}">{{ d }}đ</option>{% endfor %}</select></div>
        <button type="submit" style="background-color: {{ card_info.color }}; color:#fff;">XÁC NHẬN MUA</button>
    </form>
</div>
""" + DISCORD_TAG

ADMIN_HTML = BASE_CSS + f"<div class='navbar'>{NAV_LOGO}<div><span style='color:#f44336; font-weight:bold;'>[ADMIN]</span><a href='/logout' class='logout-btn'>Đăng xuất</a></div></div>" + """
<div class="container" style="max-width: 950px;">
    <h2>🔒 TRANG QUẢN TRỊ ADMIN</h2>
    <div style="background: #1c1f2b; padding: 15px; border-radius: 8px; margin-bottom: 20px; border:1px solid #383d52;">
        <h3>🔍 TRA CỨU TÀI KHOẢaN</h3>
        <form method="GET" action="/secret-admin-panel"><div style="display:flex; gap:10px;"><input type="text" name="search_user" placeholder="Tên tài khoản..." value="{{ search_keyword }}" required><button type="submit" style="width:auto;">Tìm</button></div></form>
        {% if search_keyword %}
            <p style="margin-top:10px;">+ {% if search_result %} 👤 Tên: <b>{{ search_result.get('username') }}</b> | 💰 Số dư: <b style="color:#4caf50;">{{ search_result.get('balance') }}đ</b> | 📞 Gmail: <b>{{ search_result.get('contact') }}</b>{% else %} Không thấy user: "{{ search_keyword }}"{% endif %} <a href="/secret-admin-panel" style="color:#ff5252; margin-left:10px;">✖ Đóng</a></p>
        {% endif %}
    </div>
    <div style="background: #2a2115; padding: 15px; border-radius: 8px; margin-bottom: 20px; border:1px solid #ff9800;">
        <h3>🎁 GIFT TIỀN</h3>
        <form method="POST" action="/admin/gift"><input type="text" name="gift_username" placeholder="User..." required><input type="number" name="gift_amount" placeholder="Tiền..." required><button type="submit" style="background:#ff9800; color:#000; margin-top:10px;">GIFT TIỀN</button></form>
    </div>
    <h3>🚨 THẺ CHỜ DUYỆT ĐỔI VÀO</h3>
    <table>
        <tr><th>User</th><th>Loại</th><th>Mệnh giá</th><th>Seri/Mã</th><th>Hành động</th></tr>
        {% for c in all_cards %}
        <tr><td>{{ c.get('username','Ẩn danh') }}</td><td>{{ c.get('type','').upper() }}</td><td>{{ c.get('amount',0) }}đ</td><td>S: {{ c.get('serial','') }}<br>M: {{ c.get('code','') }}</td><td><a href="/admin/approve/{{ c.get('id') }}" style="color:#4caf50; font-weight:bold;">[ĐÚNG]</a> | <a href="/admin/reject/{{ c.get('id') }}" style="color:#f44336; font-weight:bold;">[SAI]</a></td></tr>
        {% endfor %}
    </table>
    <br><h3>🛒 ĐƠN KHÁCH ĐẶT MUA THẺ</h3>
    <table>
        <tr><th>Người mua</th><th>Gmail nhận</th><th>Thẻ mua</th><th>Mệnh giá</th><th>Xử lý</th></tr>
        {% for b in all_bought_cards %}
        <tr><td>{{ b.get('username','Ẩn danh') }}</td><td style="color:#ff5252; font-weight:bold;">{{ b.get('contact_info','') }}</td><td>{{ b.get('type','').upper() }}</td><td>{{ b.get('amount',0) }}đ</td><td><a href="/admin/complete-buy/{{ b.get('id') }}" style="background:#4caf50; color:white; padding:6px 10px; text-decoration:none; border-radius:4px; font-weight:bold;">✓ ĐÃ GỬI</a></td></tr>
        {% endfor %}
    </table>
</div>
""" + DISCORD_TAG

@app.route('/')
def index():
    if 'username' in session: return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_HTML, discord_link=DISCORD_LINK, msg=request.args.get('msg', ''))

@app.route('/login', methods=['POST'])
def login():
    u, p = request.form['username'].strip(), request.form['password']
    res = supabase.table("users").select("*").eq("username", u).eq("password", p).execute()
    if res.data: session['username'] = u; return redirect(url_for('dashboard'))
    return redirect(url_for('index', msg="Sai tài khoản hoặc mật khẩu!"))

@app.route('/register', methods=['POST'])
def register():
    u, p, c = request.form['username'].strip(), request.form['password'], request.form.get('contact', '').strip()
    if supabase.table("users").select("username").eq("username", u).execute().data:
        return redirect(url_for('index', msg="Tên đăng nhập đã tồn tại!"))
    supabase.table("users").insert({"username": u, "password": p, "contact": c, "balance": 0}).execute()
    session['username'] = u; return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session: return redirect(url_for('index'))
    u = session['username']
    u_data = supabase.table("users").select("balance").eq("username", u).execute()
    bal = u_data.data[0]['balance'] if u_data.data else 0
    c_data = supabase.table("cards").select("*").eq("username", u).order("id", desc=True).execute()
    dep = [c for c in c_data.data if c.get('type') and not c['type'].startswith("Mua")] if c_data.data else []
    buy = [c for c in c_data.data if c.get('type') and c['type'].startswith("Mua")] if c_data.data else []
    return render_template_string(DASHBOARD_HTML, username=u, balance=bal, deposit_cards=dep, buy_cards=buy, card_types=CARD_TYPES, denominations=DENOMINATIONS, discord_link=DISCORD_LINK, msg=request.args.get('msg'), error=request.args.get('error'))

@app.route('/submit-card', methods=['POST'])
def submit_card():
    if 'username' not in session: return redirect(url_for('index'))
    supabase.table("cards").insert({'username': session['username'], 'type': request.form['card_type'], 'amount': int(request.form['amount']), 'serial': request.form['serial'].strip(), 'code': request.form['code'].strip(), 'status': 'Chờ duyệt'}).execute()
    return redirect(url_for('dashboard', msg="Gửi thẻ thành công! Vui lòng chờ duyệt."))

@app.route('/buy/<string:card_key>')
def buy_card_page(card_key):
    if 'username' not in session or card_key not in CARD_TYPES: return redirect(url_for('index'))
    u = session['username']
    u_data = supabase.table("users").select("balance").eq("username", u).execute()
    return render_template_string(BUY_CARD_HTML, username=u, balance=u_data.data[0]['balance'] if u_data.data else 0, card_key=card_key, card_info=CARD_TYPES[card_key], denominations=DENOMINATIONS, discord_link=DISCORD_LINK)

@app.route('/process-buy/<string:card_key>', methods=['POST'])
def process_buy(card_key):
    if 'username' not in session: return redirect(url_for('index'))
    u, amt = session['username'], int(request.form['buy_amount'])
    ud = supabase.table("users").select("balance", "contact").eq("username", u).execute()
    if not ud.data or ud.data[0]['balance'] < amt: return redirect(url_for('dashboard', error="Số dư không đủ!"))
    supabase.table("users").update({"balance": ud.data[0]['balance'] - amt}).eq("username", u).execute()
    supabase.table("cards").insert({'username': u, 'type': f"Mua {card_key.upper()}", 'amount': amt, 'serial': ud.data[0]['contact'] or "Không có", 'code': 'Chờ nhận tay', 'status': 'Chờ xử lý'}).execute()
    return redirect(url_for('dashboard', msg="Đặt mua thành công! Hãy chờ nhận qua Gmail."))

@app.route('/secret-admin-panel')
def admin_panel():
    if 'username' not in session or session['username'] != ADMIN_USERNAME: return "Từ chối", 403
    kw = request.args.get('search_user', '').strip()
    res = supabase.table("users").select("username", "balance", "contact").eq("username", kw).execute().data[0] if kw and supabase.table("users").select("username").eq("username", kw).execute().data else None
    all_c = supabase.table("cards").select("*").eq("status", "Chờ duyệt").order("id", desc=True).execute().data or []
    buy_o = supabase.table("cards").select("*").eq("status", "Chờ xử lý").order("id", desc=True).execute().data or []
    all_b = [{'id': b.get('id'), 'username': b.get('username', 'Ẩn danh'), 'type': b.get('type',''), 'amount': b.get('amount',0), 'contact_info': b.get('serial', 'Không có'), 'status': b.get('status','')} for b in buy_o]
    return render_template_string(ADMIN_HTML, all_cards=all_c, all_bought_cards=all_b, search_keyword=kw, search_result=res, discord_link=DISCORD_LINK)

@app.route('/admin/complete-buy/<int:order_id>')
def admin_complete_buy(order_id):
    if 'username' in session and session['username'] == ADMIN_USERNAME: supabase.table("cards").update({"status": "Đã gửi thẻ", "code": "Đã gửi Gmail"}).eq("id", order_id).execute()
    return redirect('/secret-admin-panel')

@app.route('/admin/gift', methods=['POST'])
def admin_gift():
    if 'username' not in session or session['username'] != ADMIN_USERNAME: return "Từ chối", 403
    t, amt = request.form['gift_username'].strip(), int(request.form['gift_amount'])
    ud = supabase.table("users").select("balance").eq("username", t).execute()
    if ud.data: supabase.table("users").update({"balance": ud.data[0]['balance'] + amt}).eq("username", t).execute()
    return redirect('/secret-admin-panel')

@app.route('/admin/approve/<int:card_id>')
def admin_approve(card_id):
    if 'username' not in session or session['username'] != ADMIN_USERNAME: return "Từ chối", 403
    c = supabase.table("cards").select("*").eq("id", card_id).execute()
    if c.data and c.data[0]['status'] == 'Chờ duyệt':
        supabase.table("cards").update({"status": "Thành công"}).eq("id", card_id).execute()
        u = c.data[0].get('username')
        if u:
            ud = supabase.table("users").select("balance").eq("username", u).execute()
            if ud.data: supabase.table("users").update({"balance": ud.data[0]['balance'] + c.data[0]['amount']}).eq("username", u).execute()
    return redirect('/secret-admin-panel')

@app.route('/admin/reject/<int:card_id>')
def admin_reject(card_id):
    if 'username' in session and session['username'] == ADMIN_USERNAME: supabase.table("cards").update({"status": "Thẻ lỗi/Sai mã"}).eq("id", card_id).execute()
    return redirect('/secret-admin-panel')

@app.route('/logout')
def logout(): session.pop('username', None); return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
