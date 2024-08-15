# Streaming-ETL-Pipeline-using-Kafka
This is a project that aims to de-congest the national highways by analyzing the road traffic data from different toll plazas. As a vehicle passes a toll plaza, the vehicle's data like vehicle_id, vehicle_type, toll_plaza_id, and timestamp are streamed to Kafka. 

## Setup Instructions for Kafka

### 1. Navigate to the Kafka Directory

Change to the Kafka directory using the following command:

```bash
cd kafka_2.12-3.7.0
```
Generate a unique Cluster UUID for your Kafka cluster with this command:
```bash
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
```
Note: The new cluster ID generated will be used by the KRaft controller.

Configure the log directories by passing the cluster ID. Run the following command:
```bash
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
```
Start the Kafka server using the command below:
```bash
bin/kafka-server-start.sh config/kraft/server.properties
```
