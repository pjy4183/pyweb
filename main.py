import requests
from bs4 import BeautifulSoup
import pandas 

URI = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"
serviceKey = "s4VjSKkMN%2FDUYkjeDIT1UKgTY4CxOdHsj%2BLVlRas530tNu6R8isIPPXuh1nKKqY9pYq%2BQHyfjesnlL%2Bd6lSlhQ%3D%3D"
SideoName = "sidoName=서울"
PageNumber = "&pageNo=1"
NumofRows = "&numofRows=10"
Service = "&ServiceKey=" + serviceKey

URI = URI + SideoName + PageNumber + NumofRows + Service
response = requests.get(URI)

soup = BeautifulSoup(response.text, 'html.parser')
Itemlist = soup.findAll('item')

datetimeList = []
citynameList = []
so2valueList = []
covalueList = []
o3valueList = []
no2valueList = []
pm10valueList = []
khaivalueList = []

for item in Itemlist:
    datetime = item.find('datatime').text
    cityname = item.find('stationname').text
    so2value = item.find('so2value').text
    covalue = item.find('covalue').text
    o3value = item.find('o3value').text
    no2value = item.find('no2value').text
    pm10value = item.find('pm10value').text
    khaivalue = item.find('khaivalue').text

    datetimeList.append(datetime)
    citynameList.append(cityname)
    so2valueList.append(so2value)
    covalueList.append(covalue)
    o3valueList.append(o3value)
    no2valueList.append(no2value)
    pm10valueList.append(pm10value)
    khaivalueList.append(khaivalue)

print("데이터 모으기 끝!!")

DATA = pandas.concat([pandas.DataFrame(datetimeList),
pandas.DataFrame(citynameList),
pandas.DataFrame(so2valueList),
pandas.DataFrame(covalueList),
pandas.DataFrame(o3valueList),
pandas.DataFrame(no2valueList),
pandas.DataFrame(pm10valueList),
pandas.DataFrame(khaivalueList)], axis=1)


DATA.to_excel("서울시_미세먼지데이터.xlsx",index=False)
