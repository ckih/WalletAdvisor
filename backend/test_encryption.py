import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.config import encryption_service

def test_encryption():
    test_data = "100000"
    encrypted = encryption_service.encrypt(test_data)
    print(f"Encrypted: {encrypted}")
    decrypted = encryption_service.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
    assert test_data == decrypted
    print("Encryption test passed!")

if __name__ == "__main__":
    test_encryption()
