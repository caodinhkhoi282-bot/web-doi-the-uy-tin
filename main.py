from flask import Flask, render_template_string, request, redirect, url_for, session
from supabase import create_client, Client

# === CẤU HÌNH SUPABASE (ĐÃ ĐIỀN SẴN THÔNG TIN THẬT CỦA BẠN) ===
SUPABASE_URL = "https://crtdwvzaccycikgxyriu.supabase.co"
SUPABASE_KEY = "Sb_publishable_Mr2bWaJ-2j0Ffs5V1J70kw_OrroVSxv"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.secret_key = "doitheuytin_sieucap"

# DANH SÁCH ĐẦY ĐỦ CÁC LOẠI THẺ CÓ HÌNH ẢNH
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
    body { background-color: #f4f6f9; color: #333; font-family: Arial, sans-serif; margin: 0; padding: 0; padding-bottom: 80px; }
    .navbar { background-color: #ffffff; border-bottom: 1px solid #e0e0e0; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .navbar a { color: #d32f2f; text-decoration: none; font-weight: bold; margin-left: 15px; }
    .logo-container { display: flex; align-items: center; text-decoration: none; gap: 10px; }
    .logo-img { width: 45px; height: 45px; border-radius: 50%; object-fit: cover; }
    .logo-text { font-size: 20px; color: #d4af37; font-weight: bold; }
    .container { max-width: 700px; margin: 25px auto; padding: 20px; border-radius: 12px; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    h2 { color: #222; border-left: 5px solid #2196F3; padding-left: 10px; font-size: 18px; margin-bottom: 20px; }
    .form-group { margin-bottom: 15px; }
    label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px; }
    input, select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 14px; }
    button { background-color: #2196F3; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
    button:hover { background-color: #1e88e5; }
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
    
    /* NÚT DISCORD TO HƠN + NẰM Ở GÓC GIỮA MÀN HÌNH BÊN PHẢI */
    .discord-support-btn { 
        position: fixed; 
        top: 50%; 
        right: 15px; 
        transform: translateY(-50%); 
        width: 70px; 
        height: 70px; 
        background-color: #111111; 
        border-radius: 50%; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.4); 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        cursor: pointer; 
        z-index: 9999; 
        border: 2.5px solid #23a55a; 
    }
    .discord-support-btn::after { 
        content: '➔'; 
        color: #23a55a; 
        font-size: 11px; 
        position: absolute; 
        bottom: 4px; 
        right: 4px; 
        background: #111; 
        border-radius: 50%; 
        width: 20px; 
        height: 20px; 
        display: flex; 
        justify-content: center; 
        align-items: center; 
    }
    .discord-icon { width: 38px; height: 38px; }
    .support-text-badge { 
        position: absolute; 
        top: -12px; 
        background: #23a55a; 
        color: white; 
        font-size: 11px; 
        padding: 3px 8px; 
        border-radius: 12px; 
        font-weight: bold; 
        white-space: nowrap; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* BONG BÓNG HỘP THOẠI HỖ TRỢ HIỂN THỊ CẠNH NÚT GIỮA MÀN HÌNH */
    .support-box { 
        display: none; 
        position: fixed; 
        top: 50%;
        right: 95px; 
        transform: translateY(-50%);
        width: 280px; 
        background: white; 
        border-radius: 12px; 
        box-shadow: 0 5px 25px rgba(0,0,0,0.3); 
        border: 1px solid #e0e0e0; 
        z-index: 9999; 
        overflow: hidden; 
    }
    .support-header { background: #5865F2; color: white; padding: 12px; font-weight: bold; font-size: 14px; display: flex; justify-content: space-between; align-items: center; }
    .support-body { padding: 15px; text-align: center; }
    .support-body p { margin: 0 0 10px 0; font-size: 13px; color: #444; }
    .discord-banner { width: 100%; border-radius: 6px; margin-bottom: 12px; }
    .btn-join-discord { display: block; background: #5865F2; color: white; text-decoration: none; padding: 10px; border-radius: 6px; font-weight: bold; font-size: 13px; text-align: center; }
</style>

<div class="discord-support-btn" onclick="toggleSupportBox()">
    <span class="support-text-badge">Hỗ trợ</span>
    <svg class="discord-icon" viewBox="0 0 127.14 96.36" fill="#5865F2"><path d="M107.7,8.07A105.15,105.15,0,0,0,77.26,0a77.19,77.19,0,0,0-3.3,6.83A96.67,96.67,0,0,0,53.22,6.83,77.19,77.19,0,0,0,49.88,0,105.15,105.15,0,0,0,19.44,8.07C3.66,31.58-1.86,54.65,1,77.53A105.73,105.73,0,0,0,32,96.36a74.37,74.37,0,0,0,6.71-11,68.6,68.6,0,0,1-10.57-5.1c.9-.65,1.76-1.34,2.58-2A75.4,75.4,0,0,0,96.44,78.3c.82.71,1.68,1.4,2.58,2a68.6,68.6,0,0,1-10.57,5.1,74.37,74.37,0,0,0,6.71,11,105.73,105.73,0,0,0,31-18.83C130.65,50.22,124.74,27.42,107.7,8.07ZM42.45,65.69C36.18,65.69,31,60,31,53S36.18,40.36,42.45,40.36,53.92,46,53.7,53,48.72,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.24,60,73.24,53S78.41,40.36,84.69,40.36,96.16,46,95.94,53,91,65.69,84.69,65.69Z"/></svg>
</div>

<div class="support-box" id="supportBox">
    <div class="support-header">
        <span>🎧 Kênh Hỗ Trợ 24/7</span>
        <span style="cursor:pointer; font-size:18px;" onclick="toggleSupportBox()">×</span>
    </div>
    <div class="support-body">
        <p>Bạn gặp sự cố nạp/mua thẻ? Hãy tham gia máy chủ Discord để được hỗ trợ ngay!</p>
        <img class="discord-banner" src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png" alt="Discord Support">
        <a href="https://discord.gg/x4PqVMxhH" target="_blank" class="btn-join-discord">THAM GIA DISCORD</a>
    </div>
</div>

<script>
function toggleSupportBox() {
    var box = document.getElementById('supportBox');
    box.style.display = (box.style.display === 'block') ? 'none' : 'block';
}
</script>
"""

# LOGO CHỮ D VÀNG SANG TRỌNG
LOGO_HTML_CODE = """
<div class="logo-container">
    <img class="logo-img" src="https://img.freepik.com/premium-vector/d-letter-logo-luxury-gold-color_755034-846.jpg" alt="Logo">
    <span class="logo-text">doithecaouytinok.com</span>
</div>
"""

LOGIN_HTML = BASE_CSS + f"""
<div class="container" style="max-width: 450px; margin-top: 80px;">
    <div style="display:flex; justify-content:center; margin-bottom:20px;">{LOGO_HTML_CODE}</div>
    <h2>ĐĂNG NHẬP / ĐĂNG KÝ TỰ ĐỘNG</h2>
    <form method="POST" action="/login">
        <div class="form-group"><label>Tên đăng nhập:</label><input type="text" name="username" required></div>
        <div class="form-group"><label>Mật khẩu:</label><input type="password" name="password" required></div>
        <div class="form-group"><label>Số điện thoại / Email:</label><input type="text" name="contact" placeholder="Nhập SĐT hoặc Email"></div>
        <button type="submit">VÀO TRANG ĐỔI THẺ</button>
    </form>
</div>
"""

DASHBOARD_HTML = BASE_CSS + f"""
<div class="navbar">
    <a href="/dashboard" style="text-decoration: none;">{LOGO_HTML_CODE}</a>
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
            <select name="card_type">
                {{% for key, val in card_types.items() %}}<option value="{{ key }}">{{ val.name }}</option>{{% endfor %}}
            </select>
        </div>
        <div class="form-group">
            <label>Mệnh giá thẻ:</label>
            <select name="amount">
                {{% for d in denominations %}}<option value="{{ d }}">{{ d }}đ</option>{{% endfor %}}
            </select>
        </div>
        <div class="form-group"><label>Số Seri:</label><input type="text" name="serial" required></div>
        <div class="form-group"><label>Mã số sau lớp bạc:</label><input type="text" name="code" required></div>
        <button type="submit" style="background-color: #28a745;">GỬI THẺ DUYỆT</button>
    </form>
</div>
<div class="container">
    <h2>2. CHỌN LOẠI THẺ CẦN MUA</h2>
    <div class="card-grid">
        {{% for key, val in card_types.items() %}}
        <a href="/buy/{{ key }}" class="card-item" style="background-color: {{ val.color }};">
            <div style="font-size: 18px; margin-bottom: 5px;">💳</div>{{ val.name }}
        </a>
        {{% endfor %}}
    </div>
</div>
<div class="container">
    <h2>3. LỊCH SỬ GỬI THẺ & MUA THẺ</h2>
    <h3>Thẻ đã gửi đổi tiền:</h3>
    <table>
        <tr><th>Loại thẻ</th><th>Mệnh giá</th><th>Trạng thái</th></tr>
        {{% for c in my_cards %}}
        <tr>
            <td>{{ c.type.upper() }}</td><td>{{ c.amount }}đ</td>
            <td><span class="badge {{% if c.status=='Chờ duyệt' %}}bg-warning{{% elif c.status=='Thành công' %}}bg-success{{% else %}}bg-danger{{% endif %}}">{{ c.status }}</span></td>
        </tr>
        {{% endfor %}}
    </table>
</div>
"""

BUY_DETAIL_HTML = BASE_CSS + f"""
<div class="navbar"><a href="/dashboard" style="text-decoration: none;">{LOGO_HTML_CODE}</a></div>
<div class="container">
    <h2>MUA THẺ: {{ card_info.name.upper() }}</h2>
    <form method="POST" action="/process-buy">
        <input type="hidden" name="card_type" value="{{ card_type }}">
        <div class="form-group">
            <label>Chọn mệnh giá cần mua:</label>
            <select name="amount">
                {{% for d in denominations %}}<option value="{{ d }}">{{ d }}đ</option>{{% endfor %}}
            </select>
        </div>
        <button type="submit">XÁC NHẬN THANH TOÁN MUA THẺ</button>
    </form>
</div>
"""

ADMIN_HTML = BASE_CSS + """
<div class="container" style="max-width: 950px;">
    <h2>TRANG QUẢN TRỊ BẢO MẬT (ADMIN)</h2>
    <h3>🚨 1. KHÁCH ĐỔI THẺ (CẦN BẠN DUYỆT ĐỂ CỘNG TIỀN KHÁCH)</h3>
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
</div>
"""

@app.route('/')
def index():
    if 'username' in session: return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    contact = request.form.get('contact', 'Không có')
    
    res = supabase.table("users").select("*").eq("username", username).execute()
    if not res.data:
        supabase.table("users").insert({"username": username, "password": password, "contact": contact, "balance": 0}).execute()
        balance = 0
    else:
        balance = res.data[0]['balance']
        
    session['username'] = username
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session: return redirect(url_for('index'))
    user = session['username']
    
    res_user = supabase.table("users").select("balance").eq("username", user).execute()
    balance = res_user.data[0]['balance'] if res_user.data else 0
    
    res_cards = supabase.table("cards").select("*").eq("username", user).execute()
    return render_template_string(DASHBOARD_HTML, username=user, balance=balance, my_cards=res_cards.data, card_types=CARD_TYPES, denominations=DENOMINATIONS)

@app.route('/submit-card', methods=['POST'])
def submit_card():
    if 'username' not in session: return redirect(url_for('index'))
    supabase.table("cards").insert({
        'username': session['username'],
        'type': request.form['card_type'], 'amount': int(request.form['amount']),
        'serial': request.form['serial'], 'code': request.form['code'], 'status': 'Chờ duyệt'
    }).execute()
    return redirect(url_for('dashboard'))

@app.route('/buy/<card_type>')
def buy_detail(card_type):
    if card_type not in CARD_TYPES: return redirect(url_for('dashboard'))
    return render_template_string(BUY_DETAIL_HTML, card_type=card_type, card_info=CARD_TYPES[card_type], denominations=DENOMINATIONS)

@app.route('/process-buy', methods=['POST'])
def process_buy():
    if 'username' not in session: return redirect(url_for('index'))
    user = session['username']
    amount = int(request.form['amount'])
    
    res_user = supabase.table("users").select("*").eq("username", user).execute()
    if res_user.data and res_user.data[0]['balance'] >= amount:
        new_balance = res_user.data[0]['balance'] - amount
        supabase.table("users").update({"balance": new_balance}).eq("username", user).execute()
        return "<script>alert('Mua thẻ thành công!'); window.location='/dashboard';</script>"
    return "<script>alert('Tài khoản không đủ số dư!'); window.location='/dashboard';</script>"

@app.route('/secret-admin-panel')
def admin_panel():
    res = supabase.table("cards").select("*").execute()
    return render_template_string(ADMIN_HTML, all_cards=res.data)

@app.route('/admin/approve/<card_id>')
def admin_approve(card_id):
    res_card = supabase.table("cards").select("*").eq("id", card_id).execute()
    if res_card.data and res_card.data[0]['status'] == 'Chờ duyệt':
        card = res_card.data[0]
        res_user = supabase.table("users").select("balance").eq("username", card['username']).execute()
        if res_user.data:
            new_balance = res_user.data[0]['balance'] + card['amount']
            supabase.table("users").update({"balance": new_balance}).eq("username", card['username']).execute()
        supabase.table("cards").update({"status": "Thành công"}).eq("id", card_id).execute()
    return redirect(url_for('admin_panel'))

@app.route('/admin/reject/<card_id>')
def admin_reject(card_id):
    supabase.table("cards").update({"status": "Thẻ lỗi/Sai mã"}).eq("id", card_id).execute()
    return redirect(url_for('admin_panel'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
    
