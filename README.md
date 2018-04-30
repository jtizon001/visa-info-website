# Final Project for MJ583 course at UNC visa-info-website

http://192.241.142.13/

**Discription**
This website provides travel information for U.S. citizens traveling abroad such as advsories, visa requirements and embassy locations. All This information was gathered through webscraping from travel.state.gov

**This site uses a python3 backend.**
* Flask microframe work
* sqlite3 database
* scrapy and requests to connect to travel.state.giv
* jinja to build templates

**Frontend technologies**
* d3.js library was used for world map visualization
* bootstrap library for styling

**Setup**
* pip install requirements.txt
  * if this fails, simply pip install the required packages as shown in error messages
* databases is not included in repo
  * run python sql.py
* Once databese is built run python api.py
  * If you wish to run this locally you may need to change line 187 on api.py to app.run()
