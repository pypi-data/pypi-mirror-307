# QRCode Generator

This package generates QR codes based on data from CSV or JSON files. You can encrypt the data before encoding it into the QR code.

## Installation

To install the package via pip:

    pip install qure

## Usage

```python

from qrcode_generator import QRGenerator

# Example data
student_data = {"name": "Alice", "age": 21, "grade": "A"}

# Generate QR code
generator = QRGenerator(student_data)
file_path = generator.generate()
print(f"QR Code generated at: {file_path}")

bash
Copy code

````
bash
pip install .