import os
import sys
import json
import time
import random
import asyncio
from pathlib import Path
from typing import Any, Optional, List, Dict

# Add DEV_ROOT to sys.path
DEV_ROOT = Path(__file__).resolve().parents[3]
if str(DEV_ROOT) not in sys.path:
    sys.path.append(str(DEV_ROOT))

# Add insane-search to sys.path
INSANE_SEARCH_PATH = DEV_ROOT / ".skills" / "insane-search"
if str(INSANE_SEARCH_PATH) not in sys.path:
    sys.path.append(str(INSANE_SEARCH_PATH))

from engine.transport import POOL
from engine.fetch_chain import fetch as insane_fetch
from agents.stealth_browser import StealthBrowser

class ScholarEscalator:
    def __init__(self, cookies_file: Optional[str] = None, profile: str = "scholar_labs_session"):
        self.cookies_file = cookies_file or str(Path.home() / ".msdev-browser" / "profiles" / profile / "cookies_bridge.json")
        self.profile = profile

    def load_bridged_cookies(self, host: str, impersonate: str) -> bool:
        """Load cookies from json and inject into insane-search POOL."""
        if not Path(self.cookies_file).exists():
            print(f"[ScholarEscalator] Cookies bridge file not found at {self.cookies_file}")
            return False
        try:
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            if not isinstance(cookies, list):
                print("[ScholarEscalator] Bridged cookies JSON is not a list.")
                return False
            # Default StealthBrowser UA
            ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            ok = POOL.inject_cookies(host=host, impersonate=impersonate, cookies=cookies, user_agent=ua)
            if ok:
                print(f"[ScholarEscalator] Successfully injected bridged cookies for {host} ({impersonate})")
            return ok
        except Exception as e:
            print(f"[ScholarEscalator] Failed to load bridged cookies: {e}")
            return False

    async def fetch_with_escalation(self, url: str, success_selectors: List[str], impersonate: str = "safari") -> str:
        """
        Fetch using insane-search (curl_cffi). If fails or redirects to login, 
        escalate to StealthBrowser (Playwright) and dump fresh cookies.
        """
        host = "scholar.google.com"
        self.load_bridged_cookies(host, impersonate)

        # 1. Fast path: curl_cffi
        print(f"[ScholarEscalator] Attempting fast fetch via insane-search (curl_cffi)...")
        res = insane_fetch(
            url,
            success_selectors=success_selectors,
            enable_playwright=False,
            enable_phase0=False,
            enable_learning=False,
        )

        login_required = False
        if res.ok:
            content_lower = res.content.lower()
            if "sign in" in content_lower or "로그인" in content_lower or "accounts.google.com" in res.final_url:
                login_required = True
                print("[ScholarEscalator] Google Login redirection detected in curl response.")
            elif "single molecule footprinting" in content_lower and "what is the standard of care" in content_lower:
                login_required = True
                print("[ScholarEscalator] Default example page returned from curl. Forcing escalation...")

        if res.ok and not login_required:
            print("[ScholarEscalator] Fast fetch succeeded.")
            return res.content

        # 2. Escalation path: Playwright
        print(f"[ScholarEscalator] Escalating to Stealth Browser...")
        
        bot = StealthBrowser(
            headless=False,
            profile=self.profile,
            cookies_file=self.cookies_file
        )
        try:
            await bot.start()
            
            import urllib.parse
            parsed_url = urllib.parse.urlsplit(url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            query = query_params.get('q', [''])[0]

            if "scholar_labs" in url and query:
                labs_root = "https://scholar.google.com/scholar_labs/search?hl=ko"
                print(f"[ScholarEscalator] Loading Scholar Labs root: {labs_root}")
                await bot.page.goto(labs_root)
                await asyncio.sleep(4.0)

                # 1. Login redirection detection & manual login helper
                current_url = bot.page.url
                if "accounts.google" in current_url or "signin" in current_url:
                    print("[ScholarEscalator] MANUAL INTERACTION REQUIRED: Redirected to Google Accounts. Please log in manually inside the browser.")
                    logged_in = False
                    for _ in range(150):
                        await asyncio.sleep(2.0)
                        if "scholar.google" in bot.page.url and "accounts.google" not in bot.page.url:
                            print("[ScholarEscalator] Login detected. Returning to Labs root...")
                            logged_in = True
                            break
                    if not logged_in:
                        raise TimeoutError("Login timeout or verification failed.")
                    
                    await bot.page.goto(labs_root)
                    await asyncio.sleep(5.0)

                # 2. Wait for search input explicitly
                input_selector = None
                candidates = [
                    "textarea#gs_as_i_t",
                    "textarea[name='q']",
                    "textarea",
                    "input[type='text']",
                ]
                print("[ScholarEscalator] Waiting for search input selector to be visible...")
                for sel in candidates:
                    try:
                        locator = bot.page.locator(sel)
                        await locator.wait_for(state="visible", timeout=3000)
                        input_selector = sel
                        print(f"[ScholarEscalator] Found input selector: '{sel}'")
                        break
                    except Exception:
                        continue

                if not input_selector:
                    try:
                        await bot.page.wait_for_selector("textarea", timeout=5000)
                        input_selector = "textarea"
                        print("[ScholarEscalator] Fallback to generic 'textarea'")
                    except Exception:
                        debug_path = Path(self.cookies_file).parent / "error_debug_page.html"
                        debug_path.write_text(await bot.page.content(), encoding="utf-8")
                        raise ValueError(f"Could not find search input on Scholar Labs page. Debug saved to: {debug_path}")

                await bot.mouse.click_element(selector=input_selector)
                await bot.page.fill(input_selector, query)
                await asyncio.sleep(1.0)
                await bot.page.keyboard.press("Enter")

                # Wait for search results, ignoring pre-existing example content selectors
                import re
                status_pattern = re.compile(r"(?:관련 검색 결과|Related search results).*?(\d+)")
                found = False
                for _ in range(25):
                    await asyncio.sleep(2.0)
                    content = await bot.page.content()
                    content_lower = content.lower()
                    # Check for explicit search signal OR that example texts are gone while results element is present
                    if status_pattern.search(content) or ("single molecule footprinting" not in content_lower and ".gs_r" in content):
                        print("[ScholarEscalator] Valid search results rendered.")
                        found = True
                        break

                if not found:
                    print("[ScholarEscalator] Search completion signal not detected, waiting additional 10s...")
                    await asyncio.sleep(10.0)
            else:
                await bot.browse(url)

            content = await bot.page.content()
            return content
        finally:
            await bot.close()

    async def fetch_bibtex_direct(self, data_cids: List[str], impersonate: str = "safari") -> Dict[str, str]:
        """
        Fetch BibTeX direct APIs for cids in parallel via curl_cffi. 
        Fallback to StealthBrowser if blocked.
        """
        host = "scholar.google.com"
        self.load_bridged_cookies(host, impersonate)

        bibtex_results = {}
        
        async def fetch_one(cid: str):
            url = f"https://scholar.google.com/scholar?q=info:{cid}:scholar.google.com/&output=binder&sciopts=7&hl=ko"
            for attempt in range(3):
                res = insane_fetch(
                    url,
                    success_selectors=None,
                    enable_playwright=False,
                    enable_phase0=False,
                    enable_learning=False,
                )
                if res.ok and any(k in res.content for k in ("@article", "@book", "@inproceedings", "@misc", "@phdthesis")):
                    bibtex_results[cid] = res.content.strip()
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    return
                await asyncio.sleep(random.uniform(3.0, 7.0))
            
            # Failed
            bibtex_results[cid] = ""

        # Limit concurrency to avoid fast rate-limiting
        sem = asyncio.Semaphore(2)
        
        async def sem_fetch(cid: str):
            async with sem:
                await fetch_one(cid)
                await asyncio.sleep(random.uniform(2.0, 4.0))
        
        print(f"[ScholarEscalator] Fetching {len(data_cids)} BibTeX direct APIs in parallel...", end="")
        tasks = [sem_fetch(cid) for cid in data_cids]
        await asyncio.gather(*tasks)
        print(" Done.")

        # Fallback Pool for failed cids
        failed_cids = [cid for cid, val in bibtex_results.items() if not val]
        if failed_cids:
            print(f"[ScholarEscalator] {len(failed_cids)} BibTeX direct fetches failed. Running Fallback Pool...")
            bot = StealthBrowser(headless=False, profile=self.profile, cookies_file=self.cookies_file)
            try:
                await bot.start()
                for cid in failed_cids:
                    url = f"https://scholar.google.com/scholar?q=info:{cid}:scholar.google.com/&output=binder&sciopts=7&hl=ko"
                    await bot.page.goto(url)
                    await asyncio.sleep(random.uniform(3.0, 5.0))
                    content = await bot.page.evaluate("document.body.innerText")
                    if any(k in content for k in ("@article", "@book", "@inproceedings", "@misc", "@phdthesis")):
                        bibtex_results[cid] = content.strip()
                        print(f" [BibTeX Fallback OK: {cid}]")
                    else:
                        print(f" [BibTeX Fallback Failed: {cid}]")
            finally:
                await bot.close()
                
        return bibtex_results
