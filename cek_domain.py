import requests

TELEGRAM_TOKEN = "7936697834:AAEUjyS3Nq-iPFGdcgiE4YGINlK3vq3n1kI"
CHAT_ID = "-4806495065"  # Ganti dengan ID grup kamu
DOMAINS = [
    "retrotengah.com",
    "retroaman.com",
    "senjacerdas.com",
    "senjaluas.com",
    "prediksi2.senjalive.pro",
    "buku.retroprediksi.live",
    "live.putaransenang.xyz"
]

def cek_domain(domain):
    url = f"https://check.skiddle.id/?domain={domain}&json=true"
    try:
        resp = requests.get(url, timeout=10)
        res = resp.json().get(domain, {})
        return res.get("blocked", False)
    except Exception as e:
        return f"Gagal cek: {e}"

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": pesan, "parse_mode":"Markdown"})

if __name__ == "__main__":
    hasil = []
    for d in DOMAINS:
        status = cek_domain(d)
        if isinstance(status, str):
            hasil.append(f"⚠️ {d} - {status}")
        elif status:
            hasil.append(f"🚫 {d} *NAWALA😭😭😭*")
        else:
            hasil.append(f"✅ {d} AMAN😁😁😁")

    pesan = "📡 *Hasil Cek TrustPositif:*\n\n" + "\n".join(hasil)
    kirim_telegram(pesan)
    print(pesan)
