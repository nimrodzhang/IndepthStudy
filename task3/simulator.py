# coding: utf-8
import json
import random
import time
import datetime
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['your_kafka_broker_1:9092','your_kafka_broker_2:9092'])

types = ['Online Shopping', 'Dining', 'Grocery', 'Offline Shopping']
places = ['us', 'us', 'us', 'us', 'us', 'us', 'us', 'us', 'us', 'cn']


for cnt in range(3000):
    account = 'Account_' + str(random.randint(0,100))
    amount = random.randint(1,1200)
    stype = types[random.randint(0,3)]
    place = places[random.randint(0,9)]
    ntime = time.time()
    dtime = datetime.datetime.fromtimestamp(ntime).strftime('%Y-%m-%d %H:%M:%S')


    data = {
        'requestID': str(ntime),
        'account': account,
        'timestamp': dtime,
        'amount': amount,
        'type': stype,
        'place': place
    }

    message = json.dumps(data)

    producer.send('RawRequest', message.encode('utf8'))
    time.sleep(0.05)
    # producer.send('sex',line[9].encode('utf8'))

producer.flush()
producer.close()
