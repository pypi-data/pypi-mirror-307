import rsa

from .giraffe_encryption.keys.read_key import get_existing_keys, get_public_key_string, encrypted_message_chunks_size

def decrypt(use_public_key: bool = False):
    _, private_key = get_existing_keys()

    if use_public_key:
        public_key = get_public_key_string()

    byte_number = encrypted_message_chunks_size(private_key.n)
    print(byte_number)
    with open("./test.grff", 'rb') as file:
        encrypted_message = file.read()

    encrypted_chunks = [encrypted_message[i:i+byte_number] for i in range(0, byte_number * (len(encrypted_message)//byte_number), byte_number)]
    decrypted_chunks = [rsa.decrypt(chunk, private_key) for chunk in encrypted_chunks]
    print(b"".join(decrypted_chunks))

if __name__ == "__main__":
    decrypt()