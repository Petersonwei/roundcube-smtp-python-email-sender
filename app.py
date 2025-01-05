import os
import csv
import time
import smtplib
import imaplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def is_valid_email(email):
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def read_recipients():
    """Read recipients from CSV file"""
    recipients_list = []
    try:
        with open('recipients.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                to_email = row['to_email'].strip()
                # Skip if TO email is invalid
                if not is_valid_email(to_email):
                    print(f"Skipping invalid TO email: {to_email}")
                    continue
                    
                # Split CC emails by semicolon and validate each
                cc_emails = []
                if row['cc_emails']:
                    cc_emails = [email.strip() for email in row['cc_emails'].split(';')]
                    cc_emails = [email for email in cc_emails if is_valid_email(email)]
                    
                recipients_list.append({
                    'to': to_email,
                    'cc': cc_emails,
                    'company_name': row.get('company_name', '').strip()
                })
    except Exception as e:
        print(f"Error reading recipients: {str(e)}")
        return []
    return recipients_list

def read_html_template():
    """Read the HTML template file"""
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading HTML template: {str(e)}")
        return None

def save_to_sent_folder(message_string):
    # IMAP configuration
    imap_server = os.environ.get('SMTP_SERVER')
    sender_email = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASSWORD')
    
    try:
        # Connect to IMAP server
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(sender_email, password)
        
        # Try different folder names
        try_folders = ['INBOX.Sent', 'Sent', 'INBOX/Sent']
        
        for folder_name in try_folders:
            try:
                # Select Sent folder
                imap.select(folder_name)
                # Add the message to Sent folder
                imap.append(folder_name, '\\Seen', None, message_string.encode('utf-8'))
                print(f"Successfully saved to {folder_name} folder")
                break
            except Exception as folder_error:
                print(f"Failed with folder {folder_name}: {str(folder_error)}")
                continue
                
        imap.logout()
        
    except Exception as e:
        print(f"Failed to save to sent folder: {str(e)}")

def send_email(subject):
    # Email configuration
    # TODO add 'webmail.yourdomain.com' to .env
    smtp_server = os.environ.get('SMTP_SERVER')
    # TODO add to .env, 465 is the default port for SSL 
    smtp_port = int(os.environ.get('SMTP_PORT', 465)) 
    sender_email = os.environ.get('EMAIL_USER')
    smtp_password = os.environ.get('EMAIL_PASSWORD')
    
    if not sender_email or not smtp_password:
        print("Error: Environment variables not set!")
        return

    # Get HTML content
    html_content = read_html_template()
    if not html_content:
        return

    # Get all recipient groups
    recipient_groups = read_recipients()
    if not recipient_groups:
        print("Error: No recipients found!")
        return
        
    sender_name = os.environ.get('SENDER_NAME')
    if not sender_name:
        raise ValueError("SENDER_NAME environment variable is not set")
        
    for recipient in recipient_groups:
        try:
            # Create message for each recipient
            message = MIMEMultipart('alternative')
            message['From'] = f"{sender_name} <{sender_email}>"
            message['To'] = recipient['to']
            message['Cc'] = ', '.join(recipient['cc'])
            
            # Personalize subject with company name if available
            company_name = recipient.get('company_name', '').strip()
            personalized_subject = subject
            if company_name:
                personalized_subject = f"{company_name} - {subject}"
            message['Subject'] = personalized_subject
            
            # Personalize the HTML content
            personalized_html = html_content
            greeting = "Dear Team" if not company_name else f"Dear {company_name} Team"
            
            # Replace both instances of the greeting in the HTML
            personalized_html = personalized_html.replace('Greetings,', f'{greeting},')
            personalized_html = personalized_html.replace('<p style="font-size: clamp(14px, 3vw, 16px);">Greetings</p>', 
                                                        f'<p style="font-size: clamp(14px, 3vw, 16px);">{greeting}</p>')
            
            # Add HTML and plain text content
            text_part = MIMEText("Please view this email in an HTML-capable email client.", 'plain')
            html_part = MIMEText(personalized_html, 'html')
            
            message.attach(text_part)
            message.attach(html_part)
            
            # Convert message to string for IMAP
            message_string = message.as_string()
            
            # Send email
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.set_debuglevel(1)
                server.login(sender_email, smtp_password)
                all_recipients = [recipient['to']] + recipient['cc']
                server.send_message(message)
            
            # Save to sent folder via IMAP
            save_to_sent_folder(message_string)
            
            print(f"\nEmail sent successfully to:")
            print(f"TO: {recipient['to']}")
            print(f"CC: {', '.join(recipient['cc'])}")
            
            # Wait a minutes between sends
            time.sleep(90)
            
        except Exception as e:
            print(f"\nError sending to {recipient['to']}: {str(e)}")
            if isinstance(e, smtplib.SMTPAuthenticationError):
                print("\nAuthentication failed!")
                print(f"Attempted login with: {sender_email}")
            continue

if __name__ == "__main__":
    subject = os.environ.get('EMAIL_SUBJECT')
    if not subject:
        raise ValueError("EMAIL_SUBJECT environment variable is not set")
    send_email(subject)
