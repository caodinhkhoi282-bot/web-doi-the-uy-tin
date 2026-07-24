from flask import Flask, render_template_string, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# ------------------------------------------------------------------
# TRANG CHÍNH (GIAO DIỆN WEB)
# ------------------------------------------------------------------
HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Khôi Bypass Key</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: #0a0a12;
            color: #fff;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: #14141f;
            border-radius: 28px;
            padding: 32px 28px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 12px 48px rgba(0,0,0,0.6);
            border: 1px solid #2a2a3e;
        }
        .logo {
            text-align: center;
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #00d4ff, #7b2ffc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }
        .sub {
            text-align: center;
            color: #8888aa;
            font-size: 14px;
            margin-bottom: 28px;
            border-bottom: 1px solid #222;
            padding-bottom: 14px;
        }
        .input-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }
        .input-group label {
            font-weight: 600;
            font-size: 15px;
            color: #ccc;
        }
        .input-group input {
            background: #0d0d18;
            border: 1px solid #2a2a44;
            border-radius: 14px;
            padding: 16px 18px;
            color: #fff;
            font-size: 16px;
            outline: none;
            width: 100%;
        }
        .input-group input:focus {
            border-color: #00d4ff;
            box-shadow: 0 0 0 3px rgba(0,212,255,0.15);
        }
        .btn {
            background: #00d4ff;
            border: none;
            color: #0a0a12;
            font-weight: 700;
            font-size: 18px;
            padding: 16px;
            border-radius: 14px;
            cursor: pointer;
            width: 100%;
            transition: 0.2s;
        }
        .btn:active { transform: scale(0.97); }
        .btn:disabled { opacity: 0.5; pointer-events: none; }
        .status-box {
            background: #0d0d18;
            border-radius: 14px;
            padding: 18px 20px;
            margin-top: 20px;
            min-height: 70px;
            border: 1px solid #1e1e32;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            text-align: center;
        }
        .status-box .loading {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #aaa;
            font-size: 15px;
        }
        .status-box .loading .spinner {
            width: 24px;
            height: 24px;
            border: 3px solid #1e1e32;
            border-top: 3px solid #00d4ff;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .status-box .result { display: none; width: 100%; }
        .status-box .result .key-display {
            background: #0a0a12;
            padding: 12px 16px;
            border-radius: 10px;
            font-family: monospace;
            font-size: 18px;
            word-break: break-all;
            color: #00d4ff;
            border: 1px solid #2a2a44;
            margin-bottom: 12px;
        }
        .status-box .result .actions {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .status-box .result .actions button {
            background: #2a2a44;
            border: none;
            color: #fff;
            padding: 10px 24px;
            border-radius: 30px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            flex: 1;
            min-width: 100px;
        }
        .status-box .result .actions button.copy {
            background: #00c853;
            color: #000;
        }
        .status-box .result .actions button.back {
            background: #b71c1c;
        }
        .status-box .error { color: #ff5252; font-size: 15px; }
        .hidden { display: none !important; }
        .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            color: #444;
            border-top: 1px solid #1a1a2a;
            padding-top: 16px;
        }
    </style>
</head>
<body>
    <div class="container" id="app">
        <div class="logo">⚡ Khôi Bypass</div>
        <div class="sub">Hỗ trợ Linkvertise, Link1s, Linkm4, v.v.</div>

        <div id="stepUrl">
            <div class="input-group">
                <label>🔗 URL cần bypass</label>
                <input type="text" id="urlInput" placeholder="https://linkvertise.com/...">
            </div>
            <button class="btn" id="submitBtn">Xác nhận</button>
        </div>

        <div class="status-box" id="statusBox">
            <div id="defaultStatus" style="color:#666; font-size:14px;">Nhập URL và bấm Xác nhận</div>
            <div id="loadingStatus" class="loading hidden">
                <div class="spinner"></div>
                <span>Đang lấy key ...</span>
            </div>
            <div id="resultStatus" class="result">
                <div class="key-display" id="keyDisplay">KEY_HERE</div>
                <div class="actions">
                    <button class="copy" id="copyBtn">📋 Copy</button>
                    <button class="back" id="backBtn">↩ Bỏ qua</button>
                </div>
            </div>
            <div id="errorStatus" class="error hidden">Đã xảy ra lỗi, vui lòng thử lại.</div>
        </div>

        <div class="footer">🔹 Delta • Arceus • Hydrogen • các executor khác</div>
    </div>

    <script>
        const urlInput = document.getElementById('urlInput');
        const submitBtn = document.getElementById('submitBtn');
        const defaultStatus = document.getElementById('defaultStatus');
        const loadingStatus = document.getElementById('loadingStatus');
        const resultStatus = document.getElementById('resultStatus');
        const errorStatus = document.getElementById('errorStatus');
        const keyDisplay = document.getElementById('keyDisplay');
        const copyBtn = document.getElementById('copyBtn');
        const backBtn = document.getElementById('backBtn');

        submitBtn.addEventListener('click', async function() {
            const url = urlInput.value.trim();
            if (!url) { alert('Vui lòng nhập URL.'); return; }

            defaultStatus.classList.add('hidden');
            loadingStatus.classList.remove('hidden');
            resultStatus.style.display = 'none';
            errorStatus.classList.add('hidden');
            submitBtn.disabled = true;

            try {
                const response = await fetch('/bypass', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });
                const data = await response.json();
                if (data.success) {
                    keyDisplay.textContent = data.result;
                    loadingStatus.classList.add('hidden');
                    resultStatus.style.display = 'block';
                } else {
                    throw new Error(data.error || 'Không thể bypass');
                }
            } catch (err) {
                loadingStatus.classList.add('hidden');
                errorStatus.textContent = '❌ ' + err.message;
                errorStatus.classList.remove('hidden');
                setTimeout(() => resetToDefault(), 3000);
            } finally {
                submitBtn.disabled = false;
            }
        });

        copyBtn.addEventListener('click', function() {
            const key = keyDisplay.textContent;
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(key).then(() => {
                    copyBtn.textContent = '✅ Copied!';
                    setTimeout(() => { copyBtn.textContent = '📋 Copy'; }, 1500);
                }).catch(() => fallbackCopy(key));
            } else {
                fallbackCopy(key);
            }
        });

        function fallbackCopy(text) {
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.left = '-9999px';
            document.body.appendChild(ta);
            ta.select();
            try { document.execCommand('copy'); copyBtn.textContent = '✅ Copied!'; setTimeout(() => { copyBtn.textContent = '📋 Copy'; }, 1500); } catch(e) { alert('Không thể copy'); }
            document.body.removeChild(ta);
        }

        backBtn.addEventListener('click', resetToDefault);

        function resetToDefault() {
            defaultStatus.classList.remove('hidden');
            loadingStatus.classList.add('hidden');
            resultStatus.style.display = 'none';
            errorStatus.classList.add('hidden');
            urlInput.value = '';
            urlInput.focus();
            submitBtn.disabled = false;
        }

        urlInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') submitBtn.click();
        });
    </script>
</body>
</html>
"""

# ------------------------------------------------------------------
# API BYPASS (GỌI DỊCH VỤ BÊN NGOÀI)
# ------------------------------------------------------------------
def bypass_link(url):
    """
    Gọi API bypass.vip (miễn phí, hỗ trợ Linkvertise, Link1s, Linkm4)
    Trả về key hoặc link đã bypass.
    """
    api_endpoint = "https://api.bypass.vip/"
    payload = {"url": url}
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(api_endpoint, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "success" and data.get("result"):
            return data["result"]
        else:
            # Một số API trả về khác cấu trúc, thử check
            if data.get("success") and data.get("bypassed"):
                return data["bypassed"]
            raise Exception("Phản hồi API không hợp lệ: " + json.dumps(data))
    except Exception as e:
        raise Exception(f"Lỗi gọi API: {str(e)}")

# ------------------------------------------------------------------
# ROUTE XỬ LÝ BYPASS
# ------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML)

@app.route('/bypass', methods=['POST'])
def handle_bypass():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"success": False, "error": "Thiếu URL"}), 400
    url = data['url'].strip()
    if not url:
        return jsonify({"success": False, "error": "URL rỗng"}), 400
    try:
        result = bypass_link(url)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ------------------------------------------------------------------
# CHẠY APP
# ------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
