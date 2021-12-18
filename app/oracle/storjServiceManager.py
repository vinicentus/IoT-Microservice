import sqlite3
import os

from . import dbManager
from . import eeManager

from datetime import datetime, timedelta, timezone

from uplink_python.errors import StorjException, BucketNotEmptyError, BucketNotFoundError
from uplink_python.module_classes import ListObjectsOptions, Permission, SharePrefix, UploadOptions
from uplink_python.uplink import Uplink


MY_BUCKET = "iot-microservice"
MY_STORJ_UPLOAD_PATH = "temp.db"

# Source and destination path and file name for testing
path = os.path.dirname(os.path.abspath(__file__))
SRC_FULL_FILENAME = os.path.join(path, 'temp.db')

# public_key is currently not used, but could be used for encrypting the return value for the task contract (currently none)
# Note that public_key has nothing to do with the data uploaded to storj


def execute_storj(possibly_encrypted_access: str, is_encrypted: bool, public_key: str = None):
    print(SRC_FULL_FILENAME)

    # Safely create a copy of our database
    dbManager.create_temp_db_copy(SRC_FULL_FILENAME)

    uplink = Uplink()

    if is_encrypted:
        # TODO
        print('uses encryption')
        access = uplink.parse_access(possibly_encrypted_access)
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
    upload.commit()
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
