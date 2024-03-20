import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
import threading

class BanBot:
    def __init__(self, banned_keywords):
        self.banned_keywords = banned_keywords
        self.logger = self.setup_logger()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', 12345))  # Change this to your desired IP and port
        self.server.listen(5)
        print("Ban bot is now running. Waiting for clients...")

    def setup_logger(self):
        logger = logging.getLogger('ban_bot_logger')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler('ban_log.txt')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def start(self):
        while True:
            client_socket, client_address = self.server.accept()
            print(f"Connection from {client_address} has been established.")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.check_message(message)
            except Exception as e:
                print(f"Error: {e}")
                break
        client_socket.close()

    def check_message(self, message):
        for keyword in self.banned_keywords:
            if keyword.lower() in message.lower():
                self.kick_user()
                self.logger.info(f"User banned for using banned keyword: {keyword}")
                self.send_email_alert(keyword)
                return

    def kick_user(self):
        print("User kicked from the chat! Reason: Violation of chat rules.")

    def send_email_alert(self, keyword):
        sender_email = "your_email@example.com"
        receiver_email = "spartancoding02@gmail.com"
        password = "your_email_password"
        
        subject = "Ban Alert - Violation of Chat Rules"
        body = f"User banned for using banned keyword: {keyword}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email alert sent successfully!")
        except Exception as e:
            print(f"Failed to send email alert: {e}")

if __name__ == "__main__":
    banned_keywords = ["spam", "scam", "inappropriate"]
    bot = BanBot(banned_keywords)
    bot.start()
