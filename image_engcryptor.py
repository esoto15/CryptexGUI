import os
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from cryptography.fernet import Fernet
from PIL import Image
import sys


class ImageEncryptor(QWidget):
    def __init__(self):
        super().__init__()
        self.image_label = QLabel(self)
        self.encrypt_button = QPushButton("Encrypt", self)
        self.cipher_suite = None  # Define as an instance variable

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Encryptor")
        self.setGeometry(100, 100, 400, 200)

        self.encrypt_button.clicked.connect(self.encrypt_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.encrypt_button)

        self.setLayout(layout)

    def encrypt_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)")
        if image_path:
            key = Fernet.generate_key()
            self.cipher_suite = Fernet(key)

            with open(image_path, "rb") as file:
                image_data = file.read()

            encrypted_data = self.cipher_suite.encrypt(image_data)

            encrypted_image_path = image_path + ".enc"
            with open(encrypted_image_path, "wb") as file:
                file.write(encrypted_data)

            self.display_image(encrypted_image_path)

    def display_image(self, image_path):
        # Create a temporary file path for the decrypted image
        temp_image_path = os.path.join(tempfile.gettempdir(), "decrypted_image.png")

        # Decrypt the image and save it to the temporary file
        with open(image_path, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = self.cipher_suite.decrypt(encrypted_data)  # Access the instance variable
        with open(temp_image_path, "wb") as file:
            file.write(decrypted_data)

        # Display the decrypted image using QPixmap
        pixmap = QPixmap(temp_image_path)
        self.image_label.setPixmap(pixmap.scaled(300, 300))
        self.image_label.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEncryptor()
    window.show()
    sys.exit(app.exec_())
