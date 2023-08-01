# diagram.py
from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.aws.analytics import ElasticsearchService, ES
from diagrams.aws.compute import EC2, ECS, EKS, Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import Eventbridge, SQS
from diagrams.aws.iot import IotCore, IotDeviceDefender
from diagrams.aws.management import Cloudwatch
from diagrams.aws.mobile import APIGateway
from diagrams.aws.storage import Backup, S3
from diagrams.onprem.monitoring import Grafana, Prometheus, Nagios

with Diagram("Main", show=False):
    # Definitions
    api_gateway = APIGateway("API Gateway")
    iot = IotCore("IOT Core")
    iot_device_defender = IotDeviceDefender("IOT Device Defender")
    instance = EC2("EC2")
    lambda_events = Lambda("Lambda Events")
    grafana = Grafana("Grafana")
    opensearch = ES("Opensearch")
    event_bridge = Eventbridge("EventBridge")
    dynamo = Dynamodb("DynamoDB")
    devo = Custom("Devo", "./resources/devo.png")

    # Lambda
    iot >> SQS("SQS") >> instance
    iot >> lambda_events >> instance
    iot >> dynamo

    event_bridge >> lambda_events
    lambda_events >> opensearch
    lambda_events >> dynamo

    instance >> api_gateway

    # DBs & Storage
    instance >> RDS("RDS")
    instance >> dynamo
    instance >> S3("S3 Files") >> Backup("Backup S3")

    # Logs
    instance >> devo

    # Monitoring
    instance >> Nagios("nagios")
    instance >> Prometheus("Prometheus") >> grafana
    instance >> Cloudwatch("Cloudwatch") >> grafana
    instance >> opensearch >> grafana
