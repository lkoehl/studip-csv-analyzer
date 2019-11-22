import csv
import matplotlib.pyplot as plt
import sqlite3
from sqlite3 import Error

DELIMITER = ";"
FILE = "list.csv"
ALL_STUDENTS_AUD = "all_students_aud.csv"
ALL_STUDENTS_CC = "all_students_cc.csv"
ALL_GROUPS_AUD = "all_groups_aud.csv"
ALL_GROUPS_CC = "all_groups_cc.csv"

students = []
all_students = {}

database = r"studip_students.db"


def connect_to(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established. Using sqlite3 version:", sqlite3.version)
    except Error as e:
        print("No connection to database possible", e)

    return conn


def execute_sql(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print("Execution of sql not possible", e)


conn = connect_to(database)

if conn is not None:
    # create projects table
    execute_sql(conn, """ CREATE TABLE IF NOT EXISTS all_students (
                                student_id integer PRIMARY KEY,
                                user_name text NOT NULL,
                                mat_nr bigint,
                                first_name text NOT NULL,
                                last_name text NOT NULL,
                                gender text NOT NULL,
                                login_date text NOT NULL
                            ); """)

    # create tasks table
    execute_sql(conn, """ CREATE TABLE IF NOT EXISTS groups (
                                groups_id integer PRIMARY KEY,
                                user_name text NOT NULL,
                                group_nr integer NOT NULL,
                                codingclass_nr integer NOT NULL
                            ); """)

    # create courses table
    execute_sql(conn, """ CREATE TABLE IF NOT EXISTS courses (
                                courses_id integer PRIMARY KEY,
                                user_name text NOT NULL,
                                first_area text NOT NULL,
                                first_degree text NOT NULL,
                                first_semester text NOT NULL,
                                second_area text,
                                second_degree text,
                                second_semester text
                            ); """)
else:
    print("Error! cannot create the database connection.")
