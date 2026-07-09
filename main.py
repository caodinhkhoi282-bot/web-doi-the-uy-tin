from flask import Flask, render_template_string, request, redirect, url_for, session
import os
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = "doitheuytin_sieucap"

# =================================================================
# 🔗 THÔNG TIN SUPABASE CỦA BẠN (Đã thay bằng Secret Key đặc quyền)
# =================================================================
SUPABASE_URL = "https://crtdwvzaccycikgxyriu.supabase.co"
SUPABASE_KEY = "sb_secret_ycV2N5g9jsxpP0OsFHduRQ_N_cJEqA9"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_USERNAME = "DINH_KHOI28215"

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
    body { background-color: #f4f6f9; color: #333; font-family: Arial, sans-serif; margin: 0; padding: 0; padding-bottom: 60px; }
    .navbar { background-color: #ffffff; border-bottom: 1px solid #e0e0e0; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .navbar a { color: #d32f2f; text-decoration: none; font-weight: bold; margin-left: 15px; }
    .container { max-width: 700px; margin: 25px auto; padding: 20px; border-radius: 12px; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
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
</style>
"""

LOGIN_HTML = BASE_CSS + """
<div class="container" style="max-width: 500px; margin-top: 40px;">
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
            <div class="form-group"><label>Số điện thoại / Email liên hệ:</label><input type="text" name="contact" placeholder="Nhập SĐT hoặc Email để bảo mật thẻ" required></div>
            <button type="submit" style="background-color: #4caf50;">TẠO TÀI KHOẢN MỚI</button>
        </form>
    </div>
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
        <a href="/buy/{{ key }}" class="card-item" style="background-color: {{ val.color }};">
            <div style="font-size: 20px; margin-bottom: 5px;">💳</div>
            Mua {{ val.name }}
        </a>
        {% endfor %}
    </div>
</div>

<div class="container">
    <h2>3. LỊCH SỬ GỬI THẺ CỦA BẠN</h2>
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

ADMIN_HTML = """
<head><meta name="robots" content="noindex, nofollow"></head>
""" + BASE_CSS + """
<div class="container" style="max-width: 950px;">
    <h2>🔒 TRANG QUẢN TRỊ ADMIN</h2>
    
    <div style="background: #eef2f7; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #ccc;">
        <h3>🔍 TRA CỨU SỐ DƯ TÀI KHOẢN</h3>
        <form method="GET" action="/secret-admin-panel">
            <div style="display: flex; gap: 10px;">
                <input type="text" name="search_user" placeholder="Nhập chính xác tên tài khoản khách hàng..." value="{{ search_keyword }}" required>
                <button type="submit" style="background: #2196F3; width: auto; padding: 0 25px;">Tìm Kiếm</button>
            </div>
        </form>
        
        {% if search_keyword %}
            <div style="margin-top: 15px; background: white; padding: 15px; border-radius: 6px; border: 1px dashed #2196F3;">
                {% if search_result %}
                    <p style="margin: 5px 0;">👤 Tên tài khoản: <b style="color:#2196F3; font-size:16px;">{{ search_result.username }}</b></p>
                    <p style="margin: 5px 0;">💰 Số dư tài khoản: <b style="color:#28a745; font-size:16px;">{{ search_result.balance }}đ</b></p>
                    <p style="margin: 5px 0;">📞 Thông tin liên hệ: <b>{{ search_result.contact }}</b></p>
                {% else %}
                    <p style="color: red; margin: 0; font-weight: bold;">❌ Không tìm thấy người dùng có tên: "{{ search_keyword }}"</p>
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
    
    <h3>🚨 DANH SÁCH THẺ CHỜ DUYỆT</h3>
    <table>
        <tr><th>Tài khoản</th><th>Loại</th><th>Mệnh giá</th><th>Seri</th><th>Mã</th><th>Trạng thái</th><th>Hành động</th></tr>
        {% for c in all_cards %}
        <tr>
            <td>{{ c.username }}</td><td>{{ c.type.upper() }}</td><td>{{ c.amount }}đ</td><td>{{ c.serial }}</td><td>{{ c.code }}</td>
            <td><span class="badge bg-warning">{{ c.status }}</span></td>
            <td>
                <a href="/admin/approve/{{ c.id }}" style="color:green; font-weight:bold;">[ĐÚNG]</a> | 
                <a href="/admin/reject/{{ c.id }}" style="color:red; font-weight:bold;">[LỖI]</a>
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
"""

@app.route('/')
def index():
    if 'username' in session: return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_HTML, msg=request.args.get('msg', ''))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].strip()
    password = request.form['password']
    
    res = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
    if res.data:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
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
    
    card_data = supabase.table("cards").select("*").eq("username", user).execute()
    return render_template_string(DASHBOARD_HTML, username=user, balance=balance, my_cards=card_data.data, card_types=CARD_TYPES, denominations=DENOMINATIONS)

@app.route('/submit-card', methods=['POST'])
def submit_card():
    if 'username' not in session: return redirect(url_for('index'))
    supabase.table("cards").insert({
        'username': session['username'], 'type': request.form['card_type'],
        'amount': int(request.form['amount']), 'serial': request.form['serial'].strip(),
        'code': request.form['code'].strip(), 'status': 'Chờ duyệt'
    }).execute()
    return redirect(url_for('dashboard'))

# --- TRANG QUẢN TRỊ ADMIN ĐÃ TINH CHỈNH THEO YÊU CẦU ---
@app.route('/secret-admin-panel')
def admin_panel():
    if 'username' not in session or session['username'] != ADMIN_USERNAME: return "Từ chối", 403
    
    # Tìm kiếm tài khoản (Chỉ hiển thị tên và tiền, liên hệ)
    search_keyword = request.args.get('search_user', '').strip()
    search_result = None
    if search_keyword:
        user_query = supabase.table("users").select("username", "balance", "contact").eq("username", search_keyword).execute()
        if user_query.data:
            search_result = user_query.data[0]

    all_cards = supabase.table("cards").select("*").eq("status", "Chờ duyệt").execute()
    return render_template_string(ADMIN_HTML, all_cards=all_cards.data, search_keyword=search_keyword, search_result=search_result)

@app.route('/admin/gift', methods=['POST'])
def admin_gift():
    if 'username' not in session or session['username'] != ADMIN_USERNAME: return "Từ chối", 403
    target = request.form['gift_username'].strip()
    amount = int(request.form['gift_amount'])
    
    user_data = supabase.table("users").select("balance").eq("username", target).execute()
    if user_data.data:
        new_balance = user_data.data[0]['balance'] + amount
        supabase.table("users").update({"balance": new_balance}).eq("username", target).execute()
    return "<script>alert('Gift tiền thành công!'); window.location='/secret-admin-panel';</script>"

@app.route('/admin/approve/<int:card_id>')
def admin_approve(card_id):
    if 'username' not in session or session['username'] != ADMIN_USERNAME: return "Từ chối", 403
    card = supabase.table("cards").select("*").eq("id", card_id).execute()
    if card.data and card.data[0]['status'] == 'Chờ duyệt':
        supabase.table("cards").update({"status": "Thành công"}).eq("id", card_id).execute()
        username = card.data[0]['username']
        user_data = supabase.table("users").select("balance").eq("username", username).execute()
        if user_data.data:
            new_balance = user_data.data[0]['balance'] + card.data[0]['amount']
            supabase.table("users").update({"balance": new_balance}).eq("username", username).execute()
    return redirect('/secret-admin-panel')

@app.route('/admin/reject/<int:card_id>')
def admin_reject(card_id):
    if 'username' not in session or session['username'] != ADMIN_USERNAME: return "Từ chối", 403
    supabase.table("cards").update({"status": "Thẻ lỗi/Sai mã"}).eq("id", card_id).execute()
    return redirect('/secret-admin-panel')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
            
