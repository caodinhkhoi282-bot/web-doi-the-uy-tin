import os
from flask import Flask, session, request, redirect, url_for, render_template_string, Response

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key-12345")

ADMIN_USERNAME = "admin"
DENOMINATIONS = [10000, 20000, 30000, 50000, 100000, 200000, 300000, 500000, 1000000]
COUPONS = {
    "NEWBIE": {"type": "newbie", "discount": 5000},
    "FANCUNG": {"type": "fancung", "discount": 10000}
}
CARD_TYPES = {
    "viettel": {"name": "Viettel", "img": "https://openclipart.org/image/800px/278555"},
    "vinaphone": {"name": "Vinaphone", "img": "https://openclipart.org/image/800px/278555"},
    "mobifone": {"name": "Mobifone", "img": "https://openclipart.org/image/800px/278555"},
    "garena": {"name": "Garena", "img": "https://openclipart.org/image/800px/278555"}
}
GAMES = {
    "lienquan": {"name": "Liên Quân Mobile", "img": "", "placeholder": "Nhập OpenID/Tài khoản", "rates": {20000: "Gói 1", 50000: "Gói 2"}}
}

from supabase import create_client
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://your-supabase-url.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "your-supabase-key")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BASE_CSS = """<style>
body { background: #0d0f14; color: #fff; font-family: Arial, sans-serif; margin: 0; padding: 0; }
.navbar { background: #141722; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #232838; }
.navbar-brand { display: flex; align-items: center; gap: 8px; }
.brand-logo { height: 30px; }
.brand-name { font-weight: bold; color: #dfb76c; }
.user-info-area { font-size: 12px; text-align: right; }
.logout-btn { color: #ff5252; text-decoration: none; margin-left: 8px; font-weight: bold; }
.layout-wrapper { display: flex; max-width: 1200px; margin: 20px auto; gap: 20px; padding: 0 15px; }
.sidebar-menu { width: 250px; display: flex; flex-direction: column; gap: 10px; }
.main-content { flex: 1; }
.tab-btn { background: #1c1f2b; border: 1px solid #383d52; color: #fff; padding: 12px; text-align: left; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; }
.tab-btn.active { background: #dfb76c; color: #000; border-color: #dfb76c; }
.container { background: #141722; border: 1px solid #232838; padding: 20px; border-radius: 8px; display: none; }
.container.active { display: block; }
.auth-box { max-width: 400px; margin: 40px auto; background: #141722; border: 1px solid #232838; padding: 20px; border-radius: 8px; }
.form-group { margin-bottom: 15px; text-align: left; }
.form-group label { display: block; font-size: 13px; margin-bottom: 5px; color: #ccc; }
.form-group input, .form-group select { width: 100%; padding: 10px; background: #1c1f2b; border: 1px solid #383d52; color: #fff; border-radius: 6px; box-sizing: border-box; }
button[type="submit"] { width: 100%; padding: 12px; background: #dfb76c; border: none; color: #000; font-weight: bold; border-radius: 6px; cursor: pointer; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; margin-bottom: 15px; }
.card-select-box, .card-item-btn { background: #1c1f2b; border: 1px solid #383d52; padding: 10px; text-align: center; border-radius: 6px; cursor: pointer; text-decoration: none; color: #fff; }
.card-select-box.selected { border-color: #dfb76c; background: #24241e; }
.card-select-box input { display: none; }
.card-logo-img { height: 25px; object-fit: contain; }
.card-label-name { font-size: 11px; display: block; margin-top: 4px; }
.table-responsive { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
th, td { border: 1px solid #232838; padding: 10px; text-align: left; }
th { background: #1c1f2b; color: #dfb76c; }
.badge { padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }
.bg-warning { background: #ff9800; color: #000; }
.bg-success { background: #4caf50; color: #fff; }
.bg-danger { background: #f44336; color: #fff; }
.support-circle-btn { position: fixed; bottom: 20px; right: 20px; background: #2196f3; color: #fff; padding: 10px 15px; border-radius: 50px; display: flex; align-items: center; gap: 6px; text-decoration: none; font-weight: bold; font-size: 13px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); z-index: 9999; }
.support-circle-btn svg { width: 18px; height: 18px; fill: #fff; }
.popup-overlay { position: fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); display:flex; align-items:center; justify-content:center; z-index:10000; }
.popup-box { background:#141722; border:1px solid #dfb76c; padding:20px; border-radius:8px; max-width:400px; width:90%; text-align:center; }
.popup-btn-close { margin-top:15px; background:#dfb76c; color:#000; padding:8px; border-radius:4px; font-weight:bold; cursor:pointer; font-size:12px; }
@media (max-width: 768px) { .layout-wrapper { flex-direction: column; } .sidebar-menu { width: 100%; flex-direction: row; overflow-x: auto; } .sidebar-menu button { white-space: nowrap; width: auto; } }
</style>
<script>
function openTab(evt, tabName) {
    var i, container, tab_btn;
    container = document.getElementsByClassName("container");
    for (i = 0; i < container.length; i++) { container[i].style.display = "none"; container[i].classList.remove("active"); }
    tab_btn = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tab_btn.length; i++) { tab_btn[i].classList.remove("active"); }
    document.getElementById(tabName).style.display = "block";
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}
function selectCard(box, radioId) {
    var boxes = document.getElementsByClassName("card-select-box");
    for (var i = 0; i < boxes.length; i++) { boxes[i].classList.remove("selected"); }
    box.classList.add("selected");
    document.getElementById(radioId).checked = true;
}
</script>
"""

SUPPORT_LINK = "https://zalo.me/your-profile"
NAV_LOGO = """<div class="navbar-brand"><img src="https://openclipart.org/image/800px/278555" class="brand-logo"><span class="brand-name">doithecaouytinok.com</span></div>"""
SUPPORT_BALLOON = f"""<a class="support-circle-btn" href="{SUPPORT_LINK}" target="_blank"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12v7c0 1.1.9 2 2 2h3v-8H4v-1c0-4.41 3.59-8 8-8s8 3.59 8 8v1h-3v8h3c1.1 0 2-.9 2-2v-7c0-5.52-4.48-10-10-10z"/></svg><span>Hỗ Trợ</span></a>"""

POPUP_HTML = """
<div class="popup-overlay" id="announcementPopup">
    <div class="popup-box">
        <div class="popup-body">
            <div class="popup-text-layer">
                <div style="display: flex; justify-content: space-between; width: 100%; font-size: 9px;">
                    <div style="color: #00bfff;">Cảm ơn vì đã đăng ký ủng hộ<br>và tin tưởng web hệ thống chính thức</div>
                    <div style="text-align: right; color: #ffeb3b;">Link độc quyền:<br><span style="color:#fff;">onrender.com</span></div>
                </div>
                <div class="popup-bottom-main" style="font-size: 12px; color: #dfb76c; text-align: center; text-transform: uppercase;">CRE: ĐỔI THẺ UY TÍN OK</div>
            </div>
        </div>
        <div class="popup-btn-close" onclick="document.getElementById('announcementPopup').style.display='none'">BỎ QUA THÔNG BÁO</div>
    </div>
</div>"""

LOGIN_HTML = BASE_CSS + f"<div class='navbar'>{NAV_LOGO}</div>" + """
<div style="max-width:600px; text-align:center; margin: 15px auto 5px auto; padding: 0 10px;"><h1 style='font-size:15px; color:#dfb76c; margin:0;'>HỆ THỐNG ĐỔI THẺ CAO ĐIỆN TỬ UY TÍN</h1></div>
{% if msg %}<div style="max-width:500px; margin:0 auto; color: #ff5252; font-weight: bold; text-align: center; margin-bottom: 10px; font-size:12px;">{{ msg }}</div>{% endif %}
<div class="layout-wrapper">
    <div class="sidebar-menu">
        <button class="tab-btn active" onclick="openTab(event, 'tabLogin')">🔑 ĐĂNG NHẬP</button>
        <button class="tab-btn" onclick="openTab(event, 'tabRegister')">📝 ĐĂNG KÝ</button>
    </div>
    <div class="main-content">
        <div id="tabLogin" class="container active">
            <div class="auth-box">
                <h3>🔑 ĐĂNG NHẬP HỆ THỐNG</h3>
                <form method="POST" action="/login">
                    <div class="form-group"><label>Tên đăng nhập:</label><input type="text" name="username" required></div>
                    <div class="form-group"><label>Mật khẩu:</label><input type="password" name="password" required></div>
                    <button type="submit">ĐĂNG NHẬP NGAY</button>
                </form>
            </div>
        </div>
        <div id="tabRegister" class="container">
            <div class="auth-box" style="border-color: #2e4d32;">
                <h3 style="color: #81c784;">📝 TẠO TÀI KHOẢN MỚI</h3>
                <form method="POST" action="/register">
                    <div class="form-group"><label>Tên đăng nhập mới:</label><input type="text" name="username" required></div>
                    <div class="form-group"><label>Mật khẩu bảo mật:</label><input type="password" name="password" required></div>
                    <div class="form-group"><label>Gmail nhận thẻ cào:</label><input type="text" name="contact" placeholder="Nhập Gmail chính chủ" required></div>
                    <button type="submit" style="background: linear-gradient(135deg, #4caf50, #388e3c); color: #fff;">XÁC NHẬN ĐĂNG KÝ</button>
                </form>
            </div>
        </div>
    </div>
</div>
""" + SUPPORT_BALLOON
DASHBOARD_HTML = BASE_CSS + f"<div class='navbar'>{NAV_LOGO}" + """
    <div class="user-info-area"><div>👤: <b style="color:#dfb76c;">{{ username }}</b><br>💰: <b style="color:#4caf50;">{{ balance }}đ</b></div><a href="/logout" class="logout-btn">Thoát</a></div>
</div>
{% if msg %}<div style="max-width:1200px; margin: 8px auto; padding: 0 10px; color: #64b5f6; font-size:12px; font-weight:bold; text-align:center;">{{ msg }}</div>{% endif %}
{% if error %}<div style="max-width:1200px; margin: 8px auto; padding: 0 10px; color: #ff5252; font-size:12px; font-weight:bold; text-align:center;">{{ error }}</div>{% endif %}
<div class="layout-wrapper">
    <div class="sidebar-menu">
        <button class="tab-btn active" onclick="openTab(event, 'tabDoiThe')">💳 ĐỔI THẺ CÀO</button>
        <button class="tab-btn" onclick="openTab(event, 'tabMuaThe')">🛒 MUA THẺ CÀO</button>
        <button class="tab-btn" onclick="openTab(event, 'tabNapGame')">🎮 NẠP GAME TỰ ĐỘNG</button>
        <button class="tab-btn" onclick="openTab(event, 'tabLichSu')">📜 LỊCH SỬ</button>
    </div>
    <div class="main-content">
        <div id="tabDoiThe" class="container active">
            <h2>1. GỬI THẺ CÀO (ĐỔI THÀNH TIỀN MẶT)</h2>
            <form method="POST" action="/submit-card">
                <div class="form-group">
                    <label>Chọn nhà mạng:</label>
                    <div class="card-grid">
                        {% for key, val in card_types.items() %}
                        <div class="card-select-box {% if loop.first %}selected{% endif %}" onclick="selectCard(this, 'radio_dep_{{ key }}')">
                            <input type="radio" name="card_type" value="{{ key }}" id="radio_dep_{{ key }}" {% if loop.first %}checked{% endif %}>
                            <img src="{{ val.img }}" class="card-logo-img" onerror="this.src='https://openclipart.org/image/800px/278555'"><br>
                            <span class="card-label-name">{{ val.name }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                <div class="form-group"><label>Mệnh giá thẻ:</label><select name="amount">{% for d in denominations %}<option value="{{ d }}">{{ d }}đ</option>{% endfor %}</select></div>
                <div class="form-group"><label>Mã số Seri:</label><input type="text" name="serial" placeholder="Nhập chuẩn xác mã Seri" required></div>
                <div class="form-group"><label>Mã số thẻ (sau lớp cào):</label><input type="text" name="code" placeholder="Nhập chính xác mã thẻ" required></div>
                <button type="submit" style="background: linear-gradient(135deg, #4caf50, #388e3c); color:#fff;">GỬI THẺ DUYỆT NGAY</button>
            </form>
        </div>
        <div id="tabMuaThe" class="container">
            <h2>2. CHỌN LOẠI THẺ CẦN MUA (GỬI QUA GMAIL)</h2>
            <div class="card-grid">
                {% for key, val in card_types.items() %}
                <a href="/buy/{{ key }}" class="card-item-btn">
                    <img src="{{ val.img }}" class="card-logo-img" onerror="this.src='https://openclipart.org/image/800px/278555'">
                    <span>Mua {{ val.name }}</span>
                </a>
                {% endfor %}
            </div>
        </div>
        <div id="tabNapGame" class="container">
            <h2>🎮 HỆ THỐNG NẠP GAME TỰ ĐỘNG GIÁ RẺ</h2>
            <div style="display: grid; grid-template-columns: 1fr; gap: 12px;">
                {% for g_key, g_val in games.items() %}
                <div style="background:#1c1f2b; border:1px solid #383d52; padding:12px; border-radius:8px; display: flex; flex-direction: column; align-items: center;">
                    <img src="{{ g_val.img }}" style="height:40px; object-fit:contain; margin-bottom:6px;">
                    <div style="font-weight:bold; margin-bottom:6px; color:#dfb76c; font-size:13px;">{{ g_val.name }}</div>
                    <form method="POST" action="/process-game/{{ g_key }}" style="width:100%;">
                        <div class="form-group"><select name="game_pack">{% for price, reward in g_val.rates.items() %}<option value="{{ price }}">{{ price }}đ = {{ reward }}</option>{% endfor %}</select></div>
                        <div class="form-group"><input type="text" name="game_info" placeholder="{{ g_val.placeholder }}" required></div>
                        <div class="form-group"><input type="text" name="coupon" placeholder="Mã giảm giá (nếu có)"></div>
                        <button type="submit">NẠP TIẾN HÀNH</button>
                    </form>
                </div>
                {% endfor %}
            </div>
        </div>
        <div id="tabLichSu" class="container">
            <h2>📜 LỊCH SỬ ĐỔI THẺ</h2>
            <div class="table-responsive">
                <table>
                    <tr><th>Loại thẻ</th><th>Mệnh giá</th><th>Thông tin</th><th>Trạng thái</th></tr>
                    {% for c in deposit_cards %}
                    <tr><td>{{ c.get('type','').upper() }}</td><td>{{ c.get('amount',0) }}đ</td><td>S: {{ c.get('serial','') }}<br>M: {{ c.get('code','') }}</td><td><span class="badge {% if c.get('status')=='Chờ duyệt' %}bg-warning{% elif c.get('status')=='Thành công' %}bg-success{% else %}bg-danger{% endif %}">{{ c.get('status','') }}</span></td></tr>
                    {% endfor %}
                </table>
            </div>
            <br><h2>📜 ĐƠN MUA THẺ & ĐƠN NẠP GAME</h2>
            <div class="table-responsive">
                <table>
                    <tr><th>Loại đơn</th><th>Giá gốc</th><th>Thông tin tài khoản</th><th>Trạng thái</th></tr>
                    {% for c in buy_cards %}
                    <tr><td><b>{{ c.get('type','').upper() }}</b></td><td>{{ c.get('amount',0) }}đ</td><td>{{ c.get('serial','') }}</td><td><span class="badge {% if c.get('status')=='Chờ xử lý' %}bg-warning{% elif c.get('status')=='Đã gửi thẻ' %}bg-success{% else %}bg-danger{% endif %}">{{ c.get('status','') }}</span></td></tr>
                    {% endfor %}
                </table>
            </div>
        </div>
    </div>
</div>
""" + POPUP_HTML + SUPPORT_BALLOON
BUY_CARD_HTML = BASE_CSS + f"<div class='navbar'>{NAV_LOGO}" + """
    <div class="user-info-area"><span>👤: <b>{{ username }}</b></span><a href="/dashboard" style="color:#dfb76c; text-decoration:none; font-weight:bold; font-size:12px;">[Quay lại]</a></div>
</div>
<div class="container active" style="max-width: 400px; margin:15px auto; padding:12px;">
    <h2>🛒 XÁC NHẬN MUA THẺ CÀO</h2>
    <div style="text-align:center; padding:8px; background:#fff; border-radius:8px; margin-bottom:12px;"><img src="{{ card_info.img }}" style="height:30px; object-fit:contain;" onerror="this.src='https://openclipart.org/image/800px/278555'"></div>
    <p style="font-size:13px;">Nhà mạng phân phối: <b style="color:#dfb76c;">{{ card_info.name }}</b></p>
    <form method="POST" action="/process-buy/{{ card_key }}">
        <div class="form-group"><label>Chọn mệnh giá mua:</label><select name="buy_amount">{% for d in denominations %}<option value="{{ d }}">{{ d }}đ</option>{% endfor %}</select></div>
        <button type="submit">THANH TOÁN MUA</button>
    </form>
</div>
""" + SUPPORT_BALLOON

ADMIN_HTML = BASE_CSS + f"<div class='navbar'>{NAV_LOGO}<div><span style='color:#f44336; font-weight:bold; font-size:11px;'>[ADMIN]</span><a href='/logout' class='logout-btn'>Thoát</a></div></div>" + """
<div class="container active" style="max-width: 950px; margin:15px auto; padding:12px;">
    <h2>🔒 CỔNG QUẢN TRỊ ADMIN</h2>
    <div style="background: #1c1f2b; padding: 10px; border-radius: 8px; margin-bottom: 12px; border:1px solid #383d52;">
        <h3>🔍 TRA CỨU NHANH TÀI KHOẢN</h3>
        <form method="GET" action="/secret-admin-panel"><div style="display:flex; gap:6px;"><input type="text" name="search_user" placeholder="Nhập tên user..." value="{{ search_keyword }}" required><button type="submit" style="width:auto; padding:0 12px;">Tìm</button></div></form>
        {% if search_keyword %}
            <p style="font-size:12px; margin-top:6px;">+ {% if search_result %} 👤 User: <b>{{ search_result.get('username') }}</b> | 💰 Ví: <b style="color:#4caf50;">{{ search_result.get('balance') }}đ</b>{% else %} Không tìm thấy khách hàng này!{% endif %} <a href="/secret-admin-panel" style="color:#ff5252; margin-left:8px; text-decoration:none;">[Đóng]</a></p>
        {% endif %}
    </div>
    <div style="background: #2a2115; padding: 10px; border-radius: 8px; margin-bottom: 12px; border:1px solid #ff9800;">
        <h3>🎁 CỘNG / TRỪ TIỀN HỆ THỐNG</h3>
        <form method="POST" action="/admin/gift"><div class="form-group"><input type="text" name="gift_username" placeholder="Tên tài khoản..." required></div><div class="form-group"><input type="number" name="gift_amount" placeholder="Số tiền cộng (Số âm nếu trừ)..." required></div><button type="submit" style="background:#ff9800; color:#000;">XÁC THỰC THAY ĐỔI</button></form>
    </div>
    <h3>🚨 THẺ CÀO CHỜ DUYỆT</h3>
    <div class="table-responsive">
        <table>
            <tr><th>Tài khoản</th><th>Loại thẻ</th><th>Mệnh giá</th><th>Seri / Mã</th><th>Hành động xử lý</th></tr>
            {% for c in all_cards %}
            <tr><td>{{ c.get('username') }}</td><td>{{ c.get('type','').upper() }}</td><td>{{ c.get('amount') }}đ</td><td>S: {{ c.get('serial') }}<br>M: {{ c.get('code') }}</td><td><a href="/admin/approve/{{ c.get('id') }}" style="color:#4caf50; font-weight:bold;">[ĐÚNG]</a> | <a href="/admin/reject/{{ c.get('id') }}" style="color:#f44336; font-weight:bold;">[SAI]</a></td></tr>
            {% endfor %}
        </table>
    </div>
    <br><h3>🛒 ĐƠN HÀNG CHỜ XỬ LÝ (MUA THẺ/GAME)</h3>
    <div class="table-responsive">
        <table>
            <tr><th>Khách</th><th>Liên hệ nhận đơn</th><th>Loại đơn</th><th>Mệnh giá</th><th>Hành động</th></tr>
            {% for b in all_bought_cards %}
            <tr><td>{{ b.get('username') }}</td><td style="color:#ff5252; font-weight:bold;">{{ b.get('contact_info') }}</td><td>{{ b.get('type').upper() }}</td><td>{{ b.get('amount') }}đ</td><td><a href="/admin/complete-buy/{{ b.get('id') }}" style="background:#4caf50; color:white; padding:4px 6px; text-decoration:none; border-radius:4px; font-weight:bold; font-size:10px;">✓ HOÀN TẤT</a></td></tr>
            {% endfor %}
        </table>
    </div>
</div>
""" + SUPPORT_BALLOON
@app.route('/robots.txt')
def robots():
    r = "User-agent: *\nAllow: /\nSitemap: https://web-i-th.onrender.com/sitemap.xml"
    return Response(r, mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    s = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://web-i-th.onrender.com/</loc><priority>1.0</priority></url></urlset>'
    return Response(s, mimetype='text/xml')

@app.route('/')
def index():
    if 'username' in session: return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_HTML, msg=request.args.get('msg', ''))

@app.route('/login', methods=['POST'])
def login():
    u, p = request.form['username'].strip(), request.form['password']
    res = supabase.table("users").select("*").eq("username", u).eq("password", p).execute()
    if res.data: session['username'] = u; return redirect(url_for('dashboard'))
    return redirect(url_for('index', msg="Sai tài khoản hoặc mật khẩu hệ thống!"))

@app.route('/register', methods=['POST'])
def register():
    u, p, c = request.form['username'].strip(), request.form['password'], request.form.get('contact', '').strip()
    if supabase.table("users").select("username").eq("username", u).execute().data:
        return redirect(url_for('index', msg="Tên tài khoản này đã tồn tại!"))
    supabase.table("users").insert({"username": u, "password": p, "contact": c, "balance": 0}).execute()
    session['username'] = u; return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session: return redirect(url_for('index'))
    u = session['username']
    u_data = supabase.table("users").select("balance").eq("username", u).execute()
    bal = u_data.data[0]['balance'] if u_data.data else 0
    c_data = supabase.table("cards").select("*").eq("username", u).order("id", desc=True).execute()
    dep = [c for c in c_data.data if c.get('type') and not (c['type'].startswith("Mua") or c['type'].startswith("Nạp"))] if c_data.data else []
    buy = [c for c in c_data.data if c.get('type') and (c['type'].startswith("Mua") or c['type'].startswith("Nạp"))] if c_data.data else []
    return render_template_string(DASHBOARD_HTML, username=u, balance=bal, deposit_cards=dep, buy_cards=buy, card_types=CARD_TYPES, denominations=DENOMINATIONS, games=GAMES, msg=request.args.get('msg'), error=request.args.get('error'))

@app.route('/submit-card', methods=['POST'])
def submit_card():
    if 'username' not in session: return redirect(url_for('index'))
    supabase.table("cards").insert({'username': session['username'], 'type': request.form['card_type'], 'amount': int(request.form['amount']), 'serial': request.form['serial'].strip(), 'code': request.form['code'].strip(), 'status': 'Chờ duyệt'}).execute()
    return redirect(url_for('dashboard', msg="Gửi thẻ cào thành công! Vui lòng chờ admin phê duyệt."))

@app.route('/buy/<string:card_key>')
def buy_card_page(card_key):
    if 'username' not in session or card_key not in CARD_TYPES: return redirect(url_for('index'))
    u = session['username']
    u_data = supabase.table("users").select("balance").eq("username", u).execute()
    return render_template_string(BUY_CARD_HTML, username=u, balance=u_data.data[0]['balance'] if u_data.data else 0, card_key=card_key, card_info=CARD_TYPES[card_key], denominations=DENOMINATIONS)

@app.route('/process-buy/<string:card_key>', methods=['POST'])
def process_buy(card_key):
    if 'username' not in session: return redirect(url_for('index'))
    u, amt = session['username'], int(request.form['buy_amount'])
    ud = supabase.table("users").select("balance", "contact").eq("username", u).execute()
    if not ud.data or ud.data[0]['balance'] < amt: return redirect(url_for('dashboard', error="Tài khoản của bạn không đủ số dư để mua!"))
    supabase.table("users").update({"balance": ud.data[0]['balance'] - amt}).eq("username", u).execute()
    supabase.table("cards").insert({'username': u, 'type': f"Mua {card_key.upper()}", 'amount': amt, 'serial': f"Gmail: {ud.data[0]['contact'] or 'Không có'}", 'code': 'Chờ nhận thẻ', 'status': 'Chờ xử lý'}).execute()
    return redirect(url_for('dashboard', msg="Đã đặt mua thẻ thành công! Hệ thống sẽ gửi mã vào Gmail của bạn."))

@app.route('/process-game/<string:game_key>', methods=['POST'])
def process_game(game_key):
    if 'username' not in session or game_key not in GAMES: return redirect(url_for('index'))
    u = session['username']
    g_info = GAMES[game_key]
    orig_amt = int(request.form.get('game_pack', 20000))
    reward_val = g_info['rates'].get(orig_amt, "Gói vip")
    g_user = request.form.get('game_info', '').strip()
    cp = request.form.get('coupon', '').strip().upper()
    ud = supabase.table("users").select("balance", "contact").eq("username", u).execute()
    if not ud.data: return redirect(url_for('dashboard', error="Tài khoản lỗi dữ liệu."))
    current_bal = ud.data[0]['balance']
    final_amt = orig_amt
    cp_info = ""
    
    if cp:
        if cp in COUPONS:
            c_type = COUPONS[cp]['type']
            discount_val = COUPONS[cp]['discount']
            all_u_tx = supabase.table("cards").select("id").eq("username", u).execute().data or []
            used_cp = supabase.table("cards").select("id").eq("username", u).like("serial", f"%Mã: {cp}%").execute().data or []
            if c_type == "newbie" and len(all_u_tx) <= 2 and len(used_cp) == 0:
                final_amt = max(0, orig_amt - discount_val)
                cp_info = f" | [Mã: {cp}]"
            elif c_type == "fancung":
                success_deposit = supabase.table("cards").select("id").eq("username", u).eq("status", "Thành công").execute().data or []
                if len(success_deposit) >= 5 and len(used_cp) < 10:
                    final_amt = max(0, orig_amt - discount_val)
                    cp_info = f" | [Mã: {cp}]"
                else: return redirect(url_for('dashboard', error="Bạn chưa đủ điều kiện áp dụng mã FANCUNG."))
        else: return redirect(url_for('dashboard', error="Mã giảm giá này không chính xác."))

    if current_bal < final_amt: return redirect(url_for('dashboard', error="Số dư tài khoản không đủ để giao dịch."))
    
    supabase.table("users").update({"balance": current_bal - final_amt}).eq("username", u).execute()
    supabase.table("cards").insert({'username': u, 'type': f"Nạp {g_info['name'].upper()} ({reward_val})", 'amount': final_amt, 'serial': f"Game: {g_user}{cp_info}", 'code': 'Chờ xử lý', 'status': 'Chờ xử lý'}).execute()
    return redirect(url_for('dashboard', msg="Đã tạo đơn nạp game thành công! Hệ thống đang xử lý gói nạp."))

@app.route('/secret-admin-panel')
def admin_panel():
    if 'username' not in session or session['username'] != ADMIN_USERNAME: return "Từ chối quyền truy cập", 403
    kw = request.args.get('search_user', '').strip()
    res = supabase.table("users").select("username", "balance", "contact").eq("username", kw).execute().data[0] if kw and supabase.table("users").select("username").eq("username", kw).execute().data else None
    all_c = supabase.table("cards").select("*").eq("status", "Chờ duyệt").order("id", desc=True).execute().data or []
    buy_o = supabase.table("cards").select("*").eq("status", "Chờ xử lý").order("id", desc=True).execute().data or []
    all_b = [{'id': b.get('id'), 'username': b.get('username'), 'type': b.get('type'), 'amount': b.get('amount'), 'contact_info': b.get('serial'), 'status': b.get('status')} for b in buy_o]
    return render_template_string(ADMIN_HTML, all_cards=all_c, all_bought_cards=all_b, search_keyword=kw, search_result=res)

@app.route('/admin/complete-buy/<int:order_id>')
def admin_complete_buy(order_id):
    if 'username' in session and session['username'] == ADMIN_USERNAME: 
        supabase.table("cards").update({"status": "Đã gửi thẻ", "code": "Hoàn thành"}).eq("id", order_id).execute()
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
    if 'username' in session and session['username'] == ADMIN_USERNAME: 
        supabase.table("cards").update({"status": "Thẻ lỗi/Sai mã"}).eq("id", card_id).execute()
    return redirect('/secret-admin-panel')

@app.route('/logout')
def logout(): 
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
