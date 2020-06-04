import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from string import Template

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

pm10_1={}

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
    pm10_1 = pm10
    return render_template('index.html', pm10=pm10, pm25=pm25)


@app.route('/templates/weather.html')
def index_get():
    cities = City.query.all()

    weather_data = []

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









f = open('./templates/template.html', 'rt', encoding='UTF8')
f_read = f.read()

# HTML_TEMPLATE = Template(f_read) #밑에 코드 대신 이 코드로 대체 가능
HTML_TEMPLATE = Template('''
<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <title>서울 정보</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <style>
        .nav-distance{
            padding: 1.0% 5.2%;
            background-color:rgba(217, 246, 102, 0.5);
        }
  
        .navbar-light .navbar-brand{
            font-family: NanumSquareR;
            line-height: 1.68;
            text-align: left;
            color: #35465d;
        }
    </style>
</head>
<body>
    
    <nav class="navbar navbar-expand-lg navbar-light nav-distance">
        <a class="navbar-brand" href="/">Weather</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item active">
              <a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/templates/weather.html">Search</a>
            </li>
            
          </ul>
        </div>
      </nav>
      
    ${place_name} 정보 
    f{{pm10.seoul}}
    {%pokemon.a%}

</body>
</html>
''')


@app.route('/templates/<some_place>')
def some_place_page(some_place):
    
    return(HTML_TEMPLATE.substitute(place_name=some_place))



@app.route('/templates/<some_place>')
def americano():
    pokemon = {
        'a': 1,
        'b': 2,
        'c':3
    }
    pm10 = pm10_1
    return render_template('some_place', pm10_1=pm10_1,pokemon=pokemon)


