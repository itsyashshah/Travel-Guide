from bs4 import BeautifulSoup
import requests
import json
def place(f_name):
    try:

        url = "http://tourism.rajasthan.gov.in/"

        url_final = url + f_name+'.html'
        r = requests.get(url_final)
        soup = BeautifulSoup(r.text , "lxml")
        l_place = []
        for s in soup.find_all('div', {'class': 'articleCont'}):
            # print s.h4.text
            # print s.p.text

            l_place.append(s.h4.text)
        return l_place


    except:
            pass
