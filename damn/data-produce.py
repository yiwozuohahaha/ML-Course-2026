import pymysql
import time
import random
import math
from datetime import datetime

# --- 数据库配置 ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # 你的数据库用户名
    'password': '123456yys',  # 你的数据库密码
    'database': 'greenhouse_db',
    'charset': 'utf8mb4'
}

# --- 模拟参数 ---
DEVICE_ID = "GH-001"
LOCATION = "North_Sector_A1"


def generate_record(elapsed):
    """生成符合大棚实际情况的模拟数据"""
    day_cycle = math.sin(elapsed / 3600 * math.pi / 12 - math.pi / 2)
    temp = 24 + 6 * day_cycle + random.uniform(-0.3, 0.3)
    hum = 55 - 15 * day_cycle + random.uniform(-1, 1)
    soil = 35 - (elapsed % 86400) / 10000 + random.uniform(-0.05, 0.05)
    lux = max(0, 30000 * (day_cycle + 0.2) + random.randint(-500, 500)) if day_cycle > -0.2 else 0

    return (
        DEVICE_ID,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        round(temp, 2),
        round(hum, 2),
        round(soil, 2),
        int(lux),
        LOCATION
    )


def main():
    # 连接数据库
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        print("成功连接到 MySQL 数据库")
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return

    start_time = time.time()
    sql = "INSERT INTO sensor_data (device_id, ts, temperature, humidity, soil_moisture, lux, location) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    try:
        while True:
            elapsed = time.time() - start_time
            data_tuple = generate_record(elapsed)

            # 执行插入
            cursor.execute(sql, data_tuple)
            connection.commit()  # 提交事务

            print(f"已存入数据库: {data_tuple[1]} | 温: {data_tuple[2]}°C")
            time.sleep(200)

    except KeyboardInterrupt:
        print("\n程序已停止")
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()