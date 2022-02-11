from multiprocessing.dummy import JoinableQueue
from socket import create_server
from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
import textwrap
import argparse
from tkinter.tix import Select
from turtle import title
from types import ClassMethodDescriptorType
from xml.etree.ElementTree import C14NWriterTarget

DATABASE_URL = "file:reg.sqlite?mode=ro"

def main():
    tags = []
    
    parser = argparse.ArgumentParser(description='Registrar application: show details about a class', allow_abbrev=False)

    parser.add_argument('classid', metavar='classid',type=int, help='the id of the class whose details should be shown')

    class_id = parser.parse_args().classid


    #courseid, days, starttime, endtime, bldg, roomnum, 
    #dept(s), coursenum(s), 
    #area, title, 
    #descrip, prereqs, and profname(s)

#    try:
 #       with connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
  #          with closing(connection.cursor()) as cursor:

                # if class_id does not exist in the dataset throw exception                
                check_courseid = "EXISTS (SELECT classes.courseid FROM classes"
                check_courseid += "WHERE classes.classid = ? ;"
                coursor.execute(check_courseid, [class_id])
                exists = cursor.fetchall()
                if not exists:
                    raise Exception("no class with classid ", class_id, " exists")

   #            select_courseid = "SELECT classes.courseid FROM classes "
 #              select_courseid += "WHERE classes.classid = ? ;"
#
#               cursor.execute(select_courseid, [class_id])
#               course_id = cursor.fetchone()[0]
#               print(course_id)
#

#                stmt =  "SELECT classes.courseid, classes.days, classes.starttime, classes.endtime, "
#                stmt +=         "classes.bldg, classes.roomnum, "
#                stmt +=         "crosslistings.dept, crosslistings.coursenum, " 
#                stmt +=         "courses.area, courses.title, courses.descrip, courses.prereqs "
#                stmt +=         "profs.profname "   
#                stmt += "FROM crosslistings, courses, classes, coursesprofs " 
#                stmt += "WHERE classes.courseid = '4017' "  
#                stmt += "AND courses.courseid = classes.courseid "
#                stmt += "AND crosslistings.courseid = classes.courseid "
#                stmt += "AND coursesprofs.courseid = classes.courseid "
#                stmt += "AND coursesprofs.profid = profs.profid "
#                stmt += "ORDER BY crosslistings.dept, crosslistings.coursenum, classes.classid;"
#
 #               SELECT classes.courseid, classes.days, classes.starttime, classes.endtime, 
 #                      classes.bldg, classes.roomnum,
 #                      crosslistings.dept, crosslistings.coursenum,
 #                      courses.area, courses.title, courses.descrip, courses.prereqs
 #               FROM classes, crosslistings, courses, coursesprofs, profs
  #              WHERE classes.courseid = (SELECT classes.courseid 
 #                                        FROM classes
 #                                        WHERE classes.classid = 9012) 
 #               AND courses.courseid = classes.courseid;
 #               AND crosslistings.courseid = classes.courseid;
 #               AND coursesprofs.courseid = classes.courseid
 #               AND profs.profid = (SELECT coursesprofs.profid
 #                                   FROM coursesprofs
 #                                   WHERE coursesprofs.courseid = 9012);

 #               print(stmt)

 #               run = False
 #               if run:
 #                  cursor.execute(stmt)
 #                   
 #                   row = cursor.fetchone()
 #                   print(row)

 #                   while row:
 #                       print('Course ID:', row[0], '\n')

 #                       print('Days:', row[1])
 #                       print('Start time:', row[2])
 #                       print('End time:', row[3])
 #                       print('Building:', row[4])
 #                       print('Room:', row[5], '\n')

#                        print('Dept and Number:', row[6], row[7], '\n')
#
#                        print('Area:', row[8], '\n')
#
#                        print('Title:', row[9], '\n')
#
#                        print('Description:', row[10], '\n')
#
#                        print('Prerequisites:', row[11], '\n')
#
#                        print('Professor:', row[12])
#
#                        row = cursor.fetchone()#



 #   except Exception as ex:
    #    print(ex, file=stderr)
    #    exit(1)

if __name__ == "__main__":
   main()

