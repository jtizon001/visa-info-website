# -*- coding: utf-8 -*-
import requests
import scrapy
import json
import re
import pprint
import pycountry

chart=''

def main(): #main method for scraping
    url = 'https://travel.state.gov/content/travel/en/international-travel/International-Travel-Country-Information-Pages/'
    urls = []
    country_dict={}
    count=0
    for country in pycountry.countries: #loop through every country in library and concatinate them into the link
        try:
            # if count==1:
            #     break
            x=country.name.replace(' ', '').replace("'", '').replace(',','')
            if '(' in x and ')' in x:
                x=x.split('(')[0]

            url4req=url+fix(x)+'.html'

            alpha=country.alpha_3

            r = requests.get(url4req, headers={'User-Agent': 'UNC :)'}, )
            page_content = r.content.decode('utf-8')
            sel = scrapy.Selector(text=page_content)


            #each variable is an intance of every section of countries page
            travel_advisory = sel.css('#tsg-rwd-advisories .tsg-rwd-eab-title-frame').xpath('string()').extract()[0]
            travel_advisory_info = sel.css('.tsg-rwd-alert-more-box > .tsg-rwd-alert-more-box-content').extract()[
                0]  # html tags included for simplicity
            chart = sel.css(
                '.tsg-rwd-sidebar-qf-csi-show > .tsg-rwd-sidebar-copy.tsg_rwd_textbox_full > .tsg-rwd-qf-column').extract()[
                    :2]
            embassies = sel.css('.set_1.tsg-rwd-accordion-csi-show .tsg-rwd-accordion-copy').extract()[
                0]  # html tags included
            dest_info = sel.css('.set_1.tsg-rwd-accordion-csi-show .tsg-rwd-accordion-copy ').extract()[
                1]  
            visa_reqs = sel.css('.set_1.tsg-rwd-accordion-csi-show .tsg-rwd-accordion-copy ').extract()[2]
            safety_security = sel.css('.set_1.tsg-rwd-accordion-csi-show .tsg-rwd-accordion-copy ').extract()[3]
            laws_special_circumstance = sel.css('.set_1.tsg-rwd-accordion-csi-show .tsg-rwd-accordion-copy').extract()[4]
            health = sel.css('.set_1.tsg-rwd-accordion-csi-show .tsg-rwd-accordion-copy').extract()[5]
            travel_trans = sel.css('.set_1.tsg-rwd-accordion-csi-show .tsg-rwd-accordion-copy').extract()[6]

            country_name=travel_advisory.split('Level')[0]
            country_name=country_name[:-3]
            print(country_name+': '+alpha)

            
            con_dict={ #each country in saved into this local dictionary.
                'country_name':country_name,
                'travel_advisory':travel_advisory,
                'alpha':alpha,
                'travel_advisory_info':travel_advisory_info,
                'chart':chart,
                'embassies':embassies,
                'destination_info':dest_info,
                'visa_reqs': visa_reqs,
                'safety_security':safety_security,
                'laws':laws_special_circumstance,
                'health':health,
                'travel_trans':travel_trans,
            }
            country_dict[country_name]=con_dict #local dictionary is pushed into global dictionary
            count=count+1
        except:
            pass

    #print(country_dict)
    jsonStr = json.dumps(country_dict)
    f = open("country_data.json", "w")
    f.write(jsonStr)
    f.close



#method fixes name inconsistancies

def fix(s):
    #print(s)
    if s == 'BoliviaPlurinationalStateof':
        return 'Bolivia'
    if s == 'BruneiDarussalam':
        return 'Brunei'
    if s == 'CôtedIvoire':
        return 'CotedIvoire'
    if s == 'CongoTheDemocraticRepublicofthe':
        return 'DemocraticRepublicoftheCongoDRC'
    if s == 'Congo':
        return 'RepublicoftheCongo'
    if s == 'Curaçao':
        return 'Curacao'
    if s == 'MicronesiaFederatedStatesof':
        return 'Micronesia'
    if s == 'Gibratlar':
        return 'Gilbratar'
    if s == 'IranIslamicRepublicof':
        return 'Iran'
    if s == 'KoreaRepublicof':
        return 'SouthKorea'
    if s == 'LaoPeoplesDemocraticRepublic':
        return 'Laos'
    if s == 'Macao':
        return 'Macau'
    if s == 'SaintMartin':
        return 'FrenchWestIndies'
    if s == 'MoldovaRepublicof':
        return 'Moldova'
    if s == 'MacedoniaRepublicof':
        return 'Macedonia'
    if s == 'Myanmar':
        return 'Burma'
    if s == 'Martinique':
        return 'FrenchWestIndies'
    if s == 'TaiwanProvinceofChina':
        return 'Taiwan'
    if s == 'TanzaniaUnitedRepublicof':
        return 'Tanzania'
    if s == 'VenezuelaBolivarianRepublicof':
        return 'Venezuela'
    if s == 'VirginIslandsBritish':
        return 'BritishVirginIslands'
    if s == 'VietNam':
        return 'Vietnam'
    if s == 'IsleofMan':
        return 'IsleOfMan'
    if s == 'Gambia':
        return 'TheGambia'
    if s == 'SaintBarthélemy':
        return 'FrenchWestIndies'
    return s



if __name__ == '__main__':
    main()
####################_______junk_code________################
# chart=sel.css('.tsg-rwd-qf-column *::text')[:2][0] #)[:2].xpath('string()').extract()#('.tsg-rwd-main-CSI-International-Travel-items-international')[0].xpath('string()')
#.tsg-rwd-sidebar-copy.tsg_rwd_textbox_full+.tsg-rwd-qf-column

#Bolivia = BoliviaPlurinationalStateof
#Brunei = BruneiDarussalam
#CotedIvoire = CôtedIvoire
#DemocraticRepublicoftheCongoDRC = CongoTheDemocraticRepublicofthe
#RepublicoftheCongo = Congo
#Curacao = Curaçao
#CzechRepublic = Czechia
#Micronesia = MicronesiaFederatedStatesof
#Gilbratar= Gibratlar
#Iran = IranIslamicRepublicof
#SouthKorea = KoreaRepublicof
#Loas = LaoPeoplesDemocraticRepublic
#Macau = Macao
#FrenchWestIndies = SaintMartin
#Moldova = MoldovaRepublicof
#Macedonia = MacedoniaRepublicof
#Burma = Myanmar
#FrenchWestIndies = Martinique
#Taiwan= TaiwanProvinceofChina
#Tanzania = TanzaniaUnitedRepublicof
#Venezuela = VenezuelaBolivarianRepublicof
#BritishVirginIslands = VirginIslandsBritish
#Vietnam= VietNam
#IsleOfMan=IsleofMan
#TheGambia=Gambia
#FrenchWestIndies = SaintBarthélemy


