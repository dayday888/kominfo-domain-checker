import requests, os

# Ambil dari Secrets GitHub
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Baca file domains.txt
with open("domains.txt") as f:
    DOMAINS = [d.strip() for d in f if d.strip()]

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
    requests.post(url, data={"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"})

if __name__ == "__main__":
    total = len(DOMAINS)
    gagal = []
    blokir = []
    aman = []

    for d in DOMAINS:
        status = cek_domain(d)
        if isinstance(status, str):
            gagal.append(f"{d} ({status})")
        elif status:
            blokir.append(d)
        else:
            aman.append(d)

    # Format pesan
    if len(blokir) == 0:
        pesan = f"✅ Semua domain aman dicek ({total} domain total)."
    else:
        diblokir = ", ".join(blokir)
        pesan = f"⚠️ {len(blokir)} domain diblokir: {diblokir} — sisanya aman."

    # Tambahkan info gagal jika ada
    if gagal:
        gagal_str = "\n\n⚠️ Gagal dicek:\n" + "\n".join(gagal)
        pesan += gagal_str

    kirim_telegram(pesan)
    print(pesan)
