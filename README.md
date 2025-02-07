# Streaming-ETL-Pipeline-using-Kafka with Airflow Automation

This project aims to decongest national highways by analyzing road traffic data from different toll plazas. As a vehicle passes a toll plaza, its data (vehicle_id, vehicle_type, toll_plaza_id, and timestamp) is streamed to Kafka and processed in parallel using multithreading for high efficiency. Apache Airflow is used to automate the ETL workflow.

## Key Features
- **Real-time Traffic Data Streaming**: Uses Kafka for vehicle data ingestion.
- **Multithreaded Processing**: Optimized for handling 1 million records efficiently.
- **Automated ETL Pipeline**: Apache Airflow orchestrates data extraction, transformation, and loading.

## Setup Instructions for Kafka

### 1. Navigate to the Kafka Directory
Change to the Kafka directory using the following command:
```bash
cd kafka_2.12-3.7.0
```

### 2. Generate a Cluster UUID
Generate a unique Cluster UUID for your Kafka cluster with this command:
```bash
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
```
Note: The new cluster ID generated will be used by the KRaft controller.

### 3. Configure Log Directories for KRaft
Configure the log directories by passing the cluster ID. Run the following command:
```bash
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
```

### 4. Start the Kafka Server
Start the Kafka server using the command below:
```bash
bin/kafka-server-start.sh config/kraft/server.properties
```

## MySQL Server Setup Instructions

### 1. Connect to the MySQL Server
Open your terminal and connect to the MySQL server using the following command:
```bash
mysql --host=mysql --port=3306 --user=root --password=YourPasswordHere
```

### 2. Create a Database
Create a new database named `tolldata`:
```bash
create database tolldata;
```

### 3. Create a Table
Switch to the `tolldata` database:
```bash
use tolldata;
```
Create the `livetolldata` table:
```bash
create table livetolldata(
    timestamp datetime,
    vehicle_id int,
    vehicle_type char(15),
    toll_plaza_id smallint
);
```

## Kafka Data Streaming Instructions

### 1. Create a Kafka Topic
Create a Kafka topic named `toll`.

### 2. Download and Configure the Multithreaded Traffic Generator
Download the updated `toll_traffic_generator.py` script:
```bash
wget https://your-updated-url/toll_traffic_generator.py
```
Run the script to generate and send 1 million records efficiently:
```bash
python3 toll_traffic_generator.py
```

### 3. Download and Configure the Streaming Data Reader
Download the `streaming-data-reader.py` script:
```bash
wget https://your-updated-url/streaming-data-reader.py
```
Update `streaming-data-reader.py` to connect to MySQL:
- TOPIC
- DATABASE
- USERNAME
- PASSWORD

Run the script for concurrent data processing:
```bash
python3 streaming-data-reader.py
```

### 4. Verify Data Storage
Check the first 10 rows in MySQL:
```bash
SELECT * FROM livetolldata LIMIT 10;
```

## Automating ETL with Airflow
### 1. Install and Start Airflow
```bash
pip install apache-airflow
export AIRFLOW_HOME=~/airflow
airflow db init
airflow webserver -p 8080 &
airflow scheduler &
```
### 2. Create an Airflow DAG
Define an ETL DAG to automate Kafka consumption and MySQL insertion.
Save it as `etl_dag.py` in `~/airflow/dags/`.

### 3. Trigger the DAG
Start the ETL pipeline:
```bash
airflow dags trigger kafka_etl_pipeline
```

This setup ensures that the pipeline efficiently processes large-scale streaming data while being fully automated with Airflow.

