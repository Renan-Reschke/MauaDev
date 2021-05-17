import requests
import uuid
from copy import deepcopy # copy an object, creating an INDEPENDENT new one
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import Any, List


class City(BaseModel):
    id : str
    index : int
    name : str
    timezone : str
    datetime : str

    def _init_(self, **data: Any):
        super()._init_(**data)
        self.id = uuid.uuid1()
        self.index = len(cities.db)

    def getDatetime(self):
        url = f'http://worldtimeapi.org/api/timezone/{self.timezone}'
        try:
            req = requests.get(url).json()
        except:
            raise Exception(f'Could not get datetime for {self.name}.')
        
        self.datetime = req['datetime']
        res = deepcopy(self)
        self.datetime = ''
        return res
        
class Cities():
    db = []

    @staticmethod
    def appendCity(city: City):
        for d in cities.db:
            if city.name.lower().replace(' ', '') == d.name.lower().replace(' ', ''):
                raise Exception('City already in DB.')
        cities.db.append(city)

    @staticmethod
    def getCity(cityID: str):
        for i in range(len(cities.db)):
            city = cities.db[i]
            if cityID == str(city.id):
                return city
        
        raise Exception('City not found.')

    def getCityByIndex(self, searchIndex : int):
        for i in range(len(cities.db)):
            city = cities.db[i]
            if searchIndex == city.index:
                return city
        
        raise Exception('City not found.')

cities = Cities()

app = FastAPI()

@app.get('/')
def index():
    return { 'msg' : 'Bem vindo ao FastAPI!' }

@app.get('/cities')
def getCities():
    return cities.db

@app.get('/cities/times/{cityID}')
def getDatetime(cityID : str, response : Response):
    try:
        city = cities.getCity(cityID)
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        print(e)
        return { 'msg' : str(e) }
    
    try:
        res = city.getDatetime()
    except Exception as e:
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        print(e)
        return { 'msg' : str(e) }
    
    return res


@app.get('/cities/times')
def getDatetimes(response : Response):
    results = []
    for city in cities.db:
        try:
            results.append(city.getDatetime())
        except Exception as e:
            response.status_code = status.HTTP_408_REQUEST_TIMEOUT
            print(e)
                
    return results

@app.get('/cities/{cityID}')
def _getCity(cityID: str, response : Response):
    try:
        city = cities.getCity(cityID)
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        print(e)
        return { 'msg' : str(e) }

    return city

@app.post('/cities', status_code=201)
def inputCities(citiesInput: List[City], response: Response):
    appendCount = 0
    for city in citiesInput:
        try:
            cities.appendCity(city)
        except:
            pass
        else:
            appendCount += 1

    if appendCount == 0:
        return {}
    else:
        return cities.db[-appendCount:]

@app.delete('/cities/{cityID}')
def deleteCity(cityID: str, response: Response):
    try:
        city = cities.getCity(cityID)
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        print(e)
        return { 'msg' : str(e) }
    
    cities.db.pop(city.index)
    return city