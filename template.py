from bs4 import BeautifulSoup
import requests
import json
def hotel(f_name):

    try:

        url = "https://www.holidify.com/places/"+f_name+"/hotels-where-to-stay.html"

        url_final = url
        r = requests.get(url_final)
        soup = BeautifulSoup(r.text , "lxml")
        l_hotel = []
        for s in soup.find_all('div', {'class': ' col-md-6 col-xs-7 nopadding'}):

            l_hotel.append(s.h4.text +s.p.text)

        return l_hotel
    except:
        pass
