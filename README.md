# VerifyGo 🎟️
**A DIY Production-Grade UID Generation &amp; Live Validation Engine**

VerifyGo is a lightweight, customizable event management system designed to bypass the limitations of "freemium" registration tools. It bridges local server power with global accessibility using Python, Flask, and Ngrok tunneling, allowing you to run a professional-grade validation system from a single laptop.

## 🌟 Why VerifyGo?

Most free event management tools have strict caps on the number of attendees or charge a premium for multi-device scanning. **VerifyGo** moves past these limits by:

* **Decentralizing Scanning:** Staff/students/volunteers can use their own devices and mobile data from different locations.
* **Real-time Synchronization:** Every scan updates a central database instantly.
* **Zero Infrastructure Cost:** Runs entirely on your local machine and uses free-tier developer tools.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Web Framework:** Flask
* **Production Server:** Gunicorn (WSGI)
* **Tunneling:** Ngrok
* **Frontend:** HTML5 (Mobile-ready scanner UI)
* **Package Management:** Homebrew / Pip

---

## 🚀 Project Architecture

### 1. UID Generation & Distribution

The generation script processes your input database (CSV/Excel), assigns a unique cryptographic ID to each entry, and generates a corresponding QR code. It can be configured to automatically email these QR codes to attendees using SMTP(Simple Mail Transfer Protocol).

### 2. The Validation Engine

The backend is built with Flask and served via **Gunicorn** to handle concurrent requests. This ensures that if multiple members scan UIDs at the same time, the server handles them in parallel without crashing.

### 3. The Global Tunnel

By using **Ngrok**, the local Flask server is projected onto a public URL. This is the "secret path" that allows members at different entrances to communicate with your laptop without needing to be on the same Wi-Fi network.

### **4. Database Generation (The First Step)**

Before going live, you need to prepare your "database." The generation script takes your registration list and creates the unique IDs(UIDs) used for validation.

```bash
python3 generate.py

```
* **What it does:** Reads your `database.csv`, generates a unique hash for each registration/entry, and creates a QR code.
* **Automation:** If SMTP is configured, it will automatically email these QR codes to each attendee's email address in the database.

> [!IMPORTANT]
> The `generate.py` script is pre-configured to look for specific headers (`FirstName`, `Email`, and `USN`) in a file named `registrations.csv`. You are welcome to use this as a template, or you are just a few tweaks away from modifying the logic to match your own database structure!

---

## **How to Run VerifyGo**

To get the full system online, you'll need three terminal windows open (using the same environment).

### **Step 1: The Engine (Gunicorn)**

Start the production-grade server. This handles the actual logic and database checking.

```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 LiveValidate:Validator

```

### **Step 2: The Bridge ~ Ngrok**

Open the tunnel to the internet. This provides the URL that staff members will open on their phones.

```bash
ngrok http 8000

```
---
 **Prerequisite: The Bridge (Ngrok Setup)**

To make your local server accessible to the world, you need an Ngrok account.

1. Sign up for a free account at [ngrok.com](https://ngrok.com/).
2. Retrieve your **Authtoken** from the Ngrok dashboard.
3. Configure your local Ngrok by running:

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE

```
### **Why this is necessary for your users:**

* **Authentication:** Most people don't realize they need a token until the terminal throws an error. Adding the `add-authtoken` command saves them a lot of frustration.
* **Port Matching:** Since the Gunicorn command is set to port `8000`, The Ngrok command must also be `http 8000`. If they don't match, the "bridge" won't connect.

---

### **Step 3: The Scanner (Frontend)**

Share the **Ngrok URL** with your team. They can now open the scanner UI in their mobile browsers and begin validating attendees in real-time.

---

I’ve tested this system to ensure it handles all real-world scenarios, from duplicate scans to invalid entries.
A full visual walkthrough and ***"Proof of Work"*** (including scanner states and backend logs) can be found in the images folder of this repository.

---

## **📝 Disclaimer & License**

**VerifyGo** is an open-source tool created for students and event organizers.

* **Data Privacy:** As the host, you are responsible for the security of the `database.csv`. Ensure you follow local data protection guidelines.
* **Usage:** Feel free to fork this repo, customize the HTML/CSS, or improve the Python logic!

---

## **🤝 Support & Contribution**

If you have a university event coming up and want to implement **VerifyGo** but need help with the setup or custom logic, **I’m just a DM away!**

**Author:** Shreyas Lakshmikanth
**University:** FAU Erlangen-Nürnberg

---
