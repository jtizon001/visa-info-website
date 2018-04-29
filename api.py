#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, url_for, jsonify, json
from flask import render_template
from flask import Markup, send_file
import pprint
import sqlite3
import os
import pprint
import pandas as pd
from io import StringIO, BytesIO

import matplotlib.pyplot as plt
#import PIL
#from PIL import Image, ImageDraw
import csv
import pycountry
import reqPractice

##### main file

plt.switch_backend('agg')
app = Flask(__name__)
#app.debug=True


###renders index page of site
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


### gets every country name and makes list of names and hrefs
@app.route('/country/', methods=['GET'])
def country_list():
    conn = sqlite3.connect('./countries.db')
    c=conn.cursor()
    countries=c.execute('''select name,alpha from COUNTRIES''').fetchall()
    #print(len(countries))
    country_list=[]
    for x in range(len(countries)):
        #print(x)
        url= countries[x][1]
        # if ',' in url:
        #     url=url.replace(',','')
        country_list.append({
            'name':countries[x][0],
            'url':'/country/'+url
        })
    pprint.pprint(country_list)

    return render_template('country_list.html', title='List', country_list=country_list)




#method called on startup, will read json file to colorcoat the map
@app.route('/country/map_maker', methods=['GET'])
def map_map():
    conn=sqlite3.connect('./countries.db')
    c=conn.cursor()
    map_list=[]
    iter_alpha=c.execute('''select alpha from COUNTRIES''').fetchall()
    print(len(iter_alpha))
    for x in range(len(iter_alpha)):
        try:
            advisory = c.execute('''select travelAdvisory from COUNTRIES where alpha = ?''',
                                 (iter_alpha[x][0],)).fetchall()[0][0]
            advisory_lvl=''
            if ':' in advisory:
                advisory_lvl = advisory[advisory.index(':') - 2:advisory.index(':')].strip()
            else:
                advisory_lvl=advisory.strip()[-1]
            map_list.append({
                'Country': iter_alpha[x][0],
                '1801': 0,#advisory,
                'Advisory': int(advisory_lvl),
                '1802':0
                })

        except:
            print(iter_alpha[x][0])

            pass

    map_dict = {'map_info': map_list}

    df=pd.DataFrame(map_list)
    df=df[['country','1800','1801','1802']]
    print(df)
    df.to_csv('domain.csv', index=False, header=True)
    response=jsonify(map_dict)

    #pprint.pprint(map_list)
    return response #'this shit work'


##this can be used to pull files saved in /static/data directory
@app.route('/data/<x>', methods = ['GET'])
def data(x):
    print(x)
    return app.send_static_file('data/'+x)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500


#used to make pie chart in bytestream and send to front end as an image
@app.route('/chart/', methods=['GET'])
def chart():
    print('yo')
    conn = sqlite3.connect('./countries.db')
    c = conn.cursor()
    labels = 'Level 1', 'Level 2', 'Level 3', 'Level 4'
    colors=['green', 'yellow','orange','red']
    lvl_1 = c.execute('''select count(*) from COUNTRIES where travelAdvisory like "%1%"''').fetchall()[0][0]
    lvl_2 = c.execute('''select count(*) from COUNTRIES where travelAdvisory like "%2%"''').fetchall()[0][0]
    lvl_3 = c.execute('''select count(*) from COUNTRIES where travelAdvisory like "%3%"''').fetchall()[0][0]
    lvl_4 = c.execute('''select count(*) from COUNTRIES where travelAdvisory like "%4%"''').fetchall()[0][0]
    print(lvl_1)
    print(lvl_2)
    print(lvl_1 + lvl_2)
    sizes = [lvl_1, lvl_2, lvl_3, lvl_4]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels,colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')



    img=BytesIO()
    fig1.savefig(img,format='png',transparent=True)
    img.seek(0)


    return send_file(img, mimetype='image/png')


#this route queries every section scraped from country page and serves them into the template
@app.route('/country/<x>', methods = ['GET'])
def country(x):
    try:
        conn = sqlite3.connect('./countries.db')
        c = conn.cursor()
        path = os.path.abspath('./countries.db')
        
        #Each variable is a call to the db to get each section

        xAdvisory=c.execute('''select travelAdvisory from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        #print(xAdvisory)
        name=c.execute('''select name from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        advisoryInfo= c.execute('''select travelAdvisoryInfo from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        chartLeft= c.execute('''select chartLeft from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        chartRight=c.execute('''select chartRight from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        embassies=c.execute('''select embassies from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        destinationInfo=c.execute('''select destinationInfo from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        visaReqs=c.execute('''select visaReqs from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        safety=c.execute('''select safety from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        laws=c.execute('''select laws from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        health= c.execute('''select health from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]
        travel=c.execute('''select travel from COUNTRIES as c where c.alpha = ?''', (x,)).fetchall()[0][0]

        conn.close()
        #html = render_template('index.html')
        #print('\n'+xAdvisory[0][0]+'\n')
    
    except:
        return render_template('404.html')

    return render_template('country.html',title=name,xAdvisory=xAdvisory,advisoryInfo=Markup(advisoryInfo),
                           chartLeft=Markup(chartLeft),chartRight=Markup(chartRight), embassies=Markup(embassies),
                           destinationInfo=Markup(destinationInfo), visaReqs=Markup(visaReqs), safety=Markup(safety),
                           laws=Markup(laws), health=Markup(health), travel=Markup(travel))





if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=80)

