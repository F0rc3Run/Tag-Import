import requests
import base64
import os

PROTOCOLS = [
    'vmess://', 'vless://', 'trojan://', 'ss://', 'shadowsocks://',
    'hysteria://', 'hysteria2://', 'reality://', 'tuic://', 'ssh://'
]

def clean_line(line):
    for proto in PROTOCOLS:
        if line.startswith(proto):
            if '#' in line:
                line = line.split('#')[0]
            return line + '#@F0rc3Run'
    return None

def main():
    urls = os.getenv("SUB_LINKS", "").split()
    all_lines = []

    for url in urls:
        try:
            print(f"[INFO] Downloading: {url}")
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            content = res.content.decode()

            # اگر base64 بود
            try:
                decoded = base64.b64decode(content).decode()
                lines = decoded.strip().splitlines()
            except:
                lines = content.strip().splitlines()

            cleaned = [clean_line(line.strip()) for line in lines]
            all_lines.extend([l for l in cleaned if l])
        except Exception as e:
            print(f"[ERROR] {url} => {e}")

    os.makedirs("output", exist_ok=True)
    with open("output/cleaned.txt", "w") as f:
        f.write("\n".join(all_lines))
    print(f"[DONE] {len(all_lines)} config cleaned and saved.")

if __name__ == "__main__":
    main()
