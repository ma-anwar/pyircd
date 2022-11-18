"""Tiny client implementation for quick testing; can def be more robust"""
import socket

HOST = "127.0.0.1"
PORT = 6667

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, worldsadasdsadsa dsadsadas dsadasdasdsa\r\n")
    while data := s.recv(1024):
        print(f"Received {data}")
