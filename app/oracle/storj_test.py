# Most of this file was recklessly originally copied from https://github.com/storj-thirdparty/uplink-python/blob/master/uplink_python/hello_storj.py
# TODO: rewrite this file from sratch

import sqlite3
import os

from . import dbManager
from . import eeManager

from datetime import datetime

from uplink_python.errors import StorjException, BucketNotEmptyError, BucketNotFoundError
from uplink_python.module_classes import ListObjectsOptions, Permission, SharePrefix
from uplink_python.uplink import Uplink
from .storj_test_constants import MY_API_KEY, MY_SATELLITE, MY_ENCRYPTION_PASSPHRASE


MY_BUCKET = "iot-microservice"
MY_STORJ_UPLOAD_PATH = "temp.db"

# Source and destination path and file name for testing
path = os.path.dirname(os.path.abspath(__file__))
SRC_FULL_FILENAME = os.path.join(path, 'temp.db')


def execute_storj():
    print(SRC_FULL_FILENAME)

    # Safely create a copy of our database
    dbManager.create_temp_db_copy(SRC_FULL_FILENAME)

    # Upload the database as a file to storj
    upload_to_storj()

    # complete the task after the data has been uploaded to storj
    data = "Successfully uploaded to storj"

    # # ENCRYPTION & ENCODING
    # if public_key is not None:
    #     bytes_data = bytes(str(data), 'utf-8')
    #     encryptor = eeManager.Encryptor(bytes_data, public_key)
    #     data = eeManager.encode_base64_key_and_data(
    #         *encryptor.return_key_and_data())
    # # ENCODING
    # else:
    #     data = eeManager.encode_base64(data)

    return data


def upload_to_storj():  # TODO: throw or return eceptions in thyis function, so we know if everything was uploaded succesfully
    # try-except block to catch any storj exception
    try:
        # create an object of Uplink class
        uplink = Uplink()

        # request access using passphrase
        print("\nRequesting Access using passphrase...")
        access = uplink.request_access_with_passphrase(MY_SATELLITE, MY_API_KEY,
                                                       MY_ENCRYPTION_PASSPHRASE)
        print("Request Access: SUCCESS!")

        # open Storj project
        print("\nOpening the Storj project, corresponding to the parsed Access...")
        project = access.open_project()
        print("Desired Storj project: OPENED!")

        # as an example of 'put' , lets read and upload a local file
        # upload file/object
        print("\nUploading data...")
        # get handle of file to be uploaded
        file_handle = open(SRC_FULL_FILENAME, 'r+b')
        # get upload handle to specified bucket and upload file path
        upload = project.upload_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)

        # upload file on storj
        upload.write_file(file_handle)

        # commit the upload
        upload.commit()
        # close file handle
        file_handle.close()
        print("Upload: COMPLETE!")

        # close given project with shared Access
        print("\nClosing Storj project...")
        project.close()
        print("Project CLOSED!")
    except StorjException as exception:
        print("Exception Caught: ", exception.details)


if __name__ == "__main__":
    # Backup the current db the right way, respecting db lock status
    dbManager.create_temp_db_copy(SRC_FULL_FILENAME)

    upload_to_storj()
