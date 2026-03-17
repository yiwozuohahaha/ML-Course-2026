from kafka import KafkaConsumer
import pymysql
import json

# 配置信息
KAFKA_TOPIC = 'greenhouse_topic'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'greenhouse_db'
}

# 1. 连接 MySQL
db = pymysql.connect(**MYSQL_CONFIG)
cursor = db.cursor()

# 2. 配置 Kafka 消费者
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

print("正在等待 Kafka 消息入库...")

try:
    for message in consumer:
        data = message.value

        # 3. 写入 MySQL
        sql = """INSERT INTO sensor_data (device_id, ts, temperature, humidity, soil_moisture, lux)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            data['device_id'], data['ts'], data['temperature'],
            data['humidity'], data['soil_moisture'], data['lux']
        ))
        db.commit()
        print(f"数据已从 Kafka 存入 MySQL: {data['ts']}")

except KeyboardInterrupt:
    db.close()