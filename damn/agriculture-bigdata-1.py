import json
import time
import random
import math
from datetime import datetime
from paho.mqtt import client as mqtt_client

# MQTT 配置
BROKER = 'localhost'
PORT = 1883
TOPIC = "greenhouse/sensors"
CLIENT_ID = "sensor_01"

def on_connect(client, userdata, flags, rc):
    if rc == 0: print("Connected to MQTT Broker!")
    else: print(f"Failed to connect, code {rc}")

def generate_data(elapsed):
    # 保持之前设计的真实农业数据算法
    day_cycle = math.sin(elapsed / 3600 * math.pi / 12 - math.pi / 2)
    return {
        "device_id": "GH-01",
        "ts": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "temperature": round(24 + 6 * day_cycle + random.uniform(-0.3, 0.3), 2),
        "humidity": round(55 - 15 * day_cycle + random.uniform(-1, 1), 2),
        "soil_moisture": round(35 - (elapsed % 86400) / 10000, 2),
        "lux": int(max(0, 30000 * (day_cycle + 0.2))) if day_cycle > -0.2 else 0
    }

client = mqtt_client.Client(CLIENT_ID)
client.on_connect = on_connect
client.connect(BROKER, PORT)

start_time = time.time()
while True:
    data = generate_data(time.time() - start_time)
    client.publish(TOPIC, json.dumps(data))
    print(f"MQTT 发送成功: {data}")
    time.sleep(2)