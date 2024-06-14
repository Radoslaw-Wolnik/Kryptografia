from RSA import RSA
import hashlib
import os

class podpis_RSA:

    def __int__(self, rsa):
        self.file_path = None
        assert type(rsa) == RSA, f"the rsa class passed to the class should be RSA type is {type(rsa)}"

        self._rsa = rsa

    def set_file(self, file_path):
        # Check if file exists in the given filepath
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"No file found at {self.file_path}")
        self.file_path = file_path

    def __str__(self):
        return f"ciphered using RSA\nfilepath: {self.file_path}"

    def sign(self):
        assert self.file_path is not None, "filepath should not be empty"
        # hash the file
        with open(self.file_path, 'rb') as file:
            file_data = file.read()
            hashed_file = hashlib.md5(file_data).hexdigest()
        # encode using private key in RSA
        signed = self._rsa.decode(text=hashed_file)

        return signed

    def verify(self, signed):
        assert self.file_path is not None, "filepath should not be empty"
        # hash the file in file_path (previously set if diff file)
        with open(self.file_path, 'rb') as file:
            file_data = file.read()
            hashed_file = hashlib.md5(file_data).hexdigest()
        # decode using public key in RSA
        decoded_sign = self._rsa.encode(text=signed)

        return decoded_sign == hashed_file
