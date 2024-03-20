import socket
import threading

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 12345))  # Connect to the server IP and port
        threading.Thread(target=self.receive_messages).start()
        self.send_messages()

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message:
                    print(message)
            except Exception as e:
                print(f"Error: {e}")
                break

    def send_messages(self):
        while True:
            message = input()
            self.client.sendall(message.encode())

if __name__ == "__main__":
    client = ChatClient()
