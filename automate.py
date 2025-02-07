from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mysql.connector
from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 6),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

db_config = {
    "host": "mysql",
    "database": "tolldata",
    "user": "root",
    "password": "zF4PAiJvletQsnQwe2P6Jc5C",
}

TOPIC = "vehicles"

def create_kafka_topic():
    """Create Kafka topic if it doesn't exist."""
    admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')
    topics = admin_client.list_topics()
    if TOPIC not in topics:
        topic = NewTopic(name=TOPIC, num_partitions=1, replication_factor=1)
        admin_client.create_topics([topic])
        print(f"Topic {TOPIC} created.")
    else:
        print(f"Topic {TOPIC} already exists.")

def check_mysql_data():
    """Verify data ingestion by checking MySQL table."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM livetolldata")
    count = cursor.fetchone()[0]
    print(f"Total records in livetolldata: {count}")
    connection.close()

with DAG(
    'kafka_airflow_pipeline',
    default_args=default_args,
    schedule_interval=None,  # Trigger manually
    catchup=False,
) as dag:
    
    start_kafka = BashOperator(
        task_id='start_kafka',
        bash_command='cd kafka_2.12-3.7.0 && bin/kafka-server-start.sh -daemon config/kraft/server.properties',
    )

    create_topic = PythonOperator(
        task_id='create_kafka_topic',
        python_callable=create_kafka_topic,
    )

    run_traffic_generator = BashOperator(
        task_id='run_traffic_generator',
        bash_command='python3 toll_traffic_generator.py',
    )

    start_consumer = BashOperator(
        task_id='start_consumer',
        bash_command='python3 streaming-data-reader.py',
    )

    verify_data = PythonOperator(
        task_id='verify_data',
        python_callable=check_mysql_data,
    )

    start_kafka >> create_topic >> run_traffic_generator >> start_consumer >> verify_data
