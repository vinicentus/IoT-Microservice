#!/home/pi/IoT-Microservice/venv/bin/python3
import time
import ast
import argparse
from datetime import datetime, timedelta
from dateutil.parser import parse
#from dbManager import get_entries_date_range, get_entries_from_date
#from eeManager import Encryptor, load_public_key, encode_base64_key_and_data, encode_base64

import dbManager
import eeManager
# USED TO DEMO DECRYPTION
#from eeManager import Decryptor, load_private_key, decode_base64_key_and_data

the_key = eeManager.load_public_key(
    'secrets/public_key.pem')  # REMOVE BEFORE IMPLEMENTING
the_secret = eeManager.load_private_key(
    'secrets/private_key.pem')  # REMOVE BEFORE IMPLEMENTING
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


def execute(_start_time: datetime, _stop_time: datetime, public_key=None, tableName="sps30_output"):
    """
    Function that fetches data entries from database. If public_key is provided data is encrypted and then encoded.
    If no key is provided the data is only encoded.
    :param _start_time: start date (as a datetime object)
    :param _stop_time: stop date (as a datetime object)
    :param public_key:
    :return: encoded data.
    """

    # We don't use microseconds in the database, so we shouldn't need to use them here either
    today = datetime.now().replace(microsecond=0)

    # CHECK IF START DATE IS IN THE FUTURE
    if datetime_compare(_start_time, today) <= 0:
        start_time = today
    else:
        start_time = _start_time

    # CHECK IF STOP DATE IS IN THE FUTURE
    if datetime_compare(_stop_time, today) <= 0:
        stop_time = today
    else:
        stop_time = _stop_time

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
        bytes_data = bytes(str(data), 'utf-8')
        encryptor = eeManager.Encryptor(bytes_data, public_key)
        data = eeManager.encode_base64_key_and_data(
            *encryptor.return_key_and_data())

    # ENCODING
    else:
        data = eeManager.encode_base64(data)

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('start')
    parser.add_argument('stop')
    args = parser.parse_args()

    # try to parse any kind of datetime input
    runtime = execute(parse(args.start), parse(args.stop), the_key)
    print(runtime)

    sym_key, data = eeManager.decode_base64_key_and_data(runtime)
    decryptor = eeManager.Decryptor(data, sym_key, the_secret)
    x, y = decryptor.return_key_and_data()
    res = ast.literal_eval(y.decode('utf-8'))
    print(res)
