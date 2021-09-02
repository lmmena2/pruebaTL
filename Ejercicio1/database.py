from peewee import MySQLDatabase
from peewee import Model,CharField


connection=MySQLDatabase(
    'pruebaTL',
    user='root', password='Kiara@123',
    host='localhost', port=3306
)

class Valor(Model):
    valores_cambio = CharField(max_length=50)
    fecha = CharField(max_length=50)
    fromCurrency = CharField(max_length=7)
    toCurrency = CharField(max_length=7)

    def __str__(self):
        return self.valores_cambio
    
    class Meta:
        database=connection
        table_name='valores'
