import requests
import base64
import os

PROTOCOLS = {
    'vmess': 'vmess://',
    'vless': 'vless://',
    'trojan': 'trojan://',
    'ss': 'ss://',
    'shadowsocks': 'ss://',
    'hysteria': 'hysteria://',
    'hysteria2': 'hysteria2://',
    'reality': 'reality://',
    'tuic': 'tuic://',
    'ssh': 'ssh://'
}

def get_protocol(line):
    for proto, prefix in PROTOCOLS.items():
        if line.startswith(prefix):
            return proto
    return None

def clean_line(line):
    if '#' in line:
        line = line.split('#')[0]
    return line + '#@F0rc3Run'

def main():
    urls = os.getenv("SUB_LINKS", "").split()
    protocol_data = {proto: [] for proto in PROTOCOLS}

    for url in urls:
        try:
            print(f"[INFO] Downloading: {url}")
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            content = res.content.decode()

            try:
                decoded = base64.b64decode(content).decode()
                lines = decoded.strip().splitlines()
            except:
                lines = content.strip().splitlines()

            for line in lines:
                line = line.strip()
                proto = get_protocol(line)
                if proto:
                    cleaned = clean_line(line)
                    protocol_data[proto].append(cleaned)
        except Exception as e:
            print(f"[ERROR] {url} => {e}")

    os.makedirs("output", exist_ok=True)
    for proto, lines in protocol_data.items():
        if lines:
            with open(f"output/{proto}.txt", "w") as f:
                f.write("\n".join(sorted(set(lines))))
            print(f"[OK] Saved {len(lines)} configs to output/{proto}.txt")

if __name__ == "__main__":
    main()
