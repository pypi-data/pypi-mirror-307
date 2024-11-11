from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = get_random_bytes(16)
iv = get_random_bytes(16)

def aes_encrypt(plain_text):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
    return cipher_text

def aes_decrypt(cipher_text):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size).decode('utf-8')
    return plain_text

plain_text = input("Enter a text: ")
print("Original message:", plain_text)

cipher_text = aes_encrypt(plain_text)
print("Encrypted message:", cipher_text)

decrypted_text = aes_decrypt(cipher_text)
print("Decrypted message:", decrypted_text)
