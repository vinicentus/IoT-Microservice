import sqlite3
import os
#import pandas as pd
from datetime import datetime, timezone


path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'sensor_data.db')


# TODO: make so that you can use "with create_temp_db_copy():" (or similar) to operate on the db copy while it exists, and then delete it
# Backup the current db the right way, respecting db lock status
def create_temp_db_copy(outputPath: str):
    # Don't overwrite the existing database!
    assert outputPath != db

    connection = sqlite3.connect(db)
    backup = sqlite3.connect(outputPath)
    with backup:
        connection.backup(backup)
    backup.close()
    connection.close()


def add_entry_svm30(event_datetime, co2, tvoc):
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")

    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS svm30_output (
                                       datetime timestamp,
                                       co2 REAL,
                                       tvoc REAL);'''

    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_create_table_query)

    sqlite_insert_with_param = """INSERT INTO 'svm30_output'
                          ('datetime', 'co2', 'tvoc') 
                          VALUES (?, ?, ?);"""

    data_tuple = (event_datetime, co2, tvoc)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqliteConnection.commit()
    cursor.close()


def add_entry_scd30(event_datetime, d1, d2, d3):
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")

    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS scd30_output (
                                       datetime timestamp,
                                       d1 REAL,
                                       d2 REAL,
                                       d3 REAL);'''

    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_create_table_query)

    sqlite_insert_with_param = """INSERT INTO 'scd30_output'
                          ('datetime', 'd1', 'd2', 'd3') 
                          VALUES (?, ?, ?, ?);"""

    data_tuple = (event_datetime, d1, d2, d3)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqliteConnection.commit()
    cursor.close()


def add_entry_scd41(event_datetime, d1, d2, d3):
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")

    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS scd41_output (
                                       datetime timestamp,
                                       d1 INTEGER,
                                       d2 REAL,
                                       d3 REAL);'''

    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_create_table_query)

    sqlite_insert_with_param = """INSERT INTO 'scd41_output'
                          ('datetime', 'd1', 'd2', 'd3') 
                          VALUES (?, ?, ?, ?);"""

    data_tuple = (event_datetime, d1, d2, d3)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqliteConnection.commit()
    cursor.close()


def add_entry_sps30(event_datetime, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10):
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")

    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS sps30_output (
                                       datetime timestamp,
                                       d1 REAL,
                                       d2 REAL,
                                       d3 REAL,
                                       d4 REAL,
                                       d5 REAL,
                                       d6 REAL,
                                       d7 REAL,
                                       d8 REAL,
                                       d9 REAL,
                                       d10 REAL);'''

    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_create_table_query)

    sqlite_insert_with_param = """INSERT INTO 'sps30_output'
                          ('datetime', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10') 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    data_tuple = (event_datetime, d1, d2,
                  d3, d4, d5, d6, d7, d8, d9, d10)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqliteConnection.commit()
    cursor.close()


def get_all_entries(tableName="sps30_output"):
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    sqlite_select_query = "SELECT * FROM {}".format(tableName)
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    sqliteConnection.commit()
    cursor.close()
    return records


# If no tz data is specified, or it it invalid,
# then this method assumes that is in local time.
def convertTimeStampToUTCString(datetime: datetime):
    # Used to convert a datetime object to the correct string format for passing to db.
    # Example: 2021-07-29T10:18:03Z
    # (it has to include leading zeroes, minutes and seconds, and an Z at the end)
    return datetime.astimezone(
        timezone.utc).isoformat(timespec="seconds").replace('+00:00', 'Z')


def get_entries_from_date(datetime: datetime, tableName="sps30_output"):
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    sqlite_select_query = "SELECT * FROM {} WHERE datetime= ?".format(
        tableName)
    timestampString = convertTimeStampToUTCString(datetime)
    cursor.execute(sqlite_select_query, (timestampString,))
    records = cursor.fetchall()

    sqliteConnection.commit()
    cursor.close()

    return records


def get_entries_datetime_range(start: datetime, stop: datetime, tableName="sps30_output"):
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    sqlite_select_query = "SELECT * FROM {} WHERE datetime >= ? AND datetime <= ?".format(
        tableName)
    startString = convertTimeStampToUTCString(start)
    stopString = convertTimeStampToUTCString(stop)
    cursor.execute(sqlite_select_query, (startString, stopString,))
    records = cursor.fetchall()

    sqliteConnection.commit()
    cursor.close()

    return records


if __name__ == "__main__":
    the_records = get_all_entries()
    for row in the_records:
        print(row)
    #pd.DataFrame(the_records).to_csv('big_data_sample.csv', index=False)
    exit()
