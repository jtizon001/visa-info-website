import sqlite3
import json
import pprint

def main(): #building sqlite database
    country_dict=json.loads(open('country_data.json').read())
    #print(country_dict)
    
    conn = sqlite3.connect('countries.db')
    c = conn.cursor()

    #drop tables incase everytime this runs,avoiding data clashes
    c.execute('DROP TABLE IF EXISTS "COUNTRIES"')

    #table schema, only one table needed. no duplicates in country names
    c.execute('''CREATE TABLE COUNTRIES(
      nameKey text primary key, 
      name text,
      alpha text,
      travelAdvisory text,
      travelAdvisoryInfo text,
      chartLeft text,
      chartRight text,
      embassies text,
      destinationInfo text,
      visaReqs text,
      safety text,
      laws text,
      health text,
      travel text
    )''')
   # print(len(country_dict))

    for x in country_dict: #iterates through json and add each item
        c.execute('''insert into COUNTRIES values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                  [country_dict[x]['country_name'].replace(' ','').replace(',',''),
                   country_dict[x]['country_name'],
                   country_dict[x]['alpha'],
                    country_dict[x]['travel_advisory'],
                  country_dict[x]['travel_advisory_info'],
                  country_dict[x]['chart'][0],
                  country_dict[x]['chart'][1],
                  country_dict[x]['embassies'],
                  country_dict[x]['destination_info'],
                  country_dict[x]['visa_reqs'],
                  country_dict[x]['safety_security'],
                  country_dict[x]['laws'],
                  country_dict[x]['health'],
                  country_dict[x]['travel_trans']])



    conn.commit()
    #### use sqlqueries.py to check if db is populated
    #cTest1=c.execute('''select travelAdvisory from COUNTRIES where name="Argentina"''').fetchall()
    #pprint.pprint(cTest1)
    #cTest2=c.execute('''select name,alpha from COUNTRIES''').fetchall()
    #pprint.pprint(cTest2)
    #pprint.pprint(c.execute('''select count(nameKey) from COUNTRIES''').fetchall())
    conn.close()



if __name__ == '__main__':
    main()