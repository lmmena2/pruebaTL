import requests
import boto3
import time
import json
import os
from datetime import datetime
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return (str(o) for o in [o])
        return super(DecimalEncoder, self).default(o)


def get_property_value(raw_data, property):
    value = raw_data.get("content", {}).get(property, 0)
    return round(Decimal(value), 2)


def create_new_record(table, data, dynamodb):
    table = dynamodb.Table(table)
    response = table.put_item(Item=data)
    return response


def get_all_db_records(table, dynamodb):
    table = dynamodb.Table(table)
    return table.scan()


def job(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    start_time = time.time()
    time_elapsed = 0
    while time_elapsed < int(os.environ['TASK_TIME']):
        time_elapsed = time.time() - start_time
        print(time_elapsed)
        response = requests.get(os.environ['SERVICE_END_POINT'])
        response = response.json()
        device_data = response['with']
        for data in device_data:
            record_data = {"temperature": get_property_value(data, "temperature"),
                           "humidity": get_property_value(data, "humidity"),
                           "collected_date": str(datetime.now())}
            print(record_data)
            create_new_record(table, record_data, dynamodb)
        time.sleep(int(os.environ['WAIT_TIME']))
    all_records = get_all_db_records(table, dynamodb)
    webhook_data = {"name": "PruebaTL Luis Mena", "items": all_records["Items"]}
    requests.post(os.environ['WEBHOOK_END_POINT'], json.dumps(webhook_data, cls=DecimalEncoder))
    body = {
        "message": "Data Send",
        "input": event,
    }
    return {"statusCode": 200, "body": json.dumps(body)}
