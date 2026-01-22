import pandas as pd
import qrcode
import uuid
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# --- CONFIGURATION ---
input_file = 'registrations.csv'
output_db = 'master_event_db.csv'
qr_folder = 'qr_codes'

# EMAIL SETTINGS
SENDER_EMAIL = "PUT YOUR EMAIL HERE" # <--- PUT YOUR EMAIL HERE
APP_PASSWORD = "PUT YOUR APP PASSWORD HERE"  # <--- PUT YOUR APP PASSWORD HERE

if not os.path.exists(qr_folder):
    os.makedirs(qr_folder)

# Function to send email
def send_qr_email(to_email, name, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = "Registration Sucessfull"

        body = f"Hello {name},\n\nHere is your QR code for the event. Please show this at the entrance.\n\nRegards,\nEvent Team"
        msg.attach(MIMEText(body, 'plain'))

        # Attach QR Code
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(attachment_path)}",
        )
        msg.attach(part)

        # Login and Send
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f" > Email sent to {to_email}")
        return True
    except Exception as e:
        print(f" ! FAILED to send email to {to_email}: {e}")
        return False

# --- MAIN LOGIC ---
df = pd.read_csv(input_file)

# Add System Columns if they don't exist
if 'UniqueID' not in df.columns:
    df['UniqueID'] = [str(uuid.uuid4()) for _ in range(len(df))]
if 'CheckedIn' not in df.columns:
    df['CheckedIn'] = False 
if 'EmailSent' not in df.columns: # Track if email was sent so we don't spam on re-runs
    df['EmailSent'] = False

print(f"Found {len(df)} registrations. Processing...")

for index, row in df.iterrows():
    # skip if email already sent (useful if script crashes halfway)
    if row['EmailSent'] == True:
        continue

    uid = row['UniqueID']
    filename = f"{qr_folder}/{row['USN']}_{row['FirstName']}.png"
    
    # 1. Create QR
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(uid)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    
    # 2. Send Email
    print(f"Processing {row['FirstName']}...", end="")
    success = send_qr_email(row['Email'], row['FirstName'], filename)
    
    # 3. Update Status
    if success:
        df.at[index, 'EmailSent'] = True

# Save Database
df.to_csv(output_db, index=False)
print(f"\nDONE! Database saved to {output_db}")