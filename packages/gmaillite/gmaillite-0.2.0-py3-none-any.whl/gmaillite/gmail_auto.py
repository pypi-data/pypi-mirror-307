import imaplib
import email
import itertools
import smtplib
import sys
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Spinner:
    def __init__(self, message=""):
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.message = message
        self.running = False
        self.spinner_thread = None

    def spin(self):
        while self.running:
            sys.stdout.write(f"\r{next(self.spinner)} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r')
        sys.stdout.flush()

    def start(self):
        self.running = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def stop(self):
        self.running = False
        if self.spinner_thread:
            self.spinner_thread.join()

class GmailAutomation:
    def __init__(self, response_func,email_address = 'ailite.llm@gmail.com', app_password = 'aufu lhuc zomv ndil'):
        self.email_address = email_address
        self.app_password = app_password
        self.imap_server = "imap.gmail.com"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.response_func = response_func
        # List of emails to ignore
        self.ignore_emails = [
            "noreply",
            "no-reply",
            "googlecommunityteam",
            "google-noreply",
            "googleplay-noreply"
        ]

    def should_process_email(self, sender):
        """Check if we should process this email"""
        return not any(ignore in sender.lower() for ignore in self.ignore_emails)

    def check_emails(self):
        """Check for new emails and process them"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email_address, self.app_password)
            mail.select('inbox')

            # Search for unread emails
            _, messages = mail.search(None, 'UNSEEN')

            for msg_num in messages[0].split():
                try:
                    _, msg = mail.fetch(msg_num, '(RFC822)')
                    email_body = msg[0][1]
                    email_message = email.message_from_bytes(email_body)

                    # Get sender
                    sender = email.utils.parseaddr(email_message['From'])[1]

                    # Only process non-system emails
                    if self.should_process_email(sender):
                        # Get subject and body
                        subject = email_message['Subject']

                        # Get body
                        body = ""
                        if email_message.is_multipart():
                            for part in email_message.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = email_message.get_payload(decode=True).decode()

                        # Process the email
                        response = self.response_func(subject,body)

                        # Send response
                        self.send_email_response(
                            sender,
                            f"Re: {subject}",
                            f"Thank you for your email!\n\nYou sent: {body}\n\nAutomatic response: {response}\n\nBest regards,\nEmail Bot"
                        )

                        logger.info(f"Processed email from {sender}")
                    else:
                        logger.debug(f"Skipping system email from {sender}")

                except Exception as e:
                    logger.error(f"Error processing individual email: {e}")

            mail.logout()
            return "Email check completed successfully"

        except Exception as e:
            logger.error(f"Error in check_emails: {e}")
            return f"Error: {str(e)}"

    def send_email_response(self, to_email, subject, message):
        """Send email response"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.app_password)
                server.send_message(msg)

            logger.info(f"Response sent to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    def start(self,sleep_time = 2):
        print("Email bot is running. Send a test email to ailite.llm@gmail.com ...")
        print('')
        spinner = Spinner("Checking for new emails...")

        # Run continuously
        try:
            spinner.start()
            while True:
                self.check_emails()
                time.sleep(sleep_time)  # Check every 30 seconds
        except KeyboardInterrupt:
            spinner.stop()
            print("\nBot stopped by user")
            sys.exit(0)


if __name__ == "__main__":
    def response_func(subject, body):
        # Simple AI response function
        response = 'dummy response'
        return response

    gmail = GmailAutomation(response_func)
    gmail.start()

