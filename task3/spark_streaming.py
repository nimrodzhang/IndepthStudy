
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition

import boto3, json

sc = SparkContext(appName="streamingkafka")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 20)

brokers='your_kafka_broker_1:9092,your_kafka_broker_2:9092'
topic = 'TransDetail'

partition = 0
start = 0
topicpartion = TopicAndPartition(topic, partition)
fromoffset = {topicpartion: int(start)}

lines = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers}, fromOffsets = fromoffset)

def todb(x):
        x = x[1]

        print(x)

        session = boto3.Session(aws_access_key_id='Your_id', aws_secret_access_key='Your_key')

        dynamodb = session.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('new_details')

        dbdict = json.loads(x)
        dbdict["timestamp"] = str(dbdict["timestamp"])

        table.put_item(Item=dbdict)

        return (dbdict["account"], dbdict["requestID"]), dbdict["amount"]

statistic = lines.map(todb).reduceByKey(lambda x, y: x).map(lambda x: (x[0][0], x[1])).reduceByKey(lambda x, y: x+y)

statistic.pprint()
