from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Khôi Execute</title>
    <style>
        /* Reset & base */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Roboto, Arial, sans-serif;
            background: #0d0d0d;
            color: #fff;
            height: 100vh;
            overflow: hidden;
            user-select: none;
        }
        /* Thanh công cụ trên cùng */
        .toolbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 48px;
            background: #1a1a2e;
            display: flex;
            align-items: center;
            padding: 0 12px;
            z-index: 999;
            border-bottom: 1px solid #2a2a4a;
        }
        .toolbar .brand {
            font-size: 18px;
            font-weight: bold;
            color: #00d4ff;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .toolbar .brand img {
            width: 28px;
            height: 28px;
        }
        .toolbar .spacer { flex: 1; }
        .toolbar .start-btn {
            background: #00c853;
            border: none;
            color: #fff;
            padding: 4px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
            transition: 0.2s;
            box-shadow: 0 2px 8px rgba(0,200,80,0.3);
        }
        .toolbar .start-btn.stop {
            background: #d50000;
            box-shadow: 0 2px 8px rgba(213,0,0,0.3);
        }

        /* Overlay cửa sổ web thu nhỏ */
        #web-overlay {
            position: fixed;
            top: 60px;
            left: 20px;
            width: 320px;
            height: 450px;
            background: #1a1a2e;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.8);
            border: 1px solid #2a2a4a;
            display: none;
            flex-direction: column;
            z-index: 1000;
            resize: both;
            overflow: hidden;
            min-width: 260px;
            min-height: 300px;
        }
        #web-overlay .title-bar {
            background: #2a2a4a;
            padding: 6px 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: grab;
            border-radius: 16px 16px 0 0;
            flex-shrink: 0;
        }
        #web-overlay .title-bar .title {
            font-size: 14px;
            color: #aaa;
        }
        #web-overlay .title-bar .close-btn {
            background: none;
            border: none;
            color: #fff;
            font-size: 18px;
            cursor: pointer;
            padding: 0 4px;
        }
        #web-overlay iframe {
            flex: 1;
            width: 100%;
            border: none;
            background: #0d0d0d;
        }

        /* Trang chính (nội dung web) */
        .main-content {
            margin-top: 48px;
            padding: 16px;
            height: calc(100vh - 48px);
            overflow-y: auto;
        }
        .main-content h2 {
            color: #00d4ff;
            margin-bottom: 16px;
            font-weight: 300;
        }
        .script-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .script-item {
            background: #1a1a2e;
            padding: 12px 16px;
            border-radius: 12px;
            border-left: 4px solid #00d4ff;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .script-item .name {
            font-weight: 500;
            font-size: 15px;
        }
        .script-item .actions button {
            background: #2a2a4a;
            border: none;
            color: #fff;
            padding: 4px 12px;
            border-radius: 6px;
            margin-left: 8px;
            cursor: pointer;
            font-size: 12px;
        }
        .script-item .actions button.run {
            background: #00c853;
        }
        .script-item .actions button.delete {
            background: #b71c1c;
        }
        .add-script {
            margin-top: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .add-script input, .add-script textarea {
            background: #1a1a2e;
            border: 1px solid #2a2a4a;
            border-radius: 8px;
            padding: 10px;
            color: #fff;
            font-size: 14px;
            width: 100%;
        }
        .add-script textarea {
            height: 120px;
            resize: vertical;
            font-family: monospace;
        }
        .add-script button {
            background: #00d4ff;
            border: none;
            color: #0d0d0d;
            font-weight: bold;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        .toast {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #1a1a2e;
            padding: 10px 24px;
            border-radius: 30px;
            color: #fff;
            border: 1px solid #2a2a4a;
            display: none;
            z-index: 9999;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }

        @media (max-width: 600px) {
            #web-overlay {
                width: 90%;
                height: 70%;
                left: 5%;
                top: 15%;
            }
        }
    </style>
</head>
<body>

    <!-- Thanh công cụ -->
    <div class="toolbar">
        <div class="brand">
            <span style="font-size:24px;">⚡</span> Khôi Execute
        </div>
        <div class="spacer"></div>
        <button id="startStopBtn" class="start-btn">▶ START</button>
    </div>

    <!-- Overlay cửa sổ web thu nhỏ -->
    <div id="web-overlay">
        <div class="title-bar" id="dragHandle">
            <span class="title">⏺ Khôi Execute</span>
            <button class="close-btn" id="closeOverlayBtn">✕</button>
        </div>
        <iframe id="webIframe" src="/"></iframe>
    </div>

    <!-- Nội dung chính (trang web) -->
    <div class="main-content" id="mainContent">
        <h2>📦 Script Manager</h2>
        <div class="script-list" id="scriptList"></div>

        <div class="add-script">
            <input type="text" id="scriptName" placeholder="Tên script...">
            <textarea id="scriptCode" placeholder="-- Nhập code Lua tại đây"></textarea>
            <button id="saveScriptBtn">➕ Lưu script</button>
        </div>
    </div>

    <!-- Toast thông báo -->
    <div class="toast" id="toast"></div>

    <script>
        // ========== QUẢN LÝ SCRIPT ==========
        let scripts = JSON.parse(localStorage.getItem('scripts')) || [];

        function renderScripts() {
            const container = document.getElementById('scriptList');
            container.innerHTML = '';
            if (scripts.length === 0) {
                container.innerHTML = '<div style="color:#666; text-align:center; padding:20px;">Chưa có script nào.</div>';
                return;
            }
            scripts.forEach((s, i) => {
                const div = document.createElement('div');
                div.className = 'script-item';
                div.innerHTML = `
                    <span class="name">${s.name || 'Không tên'}</span>
                    <div class="actions">
                        <button class="run" data-index="${i}">▶ Chạy</button>
                        <button class="delete" data-index="${i}">🗑</button>
                    </div>
                `;
                container.appendChild(div);
            });
            // Gán sự kiện cho các nút
            document.querySelectorAll('.run').forEach(btn => {
                btn.addEventListener('click', function() {
                    const idx = parseInt(this.dataset.index);
                    const script = scripts[idx];
                    if (script) {
                        // Mô phỏng chạy script (thực tế có thể gửi lên server hoặc hiển thị)
                        showToast('⏳ Đang chạy script: ' + script.name);
                        // Ở đây bạn có thể mở overlay và chèn script vào iframe
                        // Tạm thời chỉ thông báo
                    }
                });
            });
            document.querySelectorAll('.delete').forEach(btn => {
                btn.addEventListener('click', function() {
                    const idx = parseInt(this.dataset.index);
                    if (confirm('Xóa script này?')) {
                        scripts.splice(idx, 1);
                        localStorage.setItem('scripts', JSON.stringify(scripts));
                        renderScripts();
                        showToast('✅ Đã xóa');
                    }
                });
            });
        }

        // Lưu script mới
        document.getElementById('saveScriptBtn').addEventListener('click', function() {
            const name = document.getElementById('scriptName').value.trim();
            const code = document.getElementById('scriptCode').value.trim();
            if (!name || !code) {
                showToast('⚠️ Vui lòng nhập tên và code.');
                return;
            }
            scripts.push({ name, code });
            localStorage.setItem('scripts', JSON.stringify(scripts));
            document.getElementById('scriptName').value = '';
            document.getElementById('scriptCode').value = '';
            renderScripts();
            showToast('✅ Đã lưu script: ' + name);
        });

        // Toast
        function showToast(msg) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.style.display = 'block';
            clearTimeout(t._timer);
            t._timer = setTimeout(() => { t.style.display = 'none'; }, 2500);
        }

        // ========== START / STOP OVERLAY ==========
        let overlayVisible = false;
        const overlay = document.getElementById('web-overlay');
        const startBtn = document.getElementById('startStopBtn');
        const iframe = document.getElementById('webIframe');

        // Mở overlay (với iframe đã load)
        function showOverlay() {
            overlay.style.display = 'flex';
            overlayVisible = true;
            startBtn.textContent = '■ STOP';
            startBtn.classList.add('stop');
            // Đảm bảo iframe load nội dung (nếu chưa)
            iframe.src = iframe.src || '/';
        }

        function hideOverlay() {
            overlay.style.display = 'none';
            overlayVisible = false;
            startBtn.textContent = '▶ START';
            startBtn.classList.remove('stop');
        }

        startBtn.addEventListener('click', function() {
            if (overlayVisible) {
                hideOverlay();
            } else {
                showOverlay();
            }
        });

        // Nút đóng trên title bar
        document.getElementById('closeOverlayBtn').addEventListener('click', hideOverlay);

        // Kéo thả overlay
        const dragHandle = document.getElementById('dragHandle');
        let isDragging = false;
        let startX, startY, origX, origY;

        dragHandle.addEventListener('mousedown', function(e) {
            isDragging = true;
            const rect = overlay.getBoundingClientRect();
            startX = e.clientX;
            startY = e.clientY;
            origX = rect.left;
            origY = rect.top;
            document.addEventListener('mousemove', onDrag);
            document.addEventListener('mouseup', stopDrag);
        });

        function onDrag(e) {
            if (!isDragging) return;
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            overlay.style.left = (origX + dx) + 'px';
            overlay.style.top = (origY + dy) + 'px';
            overlay.style.right = 'auto';
            overlay.style.bottom = 'auto';
        }
        function stopDrag() {
            isDragging = false;
            document.removeEventListener('mousemove', onDrag);
            document.removeEventListener('mouseup', stopDrag);
        }

        // Hỗ trợ touch
        dragHandle.addEventListener('touchstart', function(e) {
            const touch = e.touches[0];
            isDragging = true;
            const rect = overlay.getBoundingClientRect();
            startX = touch.clientX;
            startY = touch.clientY;
            origX = rect.left;
            origY = rect.top;
            document.addEventListener('touchmove', onTouchDrag);
            document.addEventListener('touchend', stopTouchDrag);
        }, { passive: true });

        function onTouchDrag(e) {
            if (!isDragging) return;
            const touch = e.touches[0];
            const dx = touch.clientX - startX;
            const dy = touch.clientY - startY;
            overlay.style.left = (origX + dx) + 'px';
            overlay.style.top = (origY + dy) + 'px';
            overlay.style.right = 'auto';
            overlay.style.bottom = 'auto';
        }
        function stopTouchDrag() {
            isDragging = false;
            document.removeEventListener('touchmove', onTouchDrag);
            document.removeEventListener('touchend', stopTouchDrag);
        }

        // ========== KHỞI TẠO ==========
        renderScripts();

        // Nếu đã có overlay từ trước (ví dụ reload) thì ẩn đi
        hideOverlay();

        console.log('Khôi Execute đã sẵn sàng!');
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
