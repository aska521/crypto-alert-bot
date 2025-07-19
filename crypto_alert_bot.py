
import requests
import time

# === Konfigurasi Bot ===
BOT_TOKEN = '8095505771:AAE91unWUpkV9GW3AC7tkqVEVwyDd5fOy-w'
CHAT_ID = '1407624802'

# === Pengaturan User ===
USER_PILIHAN = {
    "coin": "PYTH",               # Contoh coin favorit
    "frekuensi": 900,             # 900 detik = 15 menit
    "mode": "whale_volume",       # whale_volume / breakout / rsi_alert
}

# === Fungsi Kirim Notifikasi Telegram ===
def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Gagal kirim pesan:", e)

# === Ambil Data Dexscreener (Contoh: PYTH) ===
def ambil_data_dexscreener():
    url = "https://api.dexscreener.com/latest/dex/pairs/solana/7moA6UsmqjMHkgxewzptmC4oycVEm8eRJe2iQKKpNoJx"  # Pair PYTH/USDC
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json().get("pair", {})
    except:
        return None

# === Cek Sinyal Berdasarkan Mode ===
def cek_sinyal(user_pref):
    coin = user_pref["coin"].upper()
    mode = user_pref["mode"]
    data = ambil_data_dexscreener()
    if not data:
        return

    price = float(data.get("priceUsd", 0))
    volume = float(data.get("volume", {}).get("h24", 0))
    fdv = float(data.get("fdv", 0))

    if mode == "whale_volume" and volume > 500000:
        pesan = f"""
🚨 <b>ALERT: {coin} Volume Spike!</b>
💰 Harga: ${price:.4f}
📊 Volume 24 jam: ${volume:,.0f}
📈 FDV: ${fdv:,.0f}
🎯 Rekomendasi: Pantau break $0.35 (TP) dengan SL $0.29
        """
        kirim_telegram(pesan)

    elif mode == "breakout" and price > 0.35:
        pesan = f"""
🚀 <b>{coin} Breakout Alert!</b>
💸 Harga saat ini: ${price:.4f}
💡 Break resistance $0.35 → momentum naik kuat
🔒 SL disarankan: $0.33 | TP: $0.40
        """
        kirim_telegram(pesan)

# === Looping Otomatis ===
def main_loop():
    while True:
        cek_sinyal(USER_PILIHAN)
        time.sleep(USER_PILIHAN["frekuensi"])

# === Jalankan Bot ===
main_loop()
