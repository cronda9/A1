from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
import textwrap
import argparse

DATABASE_URL = "SOMETHING"

def main():

    parser = argparse.ArgumentParser(description='Register application: show overviews of classes', allow_abbrev=False)

    parser.add_argument('-d', type = str, help = 'show only those classes whose department contains dept', action = 'store', dest='dept')
    parser.add_argument('-n', type = str, help = 'show only those classes whose course number contains num', action = 'store', dest='num')
    parser.add_argument('-a', type = str, help = 'show only those classes whose distrib area contains area', action = 'store', dest='area')
    parser.add_argument('-t', type = str, help = 'show only those classes whose course title contains title', action = 'store', dest='title')

    args = parser.parse_args()
    print(args + " ")

    dept = args.dept
    area = args.area
    num = args.num
    title = args.title

    try:
        with connect(DATABASE_URL, isolation_level=None, uri=True) as connection:

            with closing(connection.cursor()) as cursor:
                used = False
                arg = []
                stmt_str = "SELECT classid, dept, coursenum, area, title "
                stmt_str += "FROM classes, crosslistings, courses "

                if dept:
                    arg.append('%' + dept.lower() + '%')
                    if used:
                        stmt_str += "AND crosslistings.dept.lower() = ? "
                    else:
                        stmt_str += "WHERE crosslistings.dept.lower() = ? "
                        used = True
                if area:
                    arg.append('%' + area.lower() + '%')
                    if used:
                        stmt_str += "AND courses.area.lower() = ? "
                    else:
                        stmt_str += "WHERE courses.area.lower() = ? "
                        used = True
                if title:
                    arg.append('%' + title.lower() + '%')
                    if used:
                        stmt_str += "AND courses.title.lower() like ? "
                    else:
                        stmt_str += "WHERE courses.title.lower() = ? "
                        used = True
                if num:
                    arg.append('%' + num.lower() + '%')
                    if used:
                        stmt_str += "AND crosslistings.coursenum.lower() = ? "
                    else:
                        stmt_str += "WHERE crosslistings.coursenum.lower() = ? "
                        used = True

                stmt_str += "ORDER BY dept, coursenum, classid"
                print("STATE",stmt_str)
                print("ARGS",arg)


    except Exception as ex:
        print(ex, file=stderr)
        exit(1)


main()
