"""
Streaming data consumer for Airflow DAG
"""
from datetime import datetime
from kafka import KafkaConsumer
import mysql.connector

TOPIC = 'vehicles'
DATABASE = 'tolldata'
USERNAME = 'root'
PASSWORD = 'zF4PAiJvletQsnQwe2P6Jc5C'

def consume_kafka_messages(max_messages=100):
    print("Connecting to the database...")
    try:
        connection = mysql.connector.connect(host='mysql', database=DATABASE, user=USERNAME, password=PASSWORD)
        cursor = connection.cursor()
        print("Connected to database.")

        print("Connecting to Kafka...")
        consumer = KafkaConsumer(TOPIC, bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
        print("Connected to Kafka.")

        count = 0
        for msg in consumer:
            if count >= max_messages:
                break

            message = msg.value.decode("utf-8")
            timestamp, vehicle_id, vehicle_type, plaza_id = message.split(",")

            dateobj = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
            timestamp = dateobj.strftime("%Y-%m-%d %H:%M:%S")

            sql = "INSERT INTO livetolldata VALUES(%s, %s, %s, %s)"
            cursor.execute(sql, (timestamp, vehicle_id, vehicle_type, plaza_id))
            print(f"A {vehicle_type} was inserted into the database")
            connection.commit()
            count += 1

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()
        consumer.close()

if __name__ == "__main__":
    consume_kafka_messages()
