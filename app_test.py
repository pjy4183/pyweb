# -- coding: utf-8 --
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from string import Template
import datetime
import pytz

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'


db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)



def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid=f69167b991bfeed068e309a6b69cd883'
    r = requests.get(url).json()
    return r


@app.route('/')
def index():
    URI = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?"
    serviceKey = "s4VjSKkMN%2FDUYkjeDIT1UKgTY4CxOdHsj%2BLVlRas530tNu6R8isIPPXuh1nKKqY9pYq%2BQHyfjesnlL%2Bd6lSlhQ%3D%3D"
    ItemCode = "itemCode=PM10" #PM10 = 미세먼지
    DataGubun = "&dataGubun=HOUR" #DAILY or HOUR
    SearchCond = "&searchCondition=MONTH" #MONTH or WEEK
    NumofRows = "&numOfRows=1"
    Service = "&ServiceKey=" + serviceKey
    URI_pm10 = URI + ItemCode + DataGubun + SearchCond + NumofRows + Service
    response = requests.get(URI_pm10)

    soup = BeautifulSoup(response.text, 'html.parser')

    #pm25 
    ItemCode = "itemCode=PM25" #PM10 = 초미세먼지
    URI_pm25 = URI + ItemCode + DataGubun + SearchCond + NumofRows + Service
    response_pm25 = requests.get(URI_pm25)

    soup25 = BeautifulSoup(response_pm25.text, 'html.parser')

    pm10 = {
        'seoul' : soup.find('seoul').text,
        'busan' : soup.find('busan').text,
        'daegu' : soup.find('daegu').text,
        'incheon' : soup.find('incheon').text,
        'gwangju' : soup.find('gwangju').text,
        'daejeon' : soup.find('daejeon').text,
        'ulsan' : soup.find('ulsan').text,
        'gyeonggi' : soup.find('gyeonggi').text,
        'gangwon' : soup.find('gangwon').text,
        'chungbuk' : soup.find('chungbuk').text,
        'chungnam' : soup.find('chungnam').text,
        'jeonbuk' : soup.find('jeonbuk').text,
        'jeonnam' : soup.find('jeonnam').text,
        'gyeongbuk' : soup.find('gyeongbuk').text,
        'gyeongnam' : soup.find('gyeongnam').text,
        'jeju' : soup.find('jeju').text,
        'sejong' : soup.find('sejong').text
    }


    pm25 = {
        'seoul' : soup25.find('seoul').text,
        'busan' : soup25.find('busan').text,
        'daegu' : soup25.find('daegu').text,
        'incheon' : soup25.find('incheon').text,
        'gwangju' : soup25.find('gwangju').text,
        'daejeon' : soup25.find('daejeon').text,
        'ulsan' : soup25.find('ulsan').text,
        'gyeonggi' : soup25.find('gyeonggi').text,
        'gangwon' : soup25.find('gangwon').text,
        'chungbuk' : soup25.find('chungbuk').text,
        'chungnam' : soup25.find('chungnam').text,
        'jeonbuk' : soup25.find('jeonbuk').text,
        'jeonnam' : soup25.find('jeonnam').text,
        'gyeongbuk' : soup25.find('gyeongbuk').text,
        'gyeongnam' : soup25.find('gyeongnam').text,
        'jeju' : soup25.find('jeju').text,
        'sejong' : soup25.find('sejong').text
    }

    return render_template('index.html', pm10=pm10, pm25=pm25)




@app.route('/templates/weather.html')
def index_get():
    cities = City.query.all()

    weather_data=[]

    for city in cities:
        r = get_weather_data(city.name)
        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)
        

    return render_template('weather.html', weather_data=reversed(weather_data))


@app.route('/templates/weather.html', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
        
    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
            new_city_data = get_weather_data(new_city)
            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city)

                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = 'City does not exist!'
        else:
            err_msg = 'City already exists!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added successfully')


    return redirect(url_for('index_get'))

@app.route('/delete/<name>')
def delete_city(name):
    city =  City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted { city.name }', 'success')
    return redirect(url_for('index_get'))

@app.route('/templates/<some_place>')
def some_place_page(some_place):
    nx, ny = get_city_name(some_place)
    nx = "&nx=" + nx
    ny = "&ny=" + ny
    URI = get_kor_weather_API(nx, ny)
    r = requests.get(URI)

    soup = BeautifulSoup(r.text, 'html.parser')
    Itemlist = soup.findAll('item')
    data = ITEMLIST(Itemlist)
    
    weather = {
        'city' : some_place,
        'rainType' : data[1],
        'humidity' : data[3],
        'ratio': data[5],
        'temperature' : data[7],
        'windspeed' : data[9]
    }

    r = get_weather_data(some_place)
    weather2 = {
        'city' : some_place,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
    }

    return render_template('template.html', place_name=some_place, weather=weather, weather2=weather2)



def get_kor_weather_API(nx, ny):
    currentdate = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
    currenthour = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H')
    currentminute = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%M')

    if int(currentminute) >= 30:
        pass
    elif int(currentminute) < 30:
        currenthour = int(currenthour) - 1
    if len(str(currenthour)) < 2:
        currenthour = "0" + str(currenthour)


    URI = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst?"
    serviceKey = "oH7Ka3pHFV6tlkknSOGHpi5zCFaWyWUHC1MXmLCrwosu5D%2Bw9Xun%2BI25lqyLs4Vhls178qpID%2B2WNWB%2F6h%2Bywg%3D%3D"
    base_date = "base_date=" + str(currentdate)
    base_time = "&base_time=" + str(currenthour) + "00"
    numOfRows = "&numOfRows=10"
    pageNo = "&pageNo=1"
    Service = "&ServiceKey=" + str(serviceKey)
    URI = URI + base_date + base_time + nx + ny + numOfRows + pageNo + Service

    return URI

def ITEMLIST(Itemlist):
    weather = []
    for item in Itemlist:
        category = item.find("category").text #날씨코드
        obsValue = item.find("obsrvalue").text

        if category == "PTY": #강수형태
            # (없음(0), 비(1), 비 / 눈(2), 눈(3), 소나기(4) 여기서 비 / 눈은 비와 눈이 섞여 오는 것을 의미 (진눈개비))
            obsValue = item.find("obsrvalue").text
            weather.append('강수형태')
            if obsValue == '0':
                weather.append('없음')
            elif obsValue == '1':
                weather.append('진눈개비')
            elif obsValue == '2':
                weather.append('눈')
            elif obsValue == '3':
                weather.append('소나기')
        elif category == "REH": #습도
            obsValue = item.find("obsrvalue").text
            weather.append('습도')
            weather.append(obsValue + '%')
        elif category == "RN1": #1시간 강우량
            obsValue = item.find("obsrvalue").text
            weather.append('강우량')
            weather.append(obsValue + 'mm')
        elif category == "T1H": #기온
            obsValue = item.find("obsrvalue").text
            weather.append('기온')
            weather.append(obsValue + 'C')
        elif category == "WSD": #풍속
            obsValue = item.find("obsrvalue").text
            weather.append('풍속')
            weather.append(obsValue + 'm/s')
        else:
            continue
    return weather

def get_city_name(some_place):
    location = [['60', '127', 'seoul'], #서울
                ['98', '76', 'busan'], #부산
                ['89', '90', 'daegu'], #대구
                ['55', '124', 'incheon'], #인천
                ['58', '74','gwangju'], #광주
                ['67', '100','daejeon'], #대전
                ['102', '84','ulsan'], #울산
                ['60', '120','gyeonggi'], #경기도
                ['73', '134','gangwon'], #강원도
                ['69', '107','chungbuk'], #충북
                ['68', '100','chungnam'], #충남
                ['63', '89','jeonbuk'], #전북
                ['51', '67','jeonnam'], #전남
                ['89', '91','gyeongbuk'], #경북
                ['91', '77','gyeongnam'], #경남
                ['52', '38','jeju'], #제주
                ['66', '103','sejong'], #세종
                ]

    for i in location:
        if (i[2] == some_place):
            return i[0], i[1] 



