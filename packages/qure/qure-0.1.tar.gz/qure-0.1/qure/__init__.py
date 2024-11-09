__version__ = "0.1.0"
__author__ = "HOZANA INEZA Fraterne Ely"

from .generation import QRGenerator
from .scanner import QRScanner
from .encryption import encrypt_data, decrypt_data

def create_qr(data: str, encrypt: bool = True) -> str:
    if encrypt:
        data = encrypt_data(data)
    generator = QRGenerator()
    return generator.generate(data)

def scan_qr(image_path: str, decrypt: bool = True) -> str:
    scanner = QRScanner()
    data = scanner.scan(image_path)
    if decrypt:
        data = decrypt_data(data)
    return data
