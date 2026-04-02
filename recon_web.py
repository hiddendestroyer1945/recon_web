import requests
import socket
import json
import os
import logging
import dns.resolver
import whois
import random
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any, List

# Load environment variables
load_dotenv()
BUILTWITH_KEY = os.getenv("BUILTWITH_API_KEY")

# High-Health Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

class ReconWeb:
    """
    Professional Web Intelligence Engine.
    Optimized for ProxyChains4 and Tor Sockets.
    """
    def __init__(self, target: str):
        self.target = target.replace("http://", "").replace("https://", "").strip("/")
        self.url = f"https://{self.target}"
        self.timeout = 30  # Essential for Tor latency
        self.report_path = os.path.join("reports", "results.json")
        self.data: Dict[str, Any] = {
            "domain": self.target,
            "scan_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "connection_type": "ProxyChains4/Tor"
        }

    def _get_headers(self) -> Dict[str, str]:
        """Rotates User-Agents to mimic different Linux browsers."""
        agents = [
            "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ]
        return {"User-Agent": random.choice(agents)}

    def get_builtwith_data(self):
        """Grabs tech stack, apps, and versions from BuiltWith."""
        if not BUILTWITH_KEY:
            logger.warning("No BuiltWith API Key found. Skipping tech lookup.")
            return
        
        logger.info(f"[*] Querying BuiltWith API for {self.target}...")
        api_url = f"https://api.builtwith.com/v22/api.json?KEY={BUILTWITH_KEY}&LOOKUP={self.target}"
        try:
            resp = requests.get(api_url, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            raw = resp.json()
            
            techs = []
            for path in raw.get('Paths', []):
                for t in path.get('Technologies', []):
                    techs.append({
                        "name": t.get('Name'),
                        "version": t.get('Version', 'N/A'),
                        "category": t.get('Tag'),
                        "last_seen": t.get('LastDetected')
                    })
            self.data["technologies"] = techs
        except Exception as e:
            logger.error(f"BuiltWith lookup failed: {e}")

    def get_network_details(self):
        """IP, Geolocation, and DNS records via Tor."""
        logger.info("[*] Extracting Network and DNS intelligence...")
        try:
            ip = socket.gethostbyname(self.target)
            # Geo lookup through Tor circuit
            geo = requests.get(f"https://ipapi.co/{ip}/json/", timeout=self.timeout).json()

            dns_res = {}
            for q in ['A', 'MX', 'NS', 'TXT']:
                try:
                    answers = dns.resolver.resolve(self.target, q)
                    dns_res[q] = [str(r) for r in answers]
                except: continue

            self.data["network"] = {
                "ip": ip,
                "isp": geo.get("org"),
                "location": f"{geo.get('city')}, {geo.get('country_name')}",
                "dns_records": dns_res
            }
        except Exception as e:
            logger.error(f"Network discovery failed: {e}")

    def get_domain_registration(self):
        """WHOIS registration, update, and expiry timestamps."""
        logger.info("[*] Fetching WHOIS registration data...")
        try:
            w = whois.whois(self.target)
            self.data["registration"] = {
                "registrar": w.registrar,
                "created": str(w.creation_date),
                "updated": str(w.updated_date),
                "expires": str(w.expiration_date)
            }
        except Exception as e:
            logger.error(f"WHOIS lookup failed: {e}")

    def get_http_metadata(self):
        """Server versions, SEO, and Social links."""
        logger.info("[*] Parsing HTTP headers and HTML metadata...")
        try:
            resp = requests.get(self.url, headers=self._get_headers(), timeout=self.timeout)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            self.data["http_technical"] = {
                "server": resp.headers.get("Server"),
                "powered_by": resp.headers.get("X-Powered-By"),
                "title": soup.title.string if soup.title else "N/A",
                "social_links": list(set([a['href'] for a in soup.find_all('a', href=True) 
                                if any(s in a['href'] for s in ['fb.com', 'twitter.com', 'linkedin.com', 'instagram.com'])]))
            }
        except Exception as e:
            logger.error(f"Metadata parsing failed: {e}")

    def store_results(self):
        """Saves or appends results to reports/results.json."""
        os.makedirs("reports", exist_ok=True)
        
        current_logs = []
        if os.path.exists(self.report_path):
            with open(self.report_path, "r") as f:
                try:
                    current_logs = json.load(f)
                    if not isinstance(current_logs, list): current_logs = [current_logs]
                except: pass
        
        current_logs.append(self.data)
        
        with open(self.report_path, "w") as f:
            json.dump(current_logs, f, indent=4)
        logger.info(f"[✔] Scan for {self.target} finalized in {self.report_path}")

if __name__ == "__main__":
    target_site = input("Enter website for ReconWeb analysis: ").strip()
    if target_site:
        scanner = ReconWeb(target_site)
        scanner.get_builtwith_data()
        scanner.get_network_details()
        scanner.get_domain_registration()
        scanner.get_http_metadata()
        scanner.store_results()