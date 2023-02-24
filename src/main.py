import email
import imaplib
import os
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv.main import load_dotenv
from create_invoice import create_invoice
load_dotenv()
# establish connection with Gmail
server = os.getenv('IMAP_SERVER')
mail = imaplib.IMAP4_SSL(server)

# instantiate the username and the password
username = os.getenv('EMAIL_ACCOUNT')
password = os.getenv('EMAIL_PASSWORD')

# login into the gmail account
mail.login(username, password)

# Select the inbox you want to monitor
mail.select('inbox')

# Fetch the latest emails in the inbox
status, data = mail.search(None, 'ALL')
email_ids = data[0].split()

# Start an indefinite loop to listen for new incoming emails
while True:
    # Wait for new incoming email to arrive
    print('Waiting for new incoming email...')
    status, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()

    # Loop through the unread emails
    for email_id in email_ids:
        # Fetch the email message
        status, data = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])

        # Print the email information
        print('From:', msg['From'])
        print('Subject:', msg['Subject'])

        # Create a folder to store the attachments
        folder_name = 'attachments'
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        # Loop through the email parts to find attachments
        for part in msg.walk():
            # Check if the part is an attachment
            if part.get_content_disposition() is not None:
                # Get the attachment name
                filename = part.get_filename()

                # Write the attachment to a file
                if filename:
                    filepath = os.path.join(folder_name, "temp_invoice.pdf")
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print('Attachment saved to', filepath)

        # Mark the email as read
        mail.store(email_id, '+FLAGS', '\\Seen')

        # Prepare the email reply
        msg_reply = MIMEMultipart()
        msg_reply['From'] = username
        msg_reply['To'] = msg['From']
        msg_reply['Subject'] = 'Re: ' + msg['Subject']
        msg_reply.attach(MIMEText('Hello, \n\nPlease find the attached invoice.\n\nBest regards, \nInvoice Bucket'))
        create_invoice()
        # Attach the invoice to the email
        invoice_path = "invoice.pdf"
        with open(invoice_path, 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename='../invoice.pdf')
        msg_reply.attach(attachment)

        # Send the email reply
        smtp_server = smtplib.SMTP(os.getenv('SMTP_SERVER'), 587)
        smtp_server.starttls()
        smtp_server.login(username, password)
        smtp_server.sendmail(username, msg['From'], msg_reply.as_string())
        smtp_server.quit()

        print('Email reply sent with attachment:', invoice_path)

    # Wait for a certain period of time before checking for new incoming emails again
    mail.noop()
    time.sleep(1)
