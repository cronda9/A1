from multiprocessing.dummy import JoinableQueue
from socket import create_server
from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
import textwrap
import argparse
from time import perf_counter_ns
from tkinter.tix import Select
from turtle import title
from types import ClassMethodDescriptorType
from xml.etree.ElementTree import C14NWriterTarget

DATABASE_URL = "file:reg.sqlite?mode=rwc"

def main():
    tags = []
    
    parser = argparse.ArgumentParser(description='Register application: show overviews of classes', allow_abbrev=False)

    parser.add_argument('-d', type = str, help = 'show only those classes whose department contains dept', action = 'store', dest='c_id')

    class_id = parser.parse_args().c_id

    #courseid, days, starttime, endtime, bldg, roomnum, 
    # dept(s), coursenum(s), 
    # area, title, 
    # descrip, prereqs, and profname(s)

    try:
        with connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
            with closing(connection.cursor()) as cursor:

                stmt = "SELECT courseid, days, starttime, endtime, bldg, roomnum FROM classes where classes.classid = ? "
                class_info = cursor.execute(stmt, [class_id]).fetchall()

                if not class_info:
                    print("No Such Class")
                    exit(1)
                
                class_info = class_info[0]

                courseid = class_info[0]

                stmt = "SELECT area, title, descrip, prereqs FROM courses WHERE courses.courseid = ? "
                course_info = cursor.execute(stmt, [courseid]).fetchall()[0]

                stmt =  "SELECT dept, coursenum FROM crosslistings WHERE crosslistings.courseid = ? "
                stmt += "ORDER BY dept, coursenum"
                cross_info = cursor.execute(stmt, [courseid]).fetchall()

                stmt =  "SELECT profs.profname FROM profs, coursesprofs "
                stmt += "WHERE coursesprofs.courseid = ? "
                stmt += "AND profs.profid = coursesprofs.profid "
                stmt += "ORDER BY profs.profname "
                profs_info = cursor.execute(stmt, [courseid]).fetchall()

                print('Course ID:', class_info[0], '\n')
                print('Days:', class_info[1])
                print('Start time:', class_info[2])
                print('End time:', class_info[3])
                print('Building:', class_info[4])
                print('Room:', class_info[5], '\n')

                for row in cross_info:
                    print('Dept and Number:', row[0], row[1])

                print('\nArea:', course_info[0], '\n')

                text = 'Title: ' + course_info[1]
                print(textwrap.fill(text, initial_indent='', break_long_words=False, width=72))
                print()

                text = 'Description: ' + course_info[2]
                print(textwrap.fill(text, initial_indent='', break_long_words=False, width=72))
                print()

                text = 'Prerequisites: ' + course_info[3]
                print(textwrap.fill(text, initial_indent='', break_long_words=False, width=72))
                print()

                if profs_info:
                    for row in profs_info:
                        print('Professor:', row[0])







    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == "__main__":
    main()