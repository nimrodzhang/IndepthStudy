import json
import base64
import time
import boto3

from kafka import KafkaProducer
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    
    producer = KafkaProducer(bootstrap_servers=['your_kafka_broker_1:9092','your_kafka_broker_2:9092'])

    
    
    for record in event['records']['RawRequest-0']:
        raw_message = base64.b64decode(record['value'])
        message = raw_message.decode('utf-8')
        print(message)
        
        status = 'deny'
        
        data = json.loads(message)
        if(data['place'] == 'us'):
            if(data['type'] == 'Online Shopping' and data['amount']<=800):
                status = 'approve'
            if(data['type'] == 'Dining' and data['amount']<=300):
                status = 'approve'
            if(data['type'] == 'Grocery' and data['amount']<=200):
                status = 'approve'
            if(data['type'] == 'Offline Shopping' and data['amount']<=1000):
                status = 'approve'
                
        
        
        data['status'] = status
        
        new_mes = json.dumps(data)
        
        print(new_mes)
        
        producer.send('RequestApproval', new_mes.encode('utf8'))
        
        
        table_req = dynamodb.Table('new_requests')
        
        # update total number count
        if status == 'approve':
            get_resp = table_req.get_item(Key = {'status': 'approveNum', 'requestID': '0'})
            print(get_resp)
            total = get_resp['Item']['requestNum'] + 1
            
            update_resp = table_req.update_item(
                Key = {'status': 'approveNum', 'requestID': '0'},
                UpdateExpression = "set requestNum=:t",
                ExpressionAttributeValues = {':t': total},
                ReturnValues="UPDATED_NEW"
            )
        else:
            get_resp = table_req.get_item(Key = {'status': 'denyNum', 'requestID': '0'})
            print(get_resp)
            total = get_resp['Item']['requestNum'] + 1
            
            update_resp = table_req.update_item(
                Key = {'status': 'denyNum', 'requestID': '0'},
                UpdateExpression = "set requestNum=:t",
                ExpressionAttributeValues = {':t': total},
                ReturnValues="UPDATED_NEW"
            )
        
        
        response = table_req.put_item(
            Item = data
        )
        print("Response of put item in DB")
        print(response)
        
    producer.flush()
    producer.close()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
