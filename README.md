# An Empirical Study of MLOps Challenges in Deploying High-Performance AI Applications on Cloud Infrastructure

This repository documents the work undertaken for my S8 project at Cochin University of Science and Technology, as part of my academic coursework.

The central objective of this research study was to identify the key MLOps challenges encountered when deploying high-performance AI applications in cloud environments. Furthermore, the study aimed to determine an optimal architectural approach considering crucial factors such as scalability, latency, and cost-efficiency.

## Methodology

To address these objectives, we focused on the Automatic Number Plate Recognition (ANPR) task, recognized for its demanding computational workload. We trained three distinct variants of the YoloV8 model (Nano, Small, and Medium) on the same dataset. Subsequently, these models were deployed across four different cloud architectures to rigorously evaluate their performance.

## Model Training

The initial three base models of the YoloV8 family underwent fine-tuning using a publicly available Number Plate Detection Dataset from Kaggle.

To assess the generalization capabilities of the fine-tuned models, they were evaluated on an unseen and challenging dataset known as the Chinese City Parking Dataset (CCPD). This dataset includes images captured under adverse conditions such as low light and poor image quality.

The results indicated that the fine-tuned models demonstrated robust performance in detecting license plates, even in the presence of challenging image conditions.

## Building the API

The subsequent phase involved developing an Application Programming Interface (API) adhering to microservices architectural principles.

For this purpose, FastAPI, a modern, high-performance web framework for building APIs with Python, was employed to create the API wrapper for the trained models.

## Deployment

For the deployment phase of this research, we proposed and implemented four distinct cloud architectures, all leveraging the Amazon Web Services (AWS) infrastructure.

### Proposed Architectures

- AWS EC2
- AWS Lambda
- AWS Fargate
- AWS EC2 + ECS

### Evaluation Metrics

The performance of each deployment architecture was evaluated based on the following key metrics:

- Average Latency
- Latency (50th Percentile)
- Latency (90th Percentile)
- Latency (99th Percentile)
- Throughput
- Success Rate
- Failure Rate
- Cold Start Latency (specifically for serverless architectures like AWS Lambda)
- CPU Utilization
- Memory Utilization
- Cost

### Deployment Strategy

To ensure a fair comparison across different architectures, a consistent underlying resource configuration of 2 vCPUs and 4GB of RAM was maintained wherever applicable.

#### AWS EC2

- The EC2 instance was provisioned and configured with the necessary software packages and dependencies.
- Gunicorn, a Python WSGI HTTP Server for Unix, was utilized in conjunction with Uvicorn, an ASGI server, to serve the FastAPI application using 4 worker processes.
- Nginx was implemented as a reverse proxy server to handle load balancing and efficiently route incoming requests to the Gunicorn application.

#### AWS Lambda

- A custom function was developed in the AWS Lambda format to execute the model inference logic.
- Typically, Lambda functions are deployed using either a ZIP file or a Docker image. In this case, the deployment package size exceeded the 250MB limit for ZIP files. Consequently, a Docker image containing the application code and required packages was built.
- This Docker image was then pushed to AWS Elastic Container Registry (ECR).
- The Lambda function was subsequently created using the Docker image stored in ECR. The trained model files were fetched from an AWS S3 bucket during function invocation.

#### AWS Fargate

- The application code, its dependencies, and the trained model files were containerized into a Docker image using a Dockerfile.
- This Docker image was then stored in AWS Elastic Container Registry (ECR).
- Finally, the Docker image was pulled from ECR and deployed to a cluster managed by AWS Elastic Container Service (ECS).
- Auto Scaling was enabled through the Application Load Balancer to dynamically adjust the number of running tasks based on the incoming request volume.

#### AWS EC2 with ECS

- In this architecture, EC2 instances served as the underlying compute infrastructure for running containerized applications managed by ECS.
- Unlike AWS Fargate, where the underlying infrastructure is abstracted, with the EC2 launch type, the responsibility for provisioning, scaling, and maintaining the EC2 instances lies with the user.
- Similar to the Fargate deployment, the application code, dependencies, and model files were packaged into a Docker image using a Dockerfile and stored in AWS ECR. The ECS service then pulled this image to deploy it onto the EC2 instances registered within the ECS cluster.
- Auto Scaling was also configured in this setup to manage the number of EC2 instances based on demand.

### Performance Evaluation

To thoroughly evaluate the performance of the deployed API endpoints under varying loads, we employed k6, an open-source load testing tool developed by Grafana.

#### k6 Load Configuration

The load testing strategy involved a series of phases designed to simulate different traffic conditions:

- **Warm-up (1 min, 5 users):** Initiating the test with a low number of virtual users to allow the system to stabilize.
- **Ramp-up to Moderate Load (2 min, 10 users):** Gradually increasing the number of concurrent users to simulate increasing traffic.
- **Peak Load Simulation (3 min, 50 users):** Reaching a typical peak traffic level to assess performance under normal high load.
- **Stress Test (4 min, 100 users):** Pushing the system beyond its expected capacity to identify breaking points and performance bottlenecks.
- **Ramp-down (1 min, 0 users):** Gradually decreasing the load to conclude the test gracefully.
