# Most of this file was recklessly copied from https://github.com/storj-thirdparty/uplink-python/blob/master/uplink_python/hello_storj.py
# TODO: reqrite this file from sratch

import sqlite3

from datetime import datetime

from uplink_python.errors import StorjException, BucketNotEmptyError, BucketNotFoundError
from uplink_python.module_classes import ListObjectsOptions, Permission, SharePrefix
from uplink_python.uplink import Uplink
from storj_test_constants import MY_API_KEY, MY_SATELLITE, MY_ENCRYPTION_PASSPHRASE

if __name__ == "__main__":

    MY_BUCKET = "iot-microservice"
    MY_STORJ_UPLOAD_PATH = "temp.db"

    # Source and destination path and file name for testing
    SRC_FULL_FILENAME = "./app/oracle/temp.db"

    # -------------------------------------------------------------------
    # Backup the current db the right way, respecting db lock status
    connection = sqlite3.connect('./app/oracle/sensor_data.db')
    backup = sqlite3.connect(SRC_FULL_FILENAME)
    with backup:
        connection.backup(backup)
    backup.close()
    connection.close()
    # -------------------------------------------------------------------

    # try-except block to catch any storj exception
    try:
        # create an object of Uplink class
        uplink = Uplink()

        # function calls
        # request access using passphrase
        print("\nRequesting Access using passphrase...")
        access = uplink.request_access_with_passphrase(MY_SATELLITE, MY_API_KEY,
                                                       MY_ENCRYPTION_PASSPHRASE)
        print("Request Access: SUCCESS!")
        #

        # open Storj project
        print("\nOpening the Storj project, corresponding to the parsed Access...")
        project = access.open_project()
        print("Desired Storj project: OPENED!")
        #

        # enlist all the buckets in given Storj project
        print("\nListing bucket's names and creation time...")
        bucket_list = project.list_buckets()
        for bucket in bucket_list:
            # as python class object
            print(bucket.name, " | ", datetime.fromtimestamp(bucket.created))
            # as python dictionary
            print(bucket.get_dict())
        print("Buckets listing: COMPLETE!")
        #

        # as an example of 'put' , lets read and upload a local file
        # upload file/object
        print("\nUploading data...")
        # get handle of file to be uploaded
        file_handle = open(SRC_FULL_FILENAME, 'r+b')
        # get upload handle to specified bucket and upload file path
        upload = project.upload_object(MY_BUCKET, MY_STORJ_UPLOAD_PATH)
        #
        # upload file on storj
        upload.write_file(file_handle)
        #
        # commit the upload
        upload.commit()
        # close file handle
        file_handle.close()
        print("Upload: COMPLETE!")
        #

        # list objects in given bucket with above options or None
        print("\nListing object's names...")
        objects_list = project.list_objects(MY_BUCKET, ListObjectsOptions(recursive=True,
                                                                          system=True))
        # print all objects path
        for obj in objects_list:
            print(obj.key, " | ", obj.is_prefix)  # as python class object
            print(obj.get_dict())  # as python dictionary
        print("Objects listing: COMPLETE!")
        #

        #
        # close given project with shared Access
        print("\nClosing Storj project...")
        project.close()
        print("Project CLOSED!")
        #
    except StorjException as exception:
        print("Exception Caught: ", exception.details)
