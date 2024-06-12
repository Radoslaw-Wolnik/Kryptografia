from RSA import RSA
import hashlib
import os

class podpis_RSA:
    # Example usage:
    # rsa_instance = RSA()  # assuming RSA class is defined elsewhere
    # signer = podpis_RSA(rsa_instance)
    # signer.set_file('path/to/file.txt')
    # signed_data = signer.sign()

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
        # check if file exsists in given filepath
        # hash the file
        with open(self.file_path, 'rb') as file:
            file_data = file.read()
            hashed_file = hashlib.md5(file_data).hexdigest()
        # encode using private key in RSA
        signed = self._rsa.decode(text=hashed_file)

        return signed
