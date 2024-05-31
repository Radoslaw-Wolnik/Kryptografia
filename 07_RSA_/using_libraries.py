import rsa
import base64

# Generate RSA keys
(public_key, private_key) = rsa.newkeys(2048)

# Message to be encrypted
message = 'Hello, RSA!'
message_bytes = message.encode('utf-8')

# Encrypt the message using the public key
ciphertext = rsa.encrypt(message_bytes, public_key)
print(ciphertext)
print([char for char in ciphertext])

# Encode the encrypted message in Base64
ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')
print(ciphertext_base64)