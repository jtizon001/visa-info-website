import sqlite3
import pprint


def main():
    conn=sqlite3.connect('countries.db')
    c=conn.cursor()

    q1=c.execute('''select count(nameKey) from COUNTRIES''').fetchall()
    pprint.pprint(q1)
    q2=c.execute('''select name, travelAdvisory from COUNTRIES as c 
        where c.travelAdvisory like "%Level 4%" or c.travelAdvisory like "%Level 3#"''').fetchall()
    #pprint.pprint(q2)
    q3=c.execute('''select travelAdvisory from COUNTRIES''').fetchall()
    #pprint.pprint(q3)






if __name__ =='__main__':
    main()