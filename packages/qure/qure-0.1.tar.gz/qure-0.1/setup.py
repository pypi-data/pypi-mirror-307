from setuptools import setup, find_packages

setup(
    name="qure",
    version="0.1",
    author="HOZANA INEZA Fraterne Ely",
    author_email="fraterneelyh@gmail.com",
    description="A Python package to generate QR codes from JSON",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "qrcode[pil]",
        "PIL",
        "pyzbar",
        "qure",
        "cryptography"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
