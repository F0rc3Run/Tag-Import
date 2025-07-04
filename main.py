import os
import requests
import base64

PROTOCOLS = {
    'vmess': 'vmess://',
    'vless': 'vless://',
    'trojan': 'trojan://',
    'shadowsocks': 'ss://',
    'hysteria': 'hysteria://',
    'hysteria2': 'hysteria2://',
    'reality': 'reality://',
    'tuic': 'tuic://',
    'ssh': 'ssh://'
}

def clean_line(line: str, tag="@F0rc3Run") -> str:
    if '#' in line:
        line = line.split('#')[0]
    return line + f'#{tag}'

def fetch_subscription(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        raw = base64.b64decode(r.text.strip()).decode()
        return [line.strip() for line in raw.splitlines() if any(line.startswith(p) for p in PROTOCOLS.values())]
    except Exception as e:
        print(f"[ERROR] Cannot fetch {url}: {e}")
        return []

def main():
    urls = os.getenv("SUB_LINKS", "").splitlines()
    if not urls:
        print("[ERROR] SUB_LINKS is empty.")
        return

    cleaned = []
    for url in urls:
        for line in fetch_subscription(url.strip()):
            cleaned.append(clean_line(line))

    unique = list(set(cleaned))
    output = "\n".join(unique).encode()
    encoded = base64.b64encode(output).decode()

    os.makedirs("output", exist_ok=True)
    with open("output/cleaned.txt", "w") as f:
        f.write(encoded)
    print(f"[INFO] Wrote {len(unique)} cleaned configs to output/cleaned.txt")

if __name__ == "__main__":
    main()
