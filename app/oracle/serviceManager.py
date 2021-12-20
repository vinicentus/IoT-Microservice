import json
import time
import ast
import argparse
from datetime import datetime, timedelta, timezone
from cryptography.hazmat.primitives.asymmetric import rsa
from dateutil import parser
from . import dbManager
from . import eeManager


max_day_range = 60


# Returns the timedelta in seconds
def datetime_compare(timestamp1: datetime, timestamp2: datetime):
    """
    Support function for execute()
    :param date1: start date (as a datetime object)'
    :param date2: stop date (as a datetime object)'
    :return: difference between the two dates in seconds.
    """
    delta = timestamp2 - timestamp1
    # We use seconds since our database stores timestamp with second precision
    return delta.total_seconds()


def execute(_start_time: str, _stop_time: str, public_key: str = None, tableName: str = "sps30_output"):
    """
    Function that fetches data entries from database. If public_key is provided data is encrypted and then encoded.
    If no key is provided the data is only encoded.
    :param _start_time: start date formatted as an ISO-860 string
    :param _stop_time: stop date formatted as an ISO-860 string
    :param public_key: pem file (in string format) containing RSA public key
    :return: encoded data.
    """

    _converted_start_time = parser.isoparse(_start_time)
    _converted_stop_time = parser.isoparse(_stop_time)

    # We don't use microseconds in the database, so we shouldn't need to use them here either
    # This whole function uses UTC internally!
    today = datetime.now(tz=timezone.utc).replace(microsecond=0)

    # CHECK IF START DATE IS IN THE FUTURE
    if datetime_compare(_converted_start_time, today) <= 0:
        start_time = today
    else:
        start_time = _converted_start_time

    # CHECK IF STOP DATE IS IN THE FUTURE
    if datetime_compare(_converted_stop_time, today) <= 0:
        stop_time = today
    else:
        stop_time = _converted_stop_time

    # FETCH DATA FROM DB
    # CHECK IF START DATE IS BEFORE STOP DATE
    if datetime_compare(start_time, stop_time) <= 0:
        print('stop time was used', stop_time)
        data = dbManager.get_entries_from_date(stop_time, tableName)

    else:
        deltaSeconds = datetime_compare(start_time, stop_time)
        deltaDays = timedelta(seconds=deltaSeconds).days

        # CHECK IF RANGE IS OUTSIDE SCOPE
        if deltaDays > max_day_range:
            new_start_time = stop_time - timedelta(max_day_range)
            print('delta.days > max_day_range:', new_start_time, stop_time)
            data = dbManager.get_entries_datetime_range(
                new_start_time, stop_time, tableName)

        else:
            print('last alt', start_time, stop_time)
            data = dbManager.get_entries_datetime_range(
                start_time, stop_time, tableName)

    # ENCRYPTION & ENCODING
    if public_key is not None:
        # Encode data as json before encrypting
        to_json_string = json.dumps(data)
        bytes_data = bytes(str(to_json_string), 'utf-8')

        rsa_object = eeManager.serialize_public_key_bytes(public_key)

        encryptor = eeManager.Encryptor(bytes_data, rsa_object)

        data = eeManager.encode_base64_key_and_data(
            *encryptor.return_key_and_data())

    # ENCODING
    else:
        data = eeManager.encode_base64(data)

    return data


# This probably does not work, use encryption_test.py as a simple alternative
if __name__ == "__main__":
    from pathlib import Path
    this_dir = Path(__file__).parent
    the_key = eeManager.load_public_key(
        this_dir/'secrets/public_key.pem')  # REMOVE BEFORE IMPLEMENTING
    the_secret = eeManager.load_private_key(
        this_dir/'secrets/private_key.pem')  # REMOVE BEFORE IMPLEMENTING

    # parser = argparse.ArgumentParser()
    # parser.add_argument('start')
    # parser.add_argument('stop')
    # args = parser.parse_args()
    args = '2021-08-23T00:00:01Z', '2021-08-23T00:10:01Z'

    # We don't need to parse the input here,
    # instead we expect a correctly formatted ISO-8601 datetime string,
    # that will be parsed in the excecute function
    # runtime = execute(args.start, args.stop, the_key)
    runtime = execute(*args, the_key, 'scd41_output')
    print(runtime)

    sym_key, data = eeManager.decode_base64_key_and_data(runtime)
    decryptor = eeManager.Decryptor(data, sym_key, the_secret)
    x, y = decryptor.return_key_and_data()
    res = y.decode('utf-8')
    print(x)
    print(res)
