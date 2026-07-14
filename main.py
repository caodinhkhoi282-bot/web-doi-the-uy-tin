from flask import Flask, render_template
import os

# Cấu hình Flask nhận diện thư mục templates chứa giao diện html
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    # Gọi file index.html từ thư mục templates
    return render_template('index.html')

if __name__ == '__main__':
    # Tự động nhận cổng PORT từ môi trường Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    <!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roblox VN - VNGGames Shop</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: #0d0f11; color: #333333; min-height: 100vh; display: flex; justify-content: center; align-items: flex-start; }
        #loading-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: #ffffff; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 9999; transition: opacity 0.5s ease; }
        .vng-loader { position: relative; width: 120px; height: 120px; display: flex; justify-content: center; align-items: center; }
        .vng-loader::before { content: ""; position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 4px solid #f1f1f1; border-top: 4px solid #f36f21; animation: spin 1s linear infinite; }
        .vng-logo-text { font-size: 20px; font-weight: 900; color: #f36f21; text-align: center; line-height: 1; }
        .vng-logo-sub { font-size: 10px; font-weight: bold; color: #4a4a4a; letter-spacing: 2px; text-transform: uppercase; margin-top: 2px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        #shop-screen { display: none; width: 100%; max-width: 480px; background: linear-gradient(180deg, rgba(21, 26, 30, 0.8) 0%, #0d0f11 100%), url('https://images.rbxcdn.com/9da9c72e414c59b66ee0dbfb696b0143.jpg'); background-size: cover; background-position: center; background-attachment: fixed; min-height: 100vh; padding-bottom: 80px; position: relative; }
        .header-bar { background-color: #ffffff; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e5e5e5; }
        .header-left { font-weight: bold; font-size: 14px; color: #f36f21; }
        .header-left span { color: #333; font-weight: normal; margin-left: 5px; }
        .main-content { padding: 15px; }
        .game-title-section { display: flex; align-items: center; margin-bottom: 20px; margin-top: 10px; }
        .game-icon { width: 50px; height: 50px; background-color: #0074bd; border-radius: 10px; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 8px rgba(0,0,0,0.3); margin-right: 15px; }
        .game-icon svg { width: 30px; height: 30px; fill: #ffffff; }
        .game-name { color: #ffffff; font-size: 18px; font-weight: bold; }
        .card-box { background-color: #ffffff; border-radius: 12px; padding: 20px 15px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
        .card-title { font-size: 15px; font-weight: bold; color: #111111; margin-bottom: 15px; }
        .input-group label { display: block; font-size: 13px; color: #666; margin-bottom: 5px; }
        .input-group input { width: 100%; padding: 12px; border: 1px solid #cccccc; border-radius: 6px; font-size: 15px; outline: none; background-color: #f9f9f9; }
        .input-group input:focus { border-color: #f36f21; background-color: #fff; }
        .package-grid { display: grid; grid-template-columns: 1fr; gap: 12px; margin-top: 10px; }
        .package-item { border: 1px solid #eeeeee; border-radius: 8px; padding: 12px; display: flex; align-items: center; justify-content: space-between; background-color: #fafafa; cursor: pointer; transition: all 0.2s ease; }
        .package-item:hover { border-color: #f36f21; background-color: #fffaf7; }
        .p-info { display: flex; align-items: center; }
        .p-icon-box { width: 45px; height: 45px; background: #25282a; border-radius: 6px; display: flex; justify-content: center; align-items: center; margin-right: 12px; }
        .p-robux-badge { background: #ffffff; border-radius: 12px; padding: 2px 8px; font-size: 12px; font-weight: bold; color: #111; display: flex; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .p-robux-badge::before { content: "⬡"; color: #efb016; margin-right: 3px; font-weight: 900; }
        .p-det { display: flex; flex-direction: column; }
        .p-name { font-size: 14px; font-weight: bold; color: #222; }
        .p-price { font-size: 13px; color: #f36f21; font-weight: bold; margin-top: 2px; }
        .btn-buy-add { width: 32px; height: 32px; border-radius: 6px; background-color: #f36f21; color: #ffffff; display: flex; justify-content: center; align-items: center; font-size: 20px; font-weight: bold; }
        .cookie-banner { position: fixed; bottom: 0; left: 50%; transform: translateX(-50%); width: 100%; max-width: 480px; background-color: rgba(25, 25, 25, 0.95); color: #ffffff; padding: 12px 15px; font-size: 11px; line-height: 1.4; z-index: 900; border-top: 1px solid #333; }
        .cookie-btns { display: flex; justify-content: flex-end; gap: 10px; margin-top: 8px; }
        .cookie-btn-alt { background: #ffffff; color: #333; border: none; padding: 5px 10px; font-size: 11px; border-radius: 4px; font-weight: bold; }
        .cookie-btn-main { background: #f36f21; color: #ffffff; border: none; padding: 5px 10px; font-size: 11px; border-radius: 4px; font-weight: bold; }
        #success-screen { display: none; width: 100%; max-width: 480px; background-color: #f4f6f8; min-height: 100vh; padding: 15px; }
        .success-box { background-color: #ffffff; border-radius: 12px; padding: 25px 20px; margin-bottom: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        .success-icon-circle { width: 45px; height: 45px; background-color: #e1f5fe; border-radius: 50%; display: inline-flex; justify-content: center; align-items: center; margin-bottom: 12px; }
        .success-icon-circle svg { width: 24px; height: 24px; fill: #2ea655; }
        .success-title { color: #2ea655; font-size: 20px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 20px; }
        .info-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; font-size: 15px; }
        .info-label { color: #777777; }
        .info-value { color: #111111; font-weight: 600; }
        .receipt-box { background-color: #ffffff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        .receipt-image-container { background-color: #1a1c1e; border-radius: 8px; padding: 20px; display: flex; justify-content: center; align-items: center; margin-bottom: 20px; }
        .receipt-robux-card { display: flex; flex-direction: column; align-items: center; }
        .receipt-hexagon { font-size: 42px; color: #efb016; line-height: 1; margin-bottom: 5px; }
        .receipt-robux-amount { background: #ffffff; color: #111; font-weight: bold; padding: 4px 15px; border-radius: 15px; font-size: 16px; }
        .btn-back-home { width: 100%; background-color: #f36f21; color: white; border: none; padding: 14px; font-size: 15px; font-weight: bold; border-radius: 8px; margin-top: 20px; cursor: pointer; }
    </style>
</head>
<body>
    <div id="loading-screen">
        <div class="vng-loader"><div class="vng-logo-text">VNG<br><span class="vng-logo-sub">Games</span></div></div>
    </div>
    <div id="shop-screen">
        <div class="header-bar">
            <div class="header-left">vnggames<span>Shop</span></div>
            <div style="font-size: 18px; color: #666;">☰</div>
        </div>

        <div class="main-content">
            <div class="game-title-section">
                <div class="game-icon">
                    <svg viewBox="0 0 36 36"><path d="M26.2,26.2H9.8V9.8h16.5V26.2z M15,15h6v6h-6V15z"/></svg>
                </div>
                <div class="game-name">Roblox VN</div>
            </div>

            <div class="card-box">
                <div class="card-title">1. Thông tin nhân vật</div>
                <div class="input-group">
                    <label for="player_id">ID nhân vật:</label>
                    <input type="text" id="player_id" placeholder="Nhập ID/NAME nhân vật..." value="trung12345ii">
                </div>
            </div>

            <div class="card-box">
                <div class="card-title">2. Chọn gói</div>
                <div class="package-grid">
                    
                    <div class="package-item" onclick="triggerPurchase('Gói 55 Robux', '55 Robux')">
                        <div class="p-info">
                            <div class="p-icon-box">
                                <div class="p-robux-badge">55</div>
                            </div>
                            <div class="p-det">
                                <span class="p-name">Gói 55 Robux</span>
                                <span class="p-price">20.000 VND</span>
                            </div>
                        </div>
                        <div class="btn-buy-add">+</div>
                    </div>

                    <div class="package-item" onclick="triggerPurchase('Gói 300 Robux', '300 Robux')">
                        <div class="p-info">
                            <div class="p-icon-box">
                                <div class="p-robux-badge">300</div>
                            </div>
                            <div class="p-det">
                                <span class="p-name">Gói 300 Robux</span>
                                <span class="p-price">100.000 VND</span>
                            </div>
                        </div>
                        <div class="btn-buy-add">+</div>
                    </div>

                    <div class="package-item" onclick="triggerPurchase('Gói 500 Robux', '500 Robux')">
                        <div class="p-info">
                            <div class="p-icon-box">
                                <div class="p-robux-badge">500</div>
                            </div>
                            <div class="p-det">
                                <span class="p-name">Gói 500 Robux</span>
                                <span class="p-price">160.000 VND</span>
                            </div>
                        </div>
                        <div class="btn-buy-add">+</div>
                    </div>

                    <div class="package-item" onclick="triggerPurchase('Gói 10k Robux', '10.000 Robux')">
                        <div class="p-info">
                            <div class="p-icon-box">
                                <div class="p-robux-badge">10k</div>
                            </div>
                            <div class="p-det">
                                <span class="p-name">Gói 10k Robux</span>
                                <span class="p-price">3.200.000 VND</span>
                            </div>
                        </div>
                        <div class="btn-buy-add">+</div>
                    </div>

                    <div class="package-item" onclick="triggerPurchase('Gói 100k Robux', '100.000 Robux')">
                        <div class="p-info">
                            <div class="p-icon-box">
                                <div class="p-robux-badge">100k</div>
                            </div>
                            <div class="p-det">
                                <span class="p-name">Gói 100k Robux</span>
                                <span class="p-price">32.000.000 VND</span>
                            </div>
                        </div>
                        <div class="btn-buy-add">+</div>
                    </div>

                </div>
            </div>
        </div>

        <div class="cookie-banner">
            Chúng tôi sử dụng cookie để cải thiện, cá nhân hóa trải nghiệm của bạn và phân tích lưu lượng truy cập trang web... 
            <div class="cookie-btns">
                <button class="cookie-btn-alt">Tùy chỉnh</button>
                <button class="cookie-btn-main">Đồng ý tất cả</button>
            </div>
        </div>
    </div>

    <div id="success-screen">
        <div class="success-box">
            <div class="success-icon-circle">
                <svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
            </div>
            <div class="success-title">Thanh toán thành công</div>
            
            <div class="info-row">
                <span class="info-label">Máy chủ:</span>
                <span class="info-value">Server-1</span>
            </div>
            <div class="info-row">
                <span class="info-label">ID nhân vật:</span>
                <span class="info-value" id="res-id">trung12345ii</span>
            </div>
            <div class="info-row">
                <span class="info-label">Nhân vật:</span>
                <span class="info-value" id="res-name">trung12345ii</span>
            </div>
        </div>

        <div class="receipt-box">
            <div class="receipt-image-container">
                <div class="receipt-robux-card">
                    <span class="receipt-hexagon">⬡</span>
                    <span class="receipt-robux-amount" id="res-badge">55</span>
                </div>
            </div>

            <div class="info-row">
                <span class="info-label">Tên gói nạp</span>
                <span class="info-value" id="res-package">Gói 55 Robux</span>
            </div>
            <div class="info-row">
                <span class="info-label">Số lượng</span>
                <span class="info-value">x1</span>
            </div>
            <div class="info-row" style="margin-bottom: 0;">
                <span class="info-label">Mã giao dịch</span>
                <span class="info-value" id="res-txid">3129858175340134400</span>
            </div>
            
            <button class="btn-back-home" onclick="goBackHome()">Quay lại cửa hàng</button>
        </div>
    </div>

    <script>
        window.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => {
                const loader = document.getElementById('loading-screen');
                loader.style.opacity = '0';
                setTimeout(() => {
                    loader.style.display = 'none';
                    document.getElementById('shop-screen').style.display = 'block';
                }, 500);
            }, 2000);
        });

        function triggerPurchase(packageName, robuxAmount) {
            const playerId = document.getElementById('player_id').value.trim();
            if(!playerId) {
                alert("Vui lòng nhập ID nhân vật trước!");
                return;
            }

            const loader = document.getElementById('loading-screen');
            loader.style.display = 'flex';
            loader.style.opacity = '1';

            setTimeout(() => {
                document.getElementById('res-id').innerText = playerId;
                document.getElementById('res-name').innerText = playerId;
                document.getElementById('res-package').innerText = packageName;
                document.getElementById('res-badge').innerText = robuxAmount.replace(" Robux", "");
                
                const randomTxId = "3129" + Math.floor(100000000000000 + Math.random() * 90000000000000);
                document.getElementById('res-txid').innerText = randomTxId;

                document.getElementById('shop-screen').style.display = 'none';
                loader.style.opacity = '0';
                setTimeout(() => {
                    loader.style.display = 'none';
                    document.getElementById('success-screen').style.display = 'block';
                }, 400);

            }, 1500);
        }

        function goBackHome() {
            document.getElementById('success-screen').style.display = 'none';
            document.getElementById('shop-screen').style.display = 'block';
        }
    </script>
</body>
</html>
