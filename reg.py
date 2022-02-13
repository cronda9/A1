"""
reg.py
Authors: Christian Ronda and Gracyn Kuerner
"""
from sys import stderr, exit
from contextlib import closing
from sqlite3 import connect
import textwrap
import argparse

DATABASE_URL = "file:reg.sqlite?mode=ro"

def main():
    """Princeton Registar Class Search"""
    tags = []

    parser = argparse.ArgumentParser(description='Register application: show overviews of classes', allow_abbrev=False)

    help_str = 'show only those classes whose department contains '
    parser.add_argument('-d', type = str, help = help_str+'dept', action = 'store', metavar='dept')
    parser.add_argument('-n', type = str, help = help_str+'num', action = 'store', metavar='num')
    parser.add_argument('-a', type = str, help = help_str+'area', action = 'store', metavar='area')
    parser.add_argument('-t',type = str, help = help_str+'title', action = 'store', metavar='title')

    dept = parser.parse_args().d
    num = parser.parse_args().n
    area = parser.parse_args().a
    title = parser.parse_args().t

    try:
        with connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
            with closing(connection.cursor()) as cursor:

                stmt =  "SELECT classes.classid, crosslistings.dept, crosslistings.coursenum, "
                stmt +=         "courses.area, courses.title "
                stmt += "FROM crosslistings, courses, classes "
                stmt += "WHERE courses.courseid = crosslistings.courseid "
                stmt += "AND classes.courseid = crosslistings.courseid "

                if dept:
                    dept = dept.replace('%', r'\%')
                    dept = dept.replace('_', r'\_')
                    tags.append("%" + dept.lower() + "%")
                    stmt += "AND lower(crosslistings.dept) like ? ESCAPE '\\' "

                if num:
                    num = num.replace('%', r'\%')
                    num = num.replace('_', r'\_')
                    tags.append("%" + num.lower() + "%")
                    stmt += "AND lower(crosslistings.coursenum) like ? ESCAPE '\\' "

                if area:
                    area = area.replace('%', r'\%')
                    area = area.replace('_', r'\_')
                    tags.append("%" + area.lower() + "%")
                    stmt += "AND lower(courses.area) like ? ESCAPE '\\' "

                if title:
                    title = title.replace('%', r'\%')
                    title = title.replace('_', r'\_')
                    tags.append("%" + title.lower() + "%")
                    stmt += "AND lower(courses.title) like ? ESCAPE '\\'"

                stmt += "ORDER BY crosslistings.dept, crosslistings.coursenum, classes.classid;"

                cursor.execute(stmt, tags)

                row = ["-----", "----", "------", "----", "-----"]

                print("ClsId Dept CrsNum Area Title")
                while row:
                    text = f"{row[0]:>5} {row[1]:>4} {row[2]:>6} {row[3]:>4} {row[4]}"
                    print(textwrap.fill(text, initial_indent='', subsequent_indent=' ' * 23, break_long_words=False, width=72,))
                    row = cursor.fetchone()

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == "__main__":
    main()
