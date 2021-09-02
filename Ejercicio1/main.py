from database import connection
from database import Valor

from fastapi import FastAPI
from fastapi import HTTPException
from utils import get_currency

from schemas import UserRequestModel
from schemas import UserResponseModel

import requests
import json

webhook_url='https://webhook.site/4ed54cff-41ba-423e-9f46-b2c87408daf9'


 
app=FastAPI(title='pruabaTL',
            desciption='Esto es un API',
            version='1.0.1')

data_currency=get_currency("2021-08-27", "2021-09-02", "daily",'EURUSD=X')
data_valores=[]

connection.connect()
connection.create_tables([Valor])
for x in data_currency["EURUSD=X"].get("prices"):
    val=Valor(valores_cambio=str(round(x.get("adjclose"),4)),fecha=x.get("formatted_date"),fromCurrency='EUR',toCurrency='USD')
    val.save()

connection.close()


@app.on_event('startup')
def startup():
    if connection.is_closed:
        connection.connect()

@app.on_event('shutdown')
def shutdown():
    if  not connection.is_closed:
        connection.close()
    

@app.get('/valores/{user_id}')
async def get_valor(user_id):
    valor=Valor.select().where(Valor.id==user_id).first()

    if (valor):
        data_webhook={
                'name':'PruebaTL Luis Mena',
                'id': valor.id,
                'from_currency': valor.fromCurrency,
                'to_currency': valor.toCurrency,
                'date': valor.fecha,
                'Value': valor.valores_cambio
            }
        r=requests.post(webhook_url, data=json.dumps(data_webhook), headers={'Content-Type':'application/json'})

        return  UserResponseModel(id=valor.id,valores_cambio=valor.valores_cambio, fecha=valor.fecha)
    else:
        return HTTPException(404,'Valor no encontrado')

@app.post('/new_valor')
async def set_valor(valores_request:UserRequestModel):

    valor=Valor.create(
        valores_cambio=valores_request.valores_cambio,
        fecha=valores_request.fecha
    )

    return 'Valor guardado ',valores_request