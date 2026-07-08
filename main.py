import os
from flask import Flask, render_template_string, request, redirect, url_for, session
from supabase import create_client, Client

# === CẤU HÌNH SUPABASE ===
SUPABASE_URL = "https://crtdwvzaccycikgxyriu.supabase.co"
SUPABASE_KEY = "Sb_publishable_Mr2bWaJ-2j0Ffs5V1J70kw_OrroVSxv"

app = Flask(__name__)
app.secret_key = "doitheuytin_sieucap"

# Kết nối an toàn đến Supabase
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    supabase = None
    print(f"Lỗi kết nối Supabase: {e}")

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
</style>
"""

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
        <span>Xin chào: <b>{{{{ username }}}}</b> | Số dư: <b style="color:#28a745;">{{{{ balance }}}}đ</b></span>
        <a href="/logout">Đăng xuất</a>
    </div>
</div>
<div class="container">
    <h2>1. GỬI THẺ CÀO (ĐỔI THÀNH TIỀN)</h2>
    <form method="POST" action="/submit-card">
        <div class="form-group">
            <label>Loại thẻ:</label>
            <select name="card_type">
                {{% for key, val in card_types.items() %}}<option value="{{{{ key }}}}">{{{{ val.name }}}}</option>{{% endfor %}}
            </select>
        </div>
        <div class="form-group">
            <label>Mệnh giá thẻ:</label>
            <select name="amount">
                {{% for d in denominations %}}<option value="{{{{ d }}}}">{{{{ d }}}}đ</option>{{% endfor %}}
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
        <a href="/buy/{{{{ key }}}}" class="card-item" style="background-color: {{{{ val.color }}}};">
            <div style="font-size: 18px; margin-bottom: 5px;">💳</div>{{{ val.name }}}
        </a>
        {{% endfor %}}
    </div>
</div>
<div class="container">
    <h2>3. LỊCH SỬ GỬI THẺ</h2>
    <table>
        <tr><th>Loại thẻ</th><th>Mệnh giá</th><th>Trạng thái</th></tr>
        {{% for c in my_cards %}}
        <tr>
            <td>{{{{ c.type.upper() }}}}</td><td>{{{{ c.amount }}}}đ</td>
            <td><span class="badge {{% if c.status=='Chờ duyệt' %}}bg-warning{{% elif c.status=='Thành công' %}}bg-success{{% else %}}bg-danger{{% endif %}}">{{{{ c.status }}}}</span></td>
        </tr>
        {{% endfor %}}
    </table>
</div>
"""

@app.route('/')
def index():
    if 'username' in session: return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    if not supabase:
        return "<h3>Lỗi: Không thể kết nối Supabase.</h3>"
    username = request.form['username']
    password = request.form['password']
    contact = request.form.get('contact', 'Không có')
    
    try:
        res = supabase.table("users").select("*").eq("username", username).execute()
        if not res.data:
            supabase.table("users").insert({"username": username, "password": password, "contact": contact, "balance": 0}).execute()
            balance = 0
        else:
            balance = res.data[0]['balance']
        session['username'] = username
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"<h3>Lỗi kết nối bảng Users: {str(e)}</h3>"

@app.route('/dashboard')
def dashboard():
    if 'username' not in session: return redirect(url_for('index'))
    user = session['username']
    try:
        res_user = supabase.table("users").select("balance").eq("username", user).execute()
        balance = res_user.data[0]['balance'] if res_user.data else 0
        res_cards = supabase.table("cards").select("*").eq("username", user).execute()
        return render_template_string(DASHBOARD_HTML, username=user, balance=balance, my_cards=res_cards.data, card_types=CARD_TYPES, denominations=DENOMINATIONS)
    except Exception as e:
        return f"<h3>Lỗi tải dữ liệu: {str(e)}</h3>"

@app.route('/submit-card', methods=['POST'])
def submit_card():
    if 'username' not in session: return redirect(url_for('index'))
    try:
        supabase.table("cards").insert({
            'username': session['username'], 'type': request.form['card_type'], 
            'amount': int(request.form['amount']), 'serial': request.form['serial'], 
            'code': request.form['code'], 'status': 'Chờ duyệt'
        }).execute()
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"<h3>Lỗi gửi thẻ: {str(e)}</h3>"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
