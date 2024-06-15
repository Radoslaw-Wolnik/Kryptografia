from RSA import RSA
import hashlib
import os


class podpis_RSA:
    def __int__(self, rsa):
        self.file_path = None
        assert type(rsa) == RSA, f"the rsa class passed to the class should be RSA type is {type(rsa)}"
        self.file_path = None
        self._rsa = rsa

    def set_rsa(self, rsa):
        self._rsa = rsa

    def set_file(self, file_path):
        # Check if file exists in the given filepath
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No file found at {file_path}")
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
        print(hashed_file)
        signed = self._rsa.sign(text=hashed_file)

        return signed

    def verify(self, signed, public_key):
        assert self.file_path is not None, "filepath should not be empty"
        # hash the file in file_path (previously set if diff file)
        with open(self.file_path, 'rb') as file:
            file_data = file.read()
            hashed_file = hashlib.md5(file_data).hexdigest()
        # decode using public key in RSA
        decoded_sign = self._rsa.verify(text=signed, public_key=public_key)

        return decoded_sign == hashed_file
