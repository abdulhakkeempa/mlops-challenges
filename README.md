# An Empirical Study of MLOps Challenges in Deploying High-Performance AI Applications on Cloud Infrastructure
This repository contains my work for S8 project at Cochin University of Science and Technology as a part of my course work.

The goal of this research study was to identify the MLOps challenges in deploying high performance AI applications in Cloud and find a good architecture in terms of scalability, latency and cost.

## Methodology
For this project, we took the ANPR task, since it is a high workload application. We trained the YoloV8 model of 3 different variants (Nano, Small & Medium) on the same dataset and deployed the model on 4 different cloud architectures to measure the efficiency.

## Building API
The next step was to build an API following microservices standard. 

For this purpose, FastAPI was used to build the API wrapper for the model.

## Deployment
For deployment, we had proposed 4 cloud architectures,

For the entire research we have used AWS as the cloud infrastructure.

### Proposed Architectures
- AWS EC2
- AWS Lambda
- AWS Fargate
- AWS EC2 + ECS

### Evaluation Metrics
- Average Latency
- Latency (50th Percentile)
- Latency (90th Percentile)
- Latency (99th Percentile)
- Throughput
- Success Rate
- Failure Rate
- Cold Start Latency (For Serverless Architectures)
- CPU Utilization
- Memory Utilization
- Cost

