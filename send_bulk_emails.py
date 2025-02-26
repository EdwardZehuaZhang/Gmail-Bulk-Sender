import base64
import pickle
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")

def load_credentials():
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
        return creds
    return None

def read_email_body(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def send_email(recipient, subject, body_file, attachment_file):
    creds = load_credentials()
    if not creds:
        print("Authentication required. Run the authentication script first.")
        return

    service = build("gmail", "v1", credentials=creds)
    
    email_body = read_email_body(body_file)
    
    message = MIMEMultipart()
    message["To"] = recipient
    message["From"] = SENDER_EMAIL
    message["Subject"] = subject
    message.attach(MIMEText(email_body, "html", "utf-8"))

    with open(attachment_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_file)}")
        message.attach(part)
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    
    send_message = {"raw": raw_message}
    try:
        service.users().messages().send(userId="me", body=send_message).execute()
        print(f"✅ Email sent to {recipient}")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient}. Error: {e}")

def send_bulk_emails(csv_file, subject, body_file, attachment_file, send_all=False):
    df = pd.read_csv(csv_file)
    
    if not send_all:
        df = df.head(2)

    for _, row in df.iterrows():
        recipient_email = str(row["Email"]).strip()  
        
        if pd.notna(recipient_email) and recipient_email:
            emails = [email.strip() for email in recipient_email.split("/") if email.strip()]
            
            for email in emails:
                send_email(email, subject, body_file, attachment_file)

    print("📌 Bulk email sending complete.")

# ======================
# Default sending to first 2. To send all, just change send_all=False to True
# ======================
script_dir = os.path.dirname(os.path.abspath(__file__))  
csv_file_path = os.path.join(script_dir, "Masterlist for FOP 2025 - Round 1 OWEEK.csv")
body_file_path = os.path.join(script_dir, "email_body.txt")
attachment_file_path = os.path.join(script_dir, "cde_oweeek_marketing_deck_2025.pdf")

send_bulk_emails(
    csv_file_path, 
    "NUS CDE CLUB Partnership Invitation", 
    body_file_path, 
    attachment_file_path,
    send_all=False  
)
