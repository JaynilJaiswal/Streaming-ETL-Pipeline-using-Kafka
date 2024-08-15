# Streaming-ETL-Pipeline-using-Kafka
This is a project that aims to de-congest the national highways by analyzing the road traffic data from different toll plazas. As a vehicle passes a toll plaza, the vehicle's data like vehicle_id, vehicle_type, toll_plaza_id, and timestamp are streamed to Kafka. 

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

Open your terminal and connect to the MySQL server using the following command. Use the password provided when the MySQL server was initialized:

```bash
mysql --host=mysql --port=3306 --user=root --password=YourPasswordHere
```

### 2. Create a Database
At the `mysql>` prompt, execute the following command to create a new database named `tolldata`:
```bash
create database tolldata;
```

### 3. Create a Table
To create a table named `livetolldata` within the `tolldata` database, follow these steps:
#### 1. Switch to the `tolldata` database:
```bash
use tolldata;
```
#### 2. Create the `livetolldata` table with the specified schema:
```bash
create table livetolldata(
    timestamp datetime,
    vehicle_id int,
    vehicle_type char(15),
    toll_plaza_id smallint
);
```
### 4. Disconnect from the MySQL Server
To exit the MySQL server, use the command:
```bash
exit
```
## Kafka Data Streaming Instructions

### 1. Create a Kafka Topic
Create a Kafka topic named `toll`.

### 2. Download and Configure the Traffic Generator
Download the `toll_traffic_generator.py` script using the command below:

```bash
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/toll_traffic_generator.py
```
### 3. Run the Traffic Generator
Execute the traffic generator script with the following command:
```bash
python3 toll_traffic_generator.py
```

### 4. Download and Configure the Streaming Data Reader
Download the streaming-data-reader.py script using the command below:
```bash
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/vVxmU5uatDowvAIKRZrFjg/streaming-data-reader.py
```
Open `streaming-data-reader.py` in your editor and update the following details to connect to your MySQL server:
- TOPIC
- DATABASE
- USERNAME
- PASSWORD

### 5. Run the Streaming Data Reader
Execute the streaming data reader script with the following command:
```bash
python3 streaming-data-reader.py
```

### 6. Verify Data Storage
To verify that the streaming toll data is being stored correctly, open the MySQL CLI and list the top 10 rows in the `livetolldata` table:
```
SELECT * FROM livetolldata LIMIT 10;
```



