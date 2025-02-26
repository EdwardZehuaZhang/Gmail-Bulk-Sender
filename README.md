# Gmail Bulk Sender

## 🔹 Overview
Automates **bulk email sending** via **Gmail API**, using OAuth 2.0 authentication. Loads recipients from a CSV file and sends emails with a PDF attachment.

## ⚡ Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/cde-email-sender.git
cd cde-email-sender
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Configure Environment Variables**
Create a `.env` file:
```ini
SENDER_EMAIL=cdeoweekmarketing@gmail.com
CLIENT_SECRET_FILE=credentials.json
```

### **4️⃣ Add Gmail API Credentials**
- Download **`credentials.json`** from Google Cloud Console.
- Place it in the project root.

### **5️⃣ Authenticate Gmail (Run Once)**
```sh
python auth.py
```

### **6️⃣ Send Emails**
**Test with first 2 recipients:**
```sh
python send_bulk_emails.py
```

**Send to all recipients:**
Update `send_all=False` to `send_all=True` in `send_bulk_emails.py` and run:
```sh
python send_bulk_emails.py
```

## 📂 File Structure
```
📁 cde-email-sender
│── auth.py                # OAuth authentication
│── send_bulk_emails.py    # Sends emails
│── .env                   # Stores email & credentials file path
│── requirements.txt       # Dependencies
│── email_body.txt         # Email content (HTML)
│── credentials.json       # Gmail API credentials
│── token.pickle           # OAuth token
│── Masterlist.csv         # Recipient emails
│── attachment.pdf         # PDF attachment
```
