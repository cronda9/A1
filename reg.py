from socket import create_server
from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
import textwrap
import argparse
from turtle import title
from xml.etree.ElementTree import C14NWriterTarget

DATABASE_URL = "file:reg.sqlite?mode=ro"

def main():
    tags = []
    
    parser = argparse.ArgumentParser(description='Register application: show overviews of classes', allow_abbrev=False)

    parser.add_argument('-d', type = str, help = 'show only those classes whose department contains dept', action = 'store', metavar='dept')
    parser.add_argument('-n', type = str, help = 'show only those classes whose course number contains num', action = 'store', metavar='num')
    parser.add_argument('-a', type = str, help = 'show only those classes whose distrib area contains area', action = 'store', metavar='area')
    parser.add_argument('-t', type = str, help = 'show only those classes whose course title contains title', action = 'store', metavar='title')


    dept = parser.parse_args().d
    num = parser.parse_args().n
    area = parser.parse_args().a
    title = parser.parse_args().t

    try:
        with connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
            with closing(connection.cursor()) as cursor:

                stmt =  "SELECT classes.classid, "
                stmt +=         "crosslistings.dept, " 
                stmt +=         "crosslistings.coursenum, "  
                stmt +=         "courses.area, " 
                stmt +=         "courses.title " 
                stmt += "FROM crosslistings, courses, classes "  
                stmt += "WHERE courses.courseid = crosslistings.courseid "  
                stmt += "AND classes.courseid = crosslistings.courseid "

                if dept:
                    tags.append("%" + dept.lower() + "%")
                    stmt += "AND lower(crosslistings.dept) like ? "

                if num:
                    tags.append("%" + num.lower() + "%")
                    stmt += "AND lower(crosslistings.coursenum) like ? "

                if area:
                    tags.append("%" + area.lower() + "%")
                    stmt += "AND lower(courses.area) like ? "

                if title:
                    tags.append("%" + title.lower() + "%")
                    stmt += "AND lower(courses.title) like ? "

                stmt += "ORDER BY crosslistings.dept, crosslistings.coursenum, classes.classid;"

                cursor.execute(stmt, tags)

                row = ["-----", "----", "------", "----", "----"]

                print("{0:5}  {1:4}  {2:6}  {3:4}  {4}".format("ClsId", "Dept", "CrsNum", "Area", "Title"))
                while row:
                    text = "{0:>5}  {1:>4}  {2:>6}  {3:>4}  {4}".format(row[0], row[1], row[2], row[3], row[4])
                    print(textwrap.fill(text, initial_indent='', subsequent_indent=' ' * 27, break_long_words=False, width=72,))
                    row = cursor.fetchone()                            
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == "__main__":
    main()



