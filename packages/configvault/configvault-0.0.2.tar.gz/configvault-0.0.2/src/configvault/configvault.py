#########################################################################################
#                                                                                       #
# MIT License                                                                           #
#                                                                                       #
# Copyright (c) 2024 Ioannis D. (devcoons)                                              #
#                                                                                       #
# Permission is hereby granted, free of charge, to any person obtaining a copy          #
# of this software and associated documentation files (the "Software"), to deal         #
# in the Software without restriction, including without limitation the rights          #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell             #
# copies of the Software, and to permit persons to whom the Software is                 #
# furnished to do so, subject to the following conditions:                              #
#                                                                                       #
# The above copyright notice and this permission notice shall be included in all        #
# copies or substantial portions of the Software.                                       #
#                                                                                       #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR            #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,              #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE           #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER                #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,         #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE         #
# SOFTWARE.                                                                             #
#                                                                                       #
#########################################################################################

#########################################################################################
# IMPORTS                                                                               #
#########################################################################################

import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken

#########################################################################################
# CLASS: ConfigVault                                                                    #
#########################################################################################

class ConfigVault:
    """ConfigVault provides secure, encrypted configuration storage for sensitive data."""
    
    # --------------------------------------------------------------------------------- #
    
    folder_path: str = None
    encryption_key: bytes = None
    cipher: Fernet = None

    # --------------------------------------------------------------------------------- #
    
    def __init__(self, folder_path: str, password: str, salt: bytes = b'some_fixed_salt'):
        """
        Initialize ConfigVault with the storage folder path and user password.

        Args:
            folder_path (str): Path to the folder for storing encrypted data.
            password (str): User-provided password for deriving the encryption key.
            salt (bytes): A fixed salt for key derivation. It should be securely stored or configured.
        """
        self.folder_path = folder_path
        self.encryption_key = self._derive_key(password, salt)
        self.cipher = Fernet(self.encryption_key)

        # Ensure storage folder exists
        os.makedirs(self.folder_path, exist_ok=True)

    # --------------------------------------------------------------------------------- #
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive a 32-byte encryption key from the user password.

        Args:
            password (str): User-provided password.
            salt (bytes): Salt for key derivation.

        Returns:
            bytes: A base64-encoded key suitable for Fernet encryption.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    # --------------------------------------------------------------------------------- #
    
    def store(self, key: str, data: dict, force: bool = False):
        """
        Store encrypted data under a specified key.

        Args:
            key (str): Unique identifier for the data.
            data (dict): Data to be stored, must be JSON serializable.
            force (bool): If True, overwrite existing data for the key; otherwise, raise an error.
        """
        file_path = os.path.join(self.folder_path, f"{key}.vault")
        
        if os.path.exists(file_path) and not force:
            raise FileExistsError(f"Data for key '{key}' already exists. Use force=True to overwrite.")

        encrypted_data = self.cipher.encrypt(json.dumps(data).encode())
        
        with open(file_path, "wb") as file:
            file.write(encrypted_data)

    # --------------------------------------------------------------------------------- #

    def retrieve(self, key: str):
        """
        Retrieve and decrypt data for a specified key.

        Args:
            key (str): Unique identifier for the data.

        Returns:
            dict: Decrypted data if available, else None.
        """
        file_path = os.path.join(self.folder_path, f"{key}.vault")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No entry found for key: {key}")

        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        try:
            decrypted_data = self.cipher.decrypt(encrypted_data).decode()
            return json.loads(decrypted_data)
        except InvalidToken:
            raise ValueError("Invalid encryption key provided.")

    # --------------------------------------------------------------------------------- #
    
    def list_keys(self):
        """
        List all keys available in the storage folder.

        Returns:
            list: List of all keys as strings.
        """
        return [
            filename.replace(".vault", "")
            for filename in os.listdir(self.folder_path)
            if filename.endswith(".vault")
        ]

    # --------------------------------------------------------------------------------- #

    def remove(self, key: str):
        """
        Remove a specific configuration by key.

        Args:
            key (str): Unique identifier for the data to be removed.
        """
        file_path = os.path.join(self.folder_path, f"{key}.vault")
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"No entry found for key: {key}")

    # --------------------------------------------------------------------------------- #
    
    def remove_all(self):
        """
        Clear all stored configurations in the storage folder.
        """
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".vault"):
                os.remove(os.path.join(self.folder_path, filename))

#########################################################################################
# EOF                                                                                   #
#########################################################################################