"""Network utilities."""
import socket


def has_internet_connection(timeout: int = 5) -> bool:
    try:
        socket.create_connection(("www.google.com", 80), timeout=timeout)
        return True
    except (socket.timeout, socket.error):
        return False
