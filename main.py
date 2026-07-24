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
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
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
            height: 52px;
            background: #151525;
            display: flex;
            align-items: center;
            padding: 0 16px;
            z-index: 999;
            border-bottom: 1px solid #2a2a4a;
        }
        .toolbar .brand {
            font-size: 20px;
            font-weight: 700;
            background: linear-gradient(135deg, #00d4ff, #7b2ffc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
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
            padding: 6px 20px;
            border-radius: 30px;
            font-weight: 700;
            font-size: 15px;
            cursor: pointer;
            transition: 0.25s;
            box-shadow: 0 2px 12px rgba(0,200,80,0.3);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .toolbar .start-btn.stop {
            background: #d50000;
            box-shadow: 0 2px 12px rgba(213,0,0,0.3);
        }
        .toolbar .start-btn:active { transform: scale(0.96); }

        /* Cửa sổ nổi (overlay) – giống Delta */
        #overlay {
            position: fixed;
            top: 60px;
            left: 20px;
            width: 340px;
            height: 500px;
            background: #151525;
            border-radius: 20px;
            box-shadow: 0 12px 48px rgba(0,0,0,0.8);
            border: 1px solid #2a2a4a;
            display: none;
            flex-direction: column;
            z-index: 1000;
            overflow: hidden;
            resize: both;
            min-width: 280px;
            min-height: 350px;
        }
        #overlay .title-bar {
            background: #1a1a30;
            padding: 8px 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: grab;
            flex-shrink: 0;
            border-bottom: 1px solid #2a2a4a;
        }
        #overlay .title-bar .title {
            font-size: 15px;
            color: #aaa;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        #overlay .title-bar .title span { color: #00d4ff; }
        #overlay .title-bar .close-btn {
            background: none;
            border: none;
            color: #fff;
            font-size: 20px;
            cursor: pointer;
            padding: 0 6px;
            opacity: 0.6;
        }
        #overlay .title-bar .close-btn:hover { opacity: 1; }

        #overlay .content {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            background: #0d0d0d;
        }

        /* Nội dung chính (trang web) */
        .main-content {
            margin-top: 52px;
            padding: 16px 20px 30px;
            height: calc(100vh - 52px);
            overflow-y: auto;
            background: #0d0d0d;
        }
        .main-content h2 {
            color: #00d4ff;
            font-size: 22px;
            font-weight: 300;
            margin-bottom: 18px;
            border-bottom: 1px solid #222;
            padding-bottom: 8px;
        }

        .script-item {
            background: #18182a;
            padding: 14px 16px;
            border-radius: 14px;
            border-left: 4px solid #00d4ff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            transition: 0.2s;
        }
        .script-item .name {
            font-weight: 600;
            font-size: 16px;
            word-break: break-word;
            flex: 1;
        }
        .script-item .actions {
            display: flex;
            gap: 8px;
            flex-shrink: 0;
        }
        .script-item .actions button {
            background: #2a2a4a;
            border: none;
            color: #fff;
            padding: 4px 14px;
            border-radius: 8px;
            font-size: 13px;
            cursor: pointer;
            transition: 0.2s;
        }
        .script-item .actions button.run {
            background: #00c853;
            color: #000;
            font-weight: 700;
        }
        .script-item .actions button.run:active { background: #00e676; }
        .script-item .actions button.delete {
            background: #b71c1c;
        }
        .script-item .actions button.delete:active { background: #d32f2f; }

        .add-section {
            margin-top: 25px;
            background: #151525;
            border-radius: 16px;
            padding: 16px;
            border: 1px solid #2a2a4a;
        }
        .add-section input, .add-section textarea {
            background: #0d0d0d;
            border: 1px solid #2a2a4a;
            border-radius: 10px;
            padding: 12px;
            color: #fff;
            font-size: 14px;
            width: 100%;
            margin-bottom: 10px;
            outline: none;
            font-family: inherit;
        }
        .add-section textarea {
            height: 110px;
            resize: vertical;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }
        .add-section button {
            background: #00d4ff;
            border: none;
            color: #0d0d0d;
            font-weight: 700;
            padding: 12px;
            border-radius: 12px;
            width: 100%;
            font-size: 16px;
            cursor: pointer;
            transition: 0.2s;
        }
        .add-section button:active { background: #00b8d4; }

        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: #1a1a30;
            color: #fff;
            padding: 12px 28px;
            border-radius: 40px;
            border: 1px solid #2a2a4a;
            font-size: 14px;
            display: none;
            z-index: 9999;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            text-align: center;
            max-width: 90%;
        }

        .empty-msg {
            color: #555;
            text-align: center;
            padding: 30px 0;
            font-size: 15px;
        }

        /* Responsive mobile */
        @media (max-width: 640px) {
            #overlay {
                width: 92%;
                height: 75%;
                left: 4%;
                top: 12%;
                min-width: unset;
                min-height: unset;
            }
            .toolbar .brand { font-size: 17px; }
            .main-content { padding: 12px 14px; }
            .script-item { padding: 12px 14px; flex-wrap: wrap; gap: 8px; }
            .script-item .actions { width: 100%; justify-content: flex-end; }
        }
    </style>
</head>
<body>

    <!-- TOOLBAR -->
    <div class="toolbar">
        <div class="brand">⚡ Khôi Execute</div>
        <div class="spacer"></div>
        <button id="startStopBtn" class="start-btn">▶ START</button>
    </div>

    <!-- OVERLAY (cửa sổ nổi) -->
    <div id="overlay">
        <div class="title-bar" id="dragHandle">
            <div class="title">📦 <span>Khôi Execute</span></div>
            <button class="close-btn" id="closeOverlayBtn">✕</button>
        </div>
        <div class="content" id="overlayContent">
            <!-- Nội dung sẽ được sao chép từ main-content -->
        </div>
    </div>

    <!-- NỘI DUNG CHÍNH -->
    <div class="main-content" id="mainContent">
        <h2>📜 Script Manager</h2>
        <div id="scriptList"></div>

        <div class="add-section">
            <input type="text" id="scriptName" placeholder="Tên script (VD: AutoFarm)">
            <textarea id="scriptCode" placeholder="-- Dán code Lua tại đây"></textarea>
            <button id="saveBtn">➕ Lưu script</button>
        </div>
    </div>

    <!-- TOAST -->
    <div class="toast" id="toast"></div>

    <script>
        // ================================================================
        // 1. QUẢN LÝ SCRIPT (localStorage)
        // ================================================================
        let scripts = JSON.parse(localStorage.getItem('khôi_scripts') || '[]');

        function render() {
            const container = document.getElementById('scriptList');
            const overlayContainer = document.getElementById('overlayContent');
            if (scripts.length === 0) {
                const empty = `<div class="empty-msg">📭 Chưa có script nào.<br>Thêm script bên dưới.</div>`;
                container.innerHTML = empty;
                overlayContainer.innerHTML = empty;
                return;
            }
            let html = '';
            scripts.forEach((s, i) => {
                html += `
                    <div class="script-item">
                        <span class="name">${escapeHtml(s.name) || 'Không tên'}</span>
                        <div class="actions">
                            <button class="run" data-index="${i}">▶ Chạy</button>
                            <button class="delete" data-index="${i}">🗑</button>
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
            overlayContainer.innerHTML = html;

            // Gán sự kiện cho các nút trong cả hai container
            document.querySelectorAll('#scriptList .run, #overlayContent .run').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    const idx = parseInt(this.dataset.index);
                    runScript(idx);
                });
            });
            document.querySelectorAll('#scriptList .delete, #overlayContent .delete').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    const idx = parseInt(this.dataset.index);
                    if (confirm('Xóa script này?')) {
                        scripts.splice(idx, 1);
                        localStorage.setItem('khôi_scripts', JSON.stringify(scripts));
                        render();
                        showToast('🗑 Đã xóa');
                    }
                });
            });
        }

        function escapeHtml(text) {
            if (!text) return '';
            return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }

        // ================================================================
        // 2. CHẠY SCRIPT → COPY VÀO CLIPBOARD
        // ================================================================
        function runScript(index) {
            const script = scripts[index];
            if (!script) return;
            const fullScript = script.code || '';
            // Sao chép vào clipboard
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(fullScript).then(() => {
                    showToast(`✅ Đã sao chép script "${script.name}" vào clipboard. Hãy dán vào executor (Delta/Arceus).`);
                }).catch(() => {
                    fallbackCopy(fullScript);
                });
            } else {
                fallbackCopy(fullScript);
            }
        }

        function fallbackCopy(text) {
            // Tạo textarea tạm
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.left = '-9999px';
            ta.style.top = '-9999px';
            document.body.appendChild(ta);
            ta.select();
            try {
                document.execCommand('copy');
                showToast('✅ Đã sao chép script vào clipboard. Dán vào executor.');
            } catch (e) {
                showToast('⚠️ Không thể sao chép. Vui lòng copy thủ công.');
            }
            document.body.removeChild(ta);
        }

        // ================================================================
        // 3. LƯU SCRIPT MỚI
        // ================================================================
        document.getElementById('saveBtn').addEventListener('click', function() {
            const name = document.getElementById('scriptName').value.trim();
            const code = document.getElementById('scriptCode').value.trim();
            if (!name) { showToast('⚠️ Vui lòng nhập tên script.'); return; }
            if (!code) { showToast('⚠️ Vui lòng nhập code.'); return; }
            scripts.push({ name, code });
            localStorage.setItem('khôi_scripts', JSON.stringify(scripts));
            document.getElementById('scriptName').value = '';
            document.getElementById('scriptCode').value = '';
            render();
            showToast('✅ Đã lưu script "' + name + '"');
        });

        // ================================================================
        // 4. OVERLAY – START / STOP
        // ================================================================
        const overlay = document.getElementById('overlay');
        const startBtn = document.getElementById('startStopBtn');
        let overlayVisible = false;

        function showOverlay() {
            overlay.style.display = 'flex';
            overlayVisible = true;
            startBtn.textContent = '■ STOP';
            startBtn.classList.add('stop');
            // Đồng bộ nội dung overlay với main
            render();
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

        document.getElementById('closeOverlayBtn').addEventListener('click', hideOverlay);

        // Kéo thả overlay
        const dragHandle = document.getElementById('dragHandle');
        let isDragging = false, startX, startY, origX, origY;

        function onDragStart(e) {
            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            const clientY = e.clientY || (e.touches && e.touches[0].clientY);
            if (clientX === undefined) return;
            isDragging = true;
            const rect = overlay.getBoundingClientRect();
            startX = clientX;
            startY = clientY;
            origX = rect.left;
            origY = rect.top;
            document.addEventListener('mousemove', onDragMove);
            document.addEventListener('mouseup', onDragEnd);
            document.addEventListener('touchmove', onDragMove, { passive: true });
            document.addEventListener('touchend', onDragEnd);
        }

        function onDragMove(e) {
            if (!isDragging) return;
            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            const clientY = e.clientY || (e.touches && e.touches[0].clientY);
            if (clientX === undefined) return;
            const dx = clientX - startX;
            const dy = clientY - startY;
            overlay.style.left = (origX + dx) + 'px';
            overlay.style.top = (origY + dy) + 'px';
            overlay.style.right = 'auto';
            overlay.style.bottom = 'auto';
        }

        function onDragEnd() {
            isDragging = false;
            document.removeEventListener('mousemove', onDragMove);
            document.removeEventListener('mouseup', onDragEnd);
            document.removeEventListener('touchmove', onDragMove);
            document.removeEventListener('touchend', onDragEnd);
        }

        dragHandle.addEventListener('mousedown', onDragStart);
        dragHandle.addEventListener('touchstart', onDragStart, { passive: true });

        // ================================================================
        // 5. TOAST
        // ================================================================
        let toastTimer;

        function showToast(msg) {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.style.display = 'block';
            clearTimeout(toastTimer);
            toastTimer = setTimeout(() => { t.style.display = 'none'; }, 3000);
        }

        // ================================================================
        // 6. KHỞI TẠO
        // ================================================================
        render();
        hideOverlay(); // ẩn overlay khi load
        console.log('Khôi Execute sẵn sàng!');
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
