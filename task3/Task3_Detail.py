import json
import base64
import time
# import boto3

from kafka import KafkaProducer

# from boto3.dynamodb.conditions import Key, Attr
# from botocore.exceptions import ClientError

# dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    
    producer = KafkaProducer(bootstrap_servers=['your_kafka_broker_1:9092','your_kafka_broker_2:9092'])
    
    for record in event['records']['RequestApproval-0']:
        raw_message = base64.b64decode(record['value'])
        message = raw_message.decode('utf-8')
        print(message)
        
        data = json.loads(message)
        
        if data['status'] == 'deny':
            continue
        else:
            del data['status']
            new_mes = json.dumps(data)
            
            print(new_mes)
            
            producer.send('TransDetail', new_mes.encode('utf-8'))
    
    producer.flush()
    producer.close()