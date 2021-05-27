import sqlite3
import os
import pandas as pd


path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'sensor_data.db')


def add_entry(event_date, event_time, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10):
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")

    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS sensor_output (
                                       date timestamp,
                                       time timestamp,
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

    sqlite_insert_with_param = """INSERT INTO 'sensor_output'
                          ('date', 'time', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10') 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    data_tuple = (event_date, event_time, d1, d2,
                  d3, d4, d5, d6, d7, d8, d9, d10)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqliteConnection.commit()
    cursor.close()


def get_all_entries():
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    sqlite_select_query = """SELECT * FROM sensor_output"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    sqliteConnection.commit()
    cursor.close()
    return records


def get_entries_from_date(date):
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    sqlite_select_query = "SELECT * FROM sensor_output WHERE date= ?"
    cursor.execute(sqlite_select_query, (date,))
    records = cursor.fetchall()

    sqliteConnection.commit()
    cursor.close()

    return records


def get_entries_date_range(start, stop):
    sqliteConnection = sqlite3.connect(db)
    cursor = sqliteConnection.cursor()
    sqlite_select_query = "SELECT * FROM sensor_output WHERE date >= ? AND date <= ?"
    cursor.execute(sqlite_select_query, (start, stop,))
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
