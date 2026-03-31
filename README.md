# ReconWeb 🚀

**ReconWeb** is a high-performance web intelligence and technical reconnaissance engine designed specifically for Linux environments. It specializes in extracting deep technical metadata, tech stacks, and network information while operating through **ProxyChains4** and **Tor** for enhanced privacy and anonymity.

---

## 🎯 Project Goal
The goal of ReconWeb is to provide a unified, automated interface for gathering comprehensive intelligence on web targets. It bridges the gap between simple web scraping and complex penetration testing reconnaissance by consolidating technology audits, WHOIS data, and network intel into a single, structured JSON report.

## ✨ Key Features
* **Privacy-First Design:** Fully compatible with `proxychains4` to route all traffic through the Tor network.
* **Tech Stack Identification:** Deep integration with the **BuiltWith API** to identify CMS, frameworks, and specific app versions.
* **Network Intelligence:** Automatic DNS record resolution (A, MX, NS, TXT) and IP Geolocation through Tor circuits.
* **Domain Forensics:** Extracts registration, update, and expiry timestamps using the WHOIS protocol.
* **HTTP Technical Metadata:** Captures server-side headers (`Server`, `X-Powered-By`) and social media footprints.
* **Persistent Storage:** Automatically appends all scan results to a centralized `reports/results.json` database.

---

## ⚙️ Installation & Setup (Debian/Ubuntu)

To ensure high reliability (8-9/10 health score), follow these steps to synchronize your system and Python environments.

### 1. Install System Dependencies
ReconWeb requires specific system binaries to handle network protocols and proxying.
```bash
sudo apt update
sudo apt install -y tor proxychains4 whois python3-pip python3-venv
```
2. Service Configuration

Start the Tor service and ensure it is running on the default port (9050).
```Bash

sudo systemctl start tor
sudo systemctl enable tor
```
Note: Verify that /etc/proxychains4.conf is set to socks5 127.0.0.1 9050.

# Clone the repository
```Bash
git clone https://github.com/hiddendestroyer1945/recon_web.git
cd recon_web
```

# Create and activate virtual environment
```Bash
python3 -m venv venv
source venv/bin/activate
```
# Configuration (.env)
ReconWeb uses an environment file to securely handle your BuiltWith API key. 

1. Create a file named `.env` in the root directory:
```bash
touch .env
```

2. Open the file and add your BuiltWith API key:
```text
BUILTWITH_API_KEY=your_api_key_here  
```

# Install dependencies
```bash
pip install -r requirements.txt
```
🛠 Usage & Examples

Always execute the program through proxychains4 to ensure your real IP address is masked by the Tor network.
Execution
```Bash

proxychains4 python3 recon_web.py
```

Example Input/Output

When prompted, enter a domain:
Enter website for ReconWeb analysis: example.com

The program will generate/update the following file:
reports/results.json

📂 Use Case

    Security Auditing: Identifying outdated server versions and exposed technology stacks.

    Competitive Intelligence: Analyzing the third-party apps and infrastructure used by competitors.

    Bug Bounty Hunting: Quick reconnaissance of target domains to find entry points or misconfigured DNS records.

    Privacy Research: Performing lookups without revealing the researcher's origin IP.

⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

⚠️ Disclaimer

This tool is provided for educational and authorized security testing purposes only. The developers assume no liability and are not responsible for any misuse or damage caused by this program. Users are responsible for complying with all applicable laws and regulations. Always obtain proper authorization before testing systems you do not own.

👤 Author

Created by a professional Python programmer with expertise in Linux system administration and penetration testing.