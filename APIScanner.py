# Developer: @spyizxa
# Telegram: @spyizxa_0day
# iyi kullanımlar :)
import re
import os
import sys
import time
import random
import signal
import asyncio
import aiohttp
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import rich.box as box

console = Console()
ua = UserAgent()

TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""

async def telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        async with aiohttp.ClientSession() as sess:
            await sess.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg[:4000], "parse_mode": "HTML"})
    except:
        pass

def notify(msg):
    asyncio.run(telegram(msg))

class APIScanner:
    def __init__(self, target_url, threads=12, timeout=15):
        self.target_url = target_url if target_url.startswith(("http://", "https://")) else f"https://{target_url}"
        self.base_domain = urlparse(self.target_url).netloc.replace("www.", "")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": ua.random,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        })
        self.timeout = timeout
        self.threads = threads
        self.endpoints = set()
        self.js_files = set()
        self.tested = set()
        self.quiet = False
        self.multi = False

        self.patterns = [
            r'["\'](/?api[/\w\-.]+)["\']',
            r'["\'](/?v[1-9][/\w\-.]+)["\']',
            r'["\'](/?graphql[/\w\-.?]+)["\']',
            r'["\'](/?admin[/\w\-.]+)["\']',
            r'["\'](/?auth[/\w\-.]+)["\']',
            r'["\'](/?rest[/\w\-.]+)["\']',
            r'["\'](/?_next/data/[^\']+)["\']',
            r'(?:fetch|axios|\$\.get|\$\.post)\s*\(\s*["\']([^"\'{}]+)["\']',
            r'src=["\']([^"\']+\.js)["\']'
        ]

    def banner(self):
        b = '''
 ▄▄▄       ██▓███   ██▓  ██████  ▄████▄   ▄▄▄       ███▄    █  ███▄    █ ▓█████  ██▀███  
▒████▄    ▓██░  ██▒▓██▒▒██    ▒ ▒██▀ ▀█  ▒████▄     ██ ▀█   █  ██ ▀█   █ ▓█   ▀ ▓██ ▒ ██▒
▒██  ▀█▄  ▓██░ ██▓▒▒██▒░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██  ▀█ ██▒▓██  ▀█ ██▒▒███   ▓██ ░▄█ ▒
░██▄▄▄▄██ ▒██▄█▓▒ ▒░██░  ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▓██▒  ▐▌██▒▓██▒  ▐▌██▒▒▓█  ▄ ▒██▀▀█▄  
 ▓█   ▓██▒▒██▒ ░  ░░██░▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒▒██░   ▓██░▒██░   ▓██░░▒████▒░██▓ ▒██▒
 ▒▒   ▓▒█░▒▓▒░ ░  ░░▓  ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
  ▒   ▒▒ ░░▒ ░      ▒ ░░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░░ ░░   ░ ▒░░ ░░   ░ ▒░ ░ ░  ░  ░▒ ░ ▒░
  ░   ▒   ░░        ▒ ░░  ░  ░  ░          ░   ▒      ░   ░ ░    ░   ░ ░    ░     ░░   ░ 
      ░  ░          ░        ░  ░ ░            ░  ░         ░          ░    ░  ░   ░     
        '''
        console.print(Panel.fit(Text(b, style="bold red"), title="APIScanner", subtitle="WELCOME", border_style="bright_blue"))

    def delay(self):
        time.sleep(random.uniform(0.6, 1.8))

    def normalize(self, url):
        if url.startswith("//"): return "https:" + url
        if url.startswith("/"): return f"https://www.{self.base_domain}{url}"
        if url.startswith("http"): return url
        return urljoin(self.target_url, url)

    def valid_domain(self, url):
        try:
            domain = urlparse(url).netloc.lower().replace("www.", "")
            return self.base_domain in domain or domain.endswith("." + self.base_domain)
        except:
            return False

    def good_path(self, path):
        if not path or len(path) < 4 or path in {"/", "#", "."}:
            return False
        trash = ["px","em","rem","vh","vw","jpg","png","gif","svg","webp","ico","woff","ttf","css","jsonp","callback","lütfen","giriniz","please","enter","jquery","bootstrap"]
        if any(x in path.lower() for x in trash):
            return False
        if re.match(r"^/\d+$", path) or path.lstrip("/") in {"80","443","400","403","404","500"}:
            return False
        return True

    def crawl(self, url):
        try:
            self.delay()
            r = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            if r.status_code != 200: return
            ct = r.headers.get("Content-Type", "")
            if "html" in ct:
                self.parse_html(r.text)
            elif "javascript" in ct or url.endswith(".js"):
                self.parse_js(r.text)
        except:
            pass

    def parse_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        for script in soup.find_all("script", src=True):
            js = self.normalize(script["src"])
            if self.valid_domain(js) and js not in self.js_files:
                self.js_files.add(js)
                if not self.quiet:
                    console.print(f"[cyan][+] JS → {js}[/]")

        for script in soup.find_all("script"):
            if script.string:
                self.extract(script.string)

    def parse_js(self, content):
        self.extract(content)

    def extract(self, text):
        for pattern in self.patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                raw = match.group(1) if match.groups() else match.group(0)
                raw = raw.strip("\"'")
                if raw.startswith(("http", "//", "/")):
                    url = self.normalize(raw)
                    path = urlparse(url).path
                    if self.valid_domain(url) and self.good_path(path) and url not in self.endpoints:
                        self.endpoints.add(url)
                        if not self.quiet:
                            console.print(f"[bold green][+] ENDPOINT → {url}[/]")
                        self.test(url)

    def test(self, url):
        if url in self.tested or self.quiet: return
        self.tested.add(url)
        result = []
        for method in ["GET", "POST"]:
            try:
                self.delay()
                r = self.session.request(method, url, timeout=self.timeout)
                size = len(r.text)
                if r.status_code < 300:
                    result.append(f"{method} → {r.status_code} [LIVE] → {size}B")
                elif r.status_code == 401:
                    result.append(f"{method} → 401 [AUTH]")
                elif r.status_code == 403:
                    result.append(f"{method} → 403 [FORBIDDEN]")
                else:
                    result.append(f"{method} → {r.status_code}")
            except:
                result.append(f"{method} → ERROR")
        if not self.quiet:
            table = Table(title=url, box=box.ROUNDED)
            table.add_column("Method", style="cyan")
            table.add_column("Result", style="white")
            for line in result:
                m = line.split(" → ")[0]
                res = " → ".join(line.split(" → ")[1:])
                color = "green" if "LIVE" in res else "yellow" if "AUTH" in res else "red"
                table.add_row(m, res, style=color)
            console.print(table)

    def report(self):
        if not self.multi or not self.endpoints: return
        msg = f"<b>API FOUND</b>\n<b>Target:</b> <code>{self.target_url}</code>\n<b>Count:</b> {len(self.endpoints)}\n\n"
        for ep in list(self.endpoints)[:15]:
            msg += f"<code>{ep}</code>\n"
        if len(self.endpoints) > 15:
            msg += f"\n... and {len(self.endpoints)-15} more"
        notify(msg)

    def run(self):
        if not self.quiet:
            console.clear()
            self.banner()
            console.print(Panel(f"Target → [bold cyan]{self.target_url}[/]", title="Starting", border_style="bright_blue"))
        self.crawl(self.target_url)
        if self.js_files:
            if not self.quiet:
                console.print(Panel(f"JS Files → {len(self.js_files)}", border_style="bright_black"))
            with ThreadPoolExecutor(max_workers=self.threads) as pool:
                pool.map(self.crawl, self.js_files)

        if self.endpoints:
            if not self.quiet:
                table = Table(title="Endpoints Found", box=box.DOUBLE_EDGE)
                table.add_column("No", style="dim")
                table.add_column("URL", style="cyan")
                for i, ep in enumerate(sorted(self.endpoints), 1):
                    table.add_row(str(i), ep)
                console.print(table)

        if not self.quiet:
            console.print(Panel(
                f"[bold green]Scan Finished!\n"
                f"[cyan]Target:[/] {self.target_url}\n"
                f"[green]Endpoints:[/] {len(self.endpoints)}\n"
                f"[yellow]JS Files:[/] {len(self.js_files)}",
                title="RESULT", border_style="bright_green", padding=(1,4)
            ))
        self.report()

def main():
    def stop(a, b):
        console.print("\n[red]Stopped.[/]")
        sys.exit(0)
    signal.signal(signal.SIGINT, stop)

    while True:
        console.clear()
        APIScanner("example.com").banner()
        console.print("\n[bold red]Welcome to APIScanner :)[/]")
        console.print("[cyan][1] Single Target[/]")
        console.print("[cyan][2] Multi Scan (sites.txt)[/]")
        console.print("[dim]Q → Exit[/]")
        choice = console.input("\n[white]Choice → [/]").strip().lower()

        if choice == "1":
            target = console.input("\nTarget → ").strip()
            if target.lower() == "q": break
            APIScanner(target).run()
            input("\nPress Enter...")
        elif choice == "2":
            if not os.path.exists("sites.txt"):
                open("sites.txt", "w").write("example.com\n")
                console.print("[green]sites.txt created[/]")
                input("Press Enter...")
                continue
            sites = [l.strip() for l in open("sites.txt") if l.strip() and not l.startswith("#")]
            notify(f"Multi scan started → {len(sites)} sites")
            for i, site in enumerate(sites, 1):
                url = site if site.startswith("http") else "https://" + site
                console.print(f"[{i}/{len(sites)}] → {url}")
                s = APIScanner(url)
                s.quiet = True
                s.multi = True
                s.run()
                time.sleep(0.7)
            notify("Multi scan finished!")
        elif choice == "q":
            break

if __name__ == "__main__":
    main()
