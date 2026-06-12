#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests",
# ]
# ///
"""
Tübingen Index Theologicus (IxTheo) Searcher
Author: Antigravity AI
Version: 1.0.0
Description: Resolves PoW browser challenge, queries VuFind RSS search, 
             and extracts structured metadata via RIS export endpoints.
"""

import argparse
import hashlib
import json
import re
import sys
import time
import uuid
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import requests

# Default Configuration
IXTHEO_BASE_URL = "https://ixtheo.de"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

class IxTheoSearcher:
    def __init__(self, debug: bool = False):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.debug = debug
        self._cookie_token = None

    def solve_pow(self) -> str:
        """Solves the IxTheo custom cryptographic SHA-256 Proof of Work browser challenge"""
        if self._cookie_token:
            return self._cookie_token

        if self.debug:
            print("[*] Solving cryptographic browser verification challenge...", file=sys.stderr)
            
        difficulty = "0000"
        nonce = str(uuid.uuid4())
        ts = int(time.time())
        
        i = 0
        t0 = time.perf_counter()
        while True:
            msg = f"{nonce}{ts}{i}".encode("utf-8")
            hex_hash = hashlib.sha256(msg).hexdigest()
            if hex_hash.startswith(difficulty):
                token = f"{nonce}:{ts}:{i}"
                self._cookie_token = token
                if self.debug:
                    elapsed = time.perf_counter() - t0
                    print(f"[*] Solved PoW in {elapsed:.4f}s. Token: {token}", file=sys.stderr)
                return token
            i += 1

    def get_authorized_session(self) -> requests.Session:
        """Applies the resolved PoW token to the session cookies"""
        token = self.solve_pow()
        self.session.cookies.set("pow_token", token, domain="ixtheo.de", path="/")
        return self.session

    def search_records(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Queries the RSS search feed and returns record metadata summaries"""
        session = self.get_authorized_session()
        
        # VuFind RSS endpoint
        url = f"{IXTHEO_BASE_URL}/Search/Results"
        params = {
            "lookfor": query,
            "view": "rss",
            "limit": str(limit),
            "sort": "relevance"
        }
        
        if self.debug:
            print(f"[*] Querying RSS search feed: {query}", file=sys.stderr)
            
        try:
            resp = session.get(url, params=params, timeout=30)
            if resp.status_code != 200:
                print(f"[!] Error: Server returned status {resp.status_code} for search.", file=sys.stderr)
                return []
                
            # Parse XML
            root = ET.fromstring(resp.content)
            ns = {
                'dc': 'http://purl.org/dc/elements/1.1/',
                'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'
            }
            
            items = []
            for item in root.findall('.//item'):
                title_elem = item.find('title')
                link_elem = item.find('link')
                format_elem = item.find('dc:format', ns)
                date_elem = item.find('dc:date', ns)
                
                title = title_elem.text if title_elem is not None else "N/A"
                link = link_elem.text if link_elem is not None else ""
                fmt = format_elem.text if format_elem is not None else "N/A"
                year = date_elem.text if date_elem is not None else "N/A"
                
                # Extract record ID from standard URL: https://ixtheo.de/Record/1545345651
                rec_id = ""
                if link:
                    parts = link.split('/')
                    if len(parts) > 1:
                        rec_id = parts[-1]
                        
                items.append({
                    "id": rec_id,
                    "title": title,
                    "link": link,
                    "format": fmt,
                    "year": year
                })
            return items
            
        except Exception as e:
            print(f"[!] Request failed: {e}", file=sys.stderr)
            return []

    def parse_ris_metadata(self, ris_text: str) -> Dict[str, Any]:
        """Parses standard RIS file format line-by-line into structured dictionary"""
        meta = {
            "title": "",
            "authors": [],
            "journal": "",
            "year": "",
            "volume": "",
            "issue": "",
            "pages": "",
            "doi": "",
            "link": ""
        }
        
        # Clean potential BOM or blank lines
        lines = [line.strip() for line in ris_text.splitlines() if line.strip()]
        
        for line in lines:
            if not line or " - " not in line:
                continue
            tag, val = line.split(" - ", 1)
            tag = tag.strip()
            val = val.strip()
            
            if tag in ("TI", "T1"):
                meta["title"] = val
            elif tag in ("AU", "A1"):
                meta["authors"].append(val)
            elif tag in ("JO", "T2", "JF"):
                meta["journal"] = val
            elif tag == "PY":
                # Often contains YYYY/MM/DD or just YYYY
                meta["year"] = val.split('/')[0] if '/' in val else val
            elif tag == "VL":
                meta["volume"] = val
            elif tag == "IS":
                meta["issue"] = val
            elif tag == "SP":
                meta["pages"] = val
            elif tag == "EP" and meta["pages"]:
                meta["pages"] = f"{meta['pages']}-{val}"
            elif tag == "DO":
                meta["doi"] = val
            elif tag in ("UR", "LK"):
                meta["link"] = val
                
        # Stringify authors
        meta["authors"] = ", ".join(meta["authors"]) if meta["authors"] else "N/A"
        return meta

    def enrich_record_details(self, rec_id: str) -> Optional[Dict[str, Any]]:
        """Downloads RIS metadata for the specific record ID and parses it"""
        if not rec_id:
            return None
            
        session = self.get_authorized_session()
        url = f"{IXTHEO_BASE_URL}/Record/{rec_id}/Export"
        params = {"style": "RIS"}
        
        try:
            resp = session.get(url, params=params, timeout=15)
            if resp.status_code == 200:
                ris_data = self.parse_ris_metadata(resp.text)
                
                # Fallback URL to record details if link not in RIS
                if not ris_data.get("link"):
                    ris_data["link"] = f"{IXTHEO_BASE_URL}/Record/{rec_id}"
                    
                # Standardize DOI link
                if ris_data.get("doi"):
                    # Check if already a full link
                    if not ris_data["doi"].startswith("http"):
                        ris_data["link"] = f"https://doi.org/{ris_data['doi']}"
                
                return ris_data
            else:
                if self.debug:
                    print(f"[!] Failed to fetch RIS for record {rec_id}. Status: {resp.status_code}", file=sys.stderr)
                return None
        except Exception as e:
            if self.debug:
                print(f"[!] Error fetching RIS for record {rec_id}: {e}", file=sys.stderr)
            return None

def main():
    parser = argparse.ArgumentParser(description="Tübingen Index Theologicus (IxTheo) Bibliographic Searcher CLI")
    parser.add_argument("--query", "-q", required=True, help="Search query (e.g. 'Amos 4:13')")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Maximum records to retrieve (default: 10)")
    parser.add_argument("--debug", "-d", action="store_true", help="Print debug information to stderr")
    parser.add_argument("--format", "-f", choices=["json", "markdown"], default="json", help="Output format (default: json)")
    args = parser.parse_args()

    searcher = IxTheoSearcher(debug=args.debug)
    
    # 1. RSS Search
    records = searcher.search_records(args.query, limit=args.limit)
    if not records:
        if args.format == "json":
            print(json.dumps([]))
        else:
            print("검색 결과가 없습니다.")
        return

    # 2. Enrich with RIS exports
    enriched_results = []
    for rec in records:
        if args.debug:
            print(f"[*] Enriching record: {rec['title'][:40]}... (ID: {rec['id']})", file=sys.stderr)
            
        details = searcher.enrich_record_details(rec["id"])
        if details:
            details["format"] = rec["format"]
            enriched_results.append(details)
        else:
            # Fallback if RIS fails
            enriched_results.append({
                "title": rec["title"],
                "authors": "N/A",
                "journal": "N/A",
                "year": rec["year"],
                "volume": "",
                "issue": "",
                "pages": "",
                "doi": "",
                "link": rec["link"],
                "format": rec["format"]
            })

    # 3. Output
    if args.format == "json":
        print(json.dumps(enriched_results, indent=2, ensure_ascii=False))
    else:
        # Markdown Output
        print(f"# 📚 IxTheo (Index Theologicus) 검색 결과: \"{args.query}\"\n")
        for idx, item in enumerate(enriched_results, 1):
            title = item["title"]
            authors = item["authors"]
            journal = item["journal"]
            year = item["year"]
            link = item["link"]
            doi = item["doi"]
            fmt = item.get("format", "N/A")
            
            if link:
                print(f"### {idx}. [{title}]({link})")
            else:
                print(f"### {idx}. {title}")
                
            print(f"- **저자**: {authors}")
            print(f"- **유형**: {fmt} | **발행년도**: {year}")
            
            if journal and journal != "N/A":
                vol_info = []
                if item.get("volume"):
                    vol_info.append(f"Vol. {item['volume']}")
                if item.get("issue"):
                    vol_info.append(f"No. {item['issue']}")
                if item.get("pages"):
                    vol_info.append(f"pp. {item['pages']}")
                
                extra = f" ({', '.join(vol_info)})" if vol_info else ""
                print(f"- **출처**: *{journal}*{extra}")
                
            if doi:
                print(f"- **DOI**: [{doi}](https://doi.org/{doi})")
            print()

if __name__ == "__main__":
    main()
