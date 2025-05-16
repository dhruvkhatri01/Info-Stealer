# 🕵️‍♂️ Information Stealer Using Python (For Educational Purposes)

> ⚠️Disclaimer:-  This tool is developed **strictly for educational and ethical hacking training only**. Unauthorized use on any device or network without permission is **illegal**.

---

## 📌 Table of Contents
- [📚 About the Project](#-about-the-project)
- [🧰 Tools & Libraries Used](#-tools--libraries-used)
- [⚔️ Challenges Faced](#-challenges-faced)
- [⚙️ How It Works](#-how-it-works)
- [💡 Use Cases](#-use-cases)
- [📈 Advantages & Disadvantages](#-advantages--disadvantages)
- [🔮 Future Use & Relevance](#-future-use--relevance)
- [🚀 Getting Started](#-getting-started)
- [📜 License](#-license)

---

### 📚 About the Project

This project simulates a **basic information stealer** to demonstrate how attackers exploit local machine access to:
- Extract saved browser passwords from **Google Chrome**
- Capture sensitive content from the **clipboard**
- Collect **system and network information**

The purpose is to **educate students and cybersecurity professionals** on how attackers operate and how to defend against such threats.

---

### 🧰 Tools & Libraries Used

| Tool/Library      | Purpose |
|------------------|---------|
| `Python`         | Main language used for scripting |
| `pyperclip`      | Used to access clipboard data |
| `sqlite3`        | Interacts with Chrome's saved password database |
| `win32crypt`     | Decrypts DPAPI encrypted data (Windows only) |
| `pycryptodome`   | Handles AES decryption used by Chrome |
| `requests`       | Fetches public IP from online API |
| `platform`, `socket`, `uuid` | Used for gathering system details |
| `shutil`, `os`, `base64`     | File and data operations |

---

### ⚔️ Challenges Faced

1. **Chrome Password Decryption**
   - Chrome encrypts passwords with AES-GCM using keys protected by the Windows Data Protection API (DPAPI), requiring careful key extraction.
2. **Database Locking**
   - Chrome keeps the `Login Data` database locked while running, requiring temporary copies to be made.
3. **Cross-Platform Incompatibility**
   - Script currently works only on **Windows** due to `win32crypt` and Windows-specific paths.
4. **Silent Failures**
   - Some systems or browsers have security mechanisms that silently fail or block extraction.

---

### ⚙️ How It Works

1. **Extract Encryption Key**
   - Retrieves and decrypts the Chrome encryption key from the `Local State` file.
2. **Read Chrome Login Database**
   - Copies and opens the `Login Data` SQLite file to extract saved passwords.
3. **Decrypt Passwords**
   - Uses AES-GCM and system decryption methods to reveal saved credentials.
4. **Clipboard Sniffing**
   - Reads currently copied text from the clipboard (e.g., passwords, emails).
5. **System Reconnaissance**
   - Retrieves IP, hostname, MAC address, OS version, and processor info.

---

### 💡 Use Cases

#### ✅ Educational
- Hands-on practice for **ethical hacking** & **cyber forensics** students.
- Understanding browser security internals.

#### ✅ Training Simulations
- Simulate threat behavior in **cybersecurity awareness programs**.

#### ✅ Defensive Development
- Developers can test and improve **anti-data-theft countermeasures**.

---

### 📈 Advantages & Disadvantages

#### ✅ Advantages
- Teaches **real-world exploitation techniques**.
- Highlights **common attack vectors**.
- Small, portable, Python-based tool.

#### ❌ Disadvantages
- **Windows-only** (currently).
- Can be **misused** if in wrong hands.
- May be **blocked by antivirus** as a threat.

---

### 🔮 Future Use & Relevance

As long as:
- Browsers store passwords locally,
- Users copy sensitive info to clipboard,
- Devices expose metadata to apps,

this type of attack remains **relevant for both red team and blue team activities**.

#### 🔧 Potential Future Enhancements
- 🔐 Add keylogging module  
- 🌐 Exfiltrate data to remote servers  
- 📦 Package as an executable  
- 🖥️ GUI wrapper for demonstrations  
- 🔄 Real-time monitoring

---

### 🚀 Getting Started

#### 📦 Install Requirements

```bash
python -m venv venv # To Create Environment Variables.
venv\Scripts\Activate # To Activate It.
Python <file_name>.py # Run the Script.
```

---

###📁 Output Location

**Data will be saved in the output/ directory:**

- passwords.txt
- clipboard.txt
- system_info.txt

---

### ✅ Conclusion

This project serves as a practical demonstration of common data theft techniques, allowing learners to study the real-world tactics used by threat actors. While offensive in nature, the goal is **defensive education**. It equips future developers, analysts, and cybersecurity defenders to recognize and defend against such threats in both personal and professional environments.

Never deploy or test this script on machines or accounts you do not explicitly own or control.
