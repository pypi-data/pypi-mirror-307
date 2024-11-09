import json
import qrcode
from qure.encryption import encrypt_data


class QRGenerator:
    def __init__(self, data: dict):
        self.version = 1
        self.data = data
        self.error_correction = qrcode.constants.ERROR_CORRECT_L
        self.student_name = data.get('name', 'Unknown')

    def generate(self, file_path: str = None) -> str:
        try:
            
            data = json.dumps(self.data)
            encrypted_data = self.encrypt_data(data)
            
            qr = qrcode.QRCode(
                version=self.version,
                error_correction=self.error_correction,
                box_size=10,
                border=4,
            )
            qr.add_data(encrypted_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill="black", back_color="white")
            
            # If no file path is specified, use the student's name as the file name
            if not file_path:
                file_path = f"qrcodes/{self.student_name.replace(' ', '_')}_qr.png"
                
            img.save(file_path)
            return file_path
        
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None

    def encrypt_data(self, data: str) -> str:
        encrypted_data = encrypt_data(data)
        return encrypted_data


# Function to load JSON data
def load_json(file_path: str):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None


# Function to generate multiple QR codes from a JSON file
def generate_multiple_qrcodes(json_file: str):
    data = load_json(json_file)
    if data and "students" in data:
        for student in data["students"]:
            qr_generator = QRGenerator(student)
            qr_path = qr_generator.generate()  # QR code for each student
            print(f"QR Code generated for {student['name']} at: {qr_path}")
    else:
        print("Invalid or empty JSON file")