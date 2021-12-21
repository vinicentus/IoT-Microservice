from pathlib import Path
import os

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from . import dbManager
from . import eeManager

from datetime import datetime, timedelta

from uplink_python.errors import StorjException
from uplink_python.module_classes import UploadOptions
from uplink_python.uplink import Uplink


MY_BUCKET = "iot-microservice"
MY_STORJ_UPLOAD_PATH = "temp.db"

# Source and destination path and file name for testing
path = os.path.dirname(os.path.abspath(__file__))
SRC_FULL_FILENAME = os.path.join(path, 'temp.db')


# If the access is encrypted, then it is really a base64 encoded json map with key and data params,
# that can be decoded with eeManager.decode_base64_key_and_data()
def execute_storj(possibly_encrypted_access: str, is_encrypted: bool):
    print(SRC_FULL_FILENAME)

    # Safely create a copy of our database
    dbManager.create_temp_db_copy(SRC_FULL_FILENAME)

    uplink = Uplink()

    if is_encrypted:
        print('uses encryption')

        # Load private RSA key to decrypt
        this_dir = Path(__file__).parent
        the_secret: RSAPrivateKey = eeManager.load_private_key(
            this_dir/'secrets/private_key.pem')
        # Load data and asymmetrically encrypted fernet key
        key_bytes, data_bytes = eeManager.decode_base64_key_and_data(
            possibly_encrypted_access)
        # Decrypt
        decryptor = eeManager.Decryptor(
            data_bytes, key_bytes, the_secret)
        decrypted_access = decryptor.decrypted_data

        access_string = decrypted_access.decode()

        access = uplink.parse_access(access_string)
    else:
        access = uplink.parse_access(possibly_encrypted_access)

    project = access.open_project()
    # There is no documentation for this function, but it uses Unix seconds since epoch
    # https://github.com/storj/uplink-c/blob/c94970889c5278b4124bb703ab3ef29fbe9a69d4/upload.go#L52
    # The timezone required seems to be local
    five_minutes_later = datetime.now() + timedelta(minutes=5)
    options = UploadOptions(expires=int(five_minutes_later.timestamp()))
    file_handle = open(SRC_FULL_FILENAME, 'r+b')
    upload = project.upload_object(
        MY_BUCKET, MY_STORJ_UPLOAD_PATH, options)
    upload.write_file(file_handle)

    try:
        upload.commit()
    except StorjException as error:
        # Localy print the error so we know what went wrong...
        print(error.code, error.message, error.details)
        raise

    file_handle.close()
    project.close()

    # # ENCRYPTION & ENCODING
    # if public_key is not None:
    #     bytes_data = bytes(str(data), 'utf-8')
    #     encryptor = eeManager.Encryptor(bytes_data, public_key)
    #     data = eeManager.encode_base64_key_and_data(
    #         *encryptor.return_key_and_data())
    # # ENCODING
    # else:
    #     data = eeManager.encode_base64(data)

    # A return value of type str is needed, because that will be the value used to complete the underlying task contract
    return 'Successfully uploaded data to storj!'


if __name__ == "__main__":
    execute_storj()
