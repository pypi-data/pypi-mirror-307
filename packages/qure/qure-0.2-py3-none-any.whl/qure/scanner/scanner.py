from PIL import Image
from pyzbar.pyzbar import decode
import json
from qure.encryption import decrypt_data


class QRScanner:
    def __init__(self, key: str = None):
        """
        Initialize the scanner with an optional key for decryption.
        If no key is provided, it uses a default one (or generates one).
        """
        self.key = key

    def scan(self, image_path: str) -> dict:
        """
        Scan the QR code from the given image, decrypt the data, and return a JSON response.
        
        Parameters:
        - image_path: Path to the image containing the QR code.
        
        Returns:
        - JSON response containing the decrypted data.
        """
        # Open the image using Pillow
        img = Image.open(image_path)

        # Decode the QR code from the image
        decoded_objects = decode(img)

        # Check if QR code was found
        if decoded_objects:
            # Assuming the first decoded object is the correct one
            encrypted_data = decoded_objects[0].data.decode("utf-8")
            
            # Decrypt the data
            decrypted_data = self.decrypt_data(encrypted_data)
            
            # Return as a JSON response
            return self.create_json_response(decrypted_data)
        else:
            return self.create_json_response("No QR code found")

    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Decrypt the given encrypted data using the key.
        
        Parameters:
        - encrypted_data: Encrypted data as a string.
        
        Returns:
        - Decrypted original data as a string.
        """
        # Decrypt using the shared key
        if self.key:
            return decrypt_data(encrypted_data)
        return encrypted_data

    def create_json_response(self, data: str) -> dict:
        """
        Create a JSON response with the provided data.
        
        Parameters:
        - data: Data to be included in the JSON response.
        
        Returns:
        - JSON response (dict).
        """
        return json.loads(json.dumps({"status": "success", "data": data}))

