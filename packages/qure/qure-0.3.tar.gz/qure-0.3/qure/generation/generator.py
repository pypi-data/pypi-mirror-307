import json
import qrcode
from qure.encryption import encrypt_data
from qure.utils import resize_image
from PIL import Image, ImageDraw, ImageFont
import os

class QRGenerator:
    def __init__(self, data: dict):

        if data is None:
            raise ValueError("Data cannot be None")

        self.version = 1
        self.data = data
        self.error_correction = qrcode.constants.ERROR_CORRECT_L
        self.student_name = data.get('name', 'Unknown')

    def generate(self, qr_path: str = None) -> str:
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
            
            if not qr_path:
                if not os.path.exists("qrcodes"):
                    os.makedirs("qrcodes")
                qr_path = f"qrcodes/{self.student_name.replace(' ', '_')}_qrcode.png"
                
            img.save(qr_path)
            return qr_path
        
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None

    from PIL import Image, ImageDraw, ImageFont, ImageOps

    def create_student_card(self, school_logo: str, school_name: str, academic_year: str, experation_date: str, student_photo: str, cards_path: str = None) -> str:
        """
        Generates a student ID card with student details, school logo, QR code, and other details.

        Parameters:
            school_logo (str): Path to the school's logo.
            school_name (str): The name of the school.
            student_photo (str): Path to the student's photo.
            academic_year (str): Academic year information.
            cards_path (str): Optional path where the generated card will be saved.

        Returns:
            str: Path to the saved student ID card image.
        """
        qr_image_path = self.generate()

        with Image.open(qr_image_path) as qr_image:
            qr_image = qr_image.resize((90, 90), Image.LANCZOS)

            # Card dimensions and background
            card_width, card_height = 400, 233
            card = Image.new("RGB", (card_width, card_height))
            draw = ImageDraw.Draw(card)

            # Gradient background
            for y in range(card_height):
                color = (255 - int(y * 255 / card_height), 255 - int(y * 128 / card_height), 255)
                draw.line([(card_width, y), (0, y)], fill=color)

            # Load fonts
            try:
                font = ImageFont.truetype("arial.ttf", 11)
                header_font = ImageFont.truetype("arial.ttf", 18)
                footer_font = ImageFont.truetype("arial.ttf", 13)
            except IOError:
                font = ImageFont.load_default()
                header_font = font
                footer_font = font

            # Place school logo
            try:
                with Image.open(school_logo) as logo:
                    logo = logo.resize((40, 40), Image.LANCZOS)
                    card.paste(logo, (15, 15))
            except IOError:
                print("Logo not found; skipping logo placement.")

            # Header text (school name and academic year)
            draw.text((70, 15), school_name, fill="black", font=header_font)
            draw.text((70, 45), f"Academic Year: {academic_year}", fill="black", font=font)

            try:
                with Image.open(student_photo) as photo:
                    photo = photo.resize((100, 100), Image.LANCZOS)
                    card.paste(photo, (15, 80))
            except IOError:
                print("Student photo not found; skipping photo placement.")
                with Image.open(school_logo) as photo:
                    photo = photo.resize((100, 100), Image.LANCZOS)
                    card.paste(photo, (15, 80))

            text_x, text_y = 130, 80
            details = [
                f"Name: {self.data.get('name', 'Unknown')}",
                f"Age: {self.data.get('age', 'N/A')}",
                f"Email: {self.data.get('email', 'N/A')}",
                f"Expiry: {experation_date}"
            ]
            for line in details:
                draw.text((text_x, text_y), line, fill="black", font=font)
                text_y += 20

            qr_x = card_width - qr_image.width - 20
            qr_y = (card_height - qr_image.height) // 2
            card.paste(qr_image, (qr_x, qr_y))

            footer_text = "Contact: school@example.com | Phone: +250 793180141"
            footer_y = card_height - 30
            draw.text((30, footer_y), footer_text, fill="white", font=footer_font)

            if not cards_path:
                os.makedirs("cards", exist_ok=True)
                cards_path = f"cards/{self.data.get('name', 'Student').replace(' ', '_')}_student_card.png"

            # Save the card
            card.save(cards_path)
            return cards_path



    def encrypt_data(self, data: str) -> str:
        encrypted_data = encrypt_data(data)
        return encrypted_data


def load_json(file_path: str):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None


def generate_qrcodes(json_file: str):
    data = load_json(json_file)
    if data and "students" in data:
        for student in data["students"]:
            qr_generator = QRGenerator(student)
            qr_path = qr_generator.generate()  # QR code for each student
            print(f"QR Code generated for {students['name']} at: {qr_path}")
    else:
        print("Invalid or empty JSON file")

def generate_cards(json_file: str, school_logo: str, school_name: str, academic_year: str, experation_date: str):
    data = load_json(json_file)
    if data and "students" in data:
        for student in data["students"]:
            qr_generator = QRGenerator(student)
            card_path = qr_generator.create_student_card(school_logo, school_name, academic_year, experation_date, student_photo=student['photo'])
            print(f"Student Card generated for {student['name']} at: {card_path}")
        return card_path
    else:
        print("Invalid or empty JSON file")