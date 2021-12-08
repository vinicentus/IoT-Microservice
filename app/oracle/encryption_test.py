import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
import eeManager


this_dir = Path(__file__).parent
the_key: RSAPublicKey = eeManager.load_public_key(
    this_dir/'secrets/public_key.pem')
the_secret: RSAPrivateKey = eeManager.load_private_key(
    this_dir/'secrets/private_key.pem')


string_data = 'Lorem ipsum'
bytes_data = bytes(string_data, 'utf-8')

encryptor = eeManager.Encryptor(bytes_data, the_key)

enc_sym_key, enc_data = encryptor.return_key_and_data()
print(base64.b64encode(enc_sym_key))
print(enc_data)

decryptor = eeManager.Decryptor(enc_data, enc_sym_key, the_secret)

key, data = decryptor.return_key_and_data()
print(key)
print(data)

encryptor.generate_sym_key()
encryptor.asymmetrical_encryption()
