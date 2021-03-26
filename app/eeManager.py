import json
import base64
import time
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.fernet import Fernet


def encode_base64(data):
    """
    Encodes into base64.

    :param dict data:
    :return: encoded base64 string.
    """
    to_string = json.dumps(data)
    to_bytes = str.encode(to_string)
    encoded = base64.b64encode(to_bytes)

    return encoded.decode()


def decode_base64(data):
    """
    decodes from base64.

    :param  string data:
    :return: dict object.
    """
    to_bytes = base64.b64decode(data)

    return json.loads(to_bytes)


def return_timestamp():
    """
    Gets and returns the current local time.

    :return string timestamp: Current local time in format %Y-%m-%d %H:%M:%S %Z.
    """
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S %Z')

    return timestamp


#####################################
#   ENCRYPTION/DECRYPTION SECTION   #
#####################################


class Encryptor:
    """
    Encryptor Class desc.
    """

    def __init__(self, data_to_encrypt, asym_pub_key):
        """
        Constructor.
        """
        self.data_to_encrypt = data_to_encrypt
        self.asym_pub_key = asym_pub_key

        self.sym_key = self.generate_sym_key()
        self.fernet = Fernet(self.sym_key)

        # data to send customer, encrypted with self.sym_key
        self.encrypted_data = self.symmetrical_encryption()
        # key to send customer, encrypted with self.asym_pub_key
        self.encrypted_sym_key = self.asymmetrical_encryption()

    def generate_sym_key(self):
        """
        Generates a symmetrical key and returns it.
        """
        _sym_key = Fernet.generate_key()
        return _sym_key

    def symmetrical_encryption(self):
        """
        Desc
        """
        sym_encrypted_data = self.fernet.encrypt(self.data_to_encrypt)

        return sym_encrypted_data

    def asymmetrical_encryption(self):
        """
        Desc
        """
        # public_key = serialization.load_pem_public_key(self.asym_pub_key, backend=default_backend())

        encrypted_key = self.asym_pub_key.encrypt(
            self.sym_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))

        return encrypted_key

    def return_key_and_data(self):
        key = self.encrypted_sym_key
        data = self.encrypted_data

        return key, data


class Decryptor:
    """
    Decryptor Class desc.
    """

    def __init__(self, data_to_decrypt, encrypted_sym_key, asym_private_key):
        """
        Constructor.
        """
        self.data_to_decrypt = data_to_decrypt
        self.encrypted_sym_key = encrypted_sym_key
        self.asym_private_key = asym_private_key

        self.decrypted_sym_key = self.asymmetrical_decryption()
        self.fernet = Fernet(self.decrypted_sym_key)
        self.decrypted_data = self.symmetrical_decryption()

    def asymmetrical_decryption(self):
        decrypted_data = self.asym_private_key.decrypt(
            self.encrypted_sym_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))

        return decrypted_data

    def symmetrical_decryption(self):
        """
        Decrypts an encrypted message
        """
        return self.fernet.decrypt(self.data_to_decrypt)

    def return_key_and_data(self):
        key = self.decrypted_sym_key
        data = self.decrypted_data

        return key, data


def encode_base64_key_and_data(key, data):
    """
    Desc
    """
    # CONVERT key AND data FROM BYTES -> STRING
    key_bytes_to_string = key.decode('latin1')
    data_bytes_to_string = data.decode()

    # CREATE DICT OBJECT
    data_to_dict = {
        'key': key_bytes_to_string,
        'data': data_bytes_to_string
    }

    # ENCODE data_to_dict INTO BASE64
    encoded_data = encode_base64(data_to_dict)

    return encoded_data


def decode_base64_key_and_data(base64_string):
    """
    Desc
    """
    data = decode_base64(base64_string)

    key_to_bytes = data['key'].encode('latin1')
    data_to_bytes = data['data'].encode()

    return key_to_bytes, data_to_bytes


def load_public_key(path):
    with open(path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend())
        return public_key


def load_private_key(path):
    with open(path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend())
        return private_key


def generate_private_public_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    return private_key, public_key


def write_keys_to_file(path, private_key_name, public_key_name):
    private, public = generate_private_public_keys()

    private_pem = private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    new_dir = os.path.join(parent_dir, "secrets")
    private_key_path = os.path.join(new_dir, private_key_name)
    public_key_path = os.path.join(new_dir, public_key_name)

    with open(private_key_path, 'wb') as f:
        f.write(private_pem)

    with open(public_key_path, 'wb') as f:
        f.write(public_pem)
