## Building and Pushing Docker Image for AWS Lambda Deployment

This section outlines the steps to build a Docker image for your high-performance AI application, specifically for deployment as an AWS Lambda function, and then push this image to your AWS Elastic Container Registry (ECR) repository.

1.  **Build the Docker Image:**

    Navigate to the root directory of your project, which contains your `Dockerfile`. Then, execute the following Docker command to build the image. We'll tag it with a local name for easier reference:

    ```bash
    docker build -t yolov8-lambda .
    ```

    -   `docker build`: This is the Docker command to build an image from a `Dockerfile`.
    -   `-t yolov8-lambda`: This flag tags your newly built image with the name `yolov8-lambda`. You can choose a different name if you prefer.
    -   `.`: The dot specifies that the build context (the set of files and directories accessible during the build) is the current directory.

2.  **Create an AWS ECR Repository (if it doesn't exist):**

    Before you can push your Docker image to ECR, you need to have a repository in your AWS account. If you haven't created one yet, use the following AWS CLI command. **Replace `<ecr-repository-name>` with your desired repository name (e.g., `mlops-anpr-lambda`).**

    ```bash
    aws ecr create-repository --repository-name <ecr-repository-name>
    ```

    If the repository already exists, you can skip this step. Take note of the `repositoryUri` in the output of this command, as you'll need it in subsequent steps.

3.  **Authenticate Docker with AWS ECR:**

    To push Docker images to your ECR repository, you need to authenticate your Docker client with your AWS account. Use the following command to retrieve a temporary password and log in:

    ```bash
    aws ecr get-login-password --region <your-aws-region> | docker login --username AWS --password-stdin <your-ecr-url>
    ```

    -   `aws ecr get-login-password --region <your-aws-region>`: This AWS CLI command retrieves an authentication token (password) for your specified AWS region. **Replace `<your-aws-region>` with your AWS region (e.g., `us-east-1`, `ap-south-1`).**
    -   `| docker login --username AWS --password-stdin <your-ecr-url>`: This part pipes the retrieved password to the `docker login` command. **Replace `<your-ecr-url>` with the full URI of your ECR repository (e.g., `123456789012.dkr.ecr.us-east-1.amazonaws.com`).** You can find this URI in the output of the `aws ecr create-repository` command or by listing your repositories using `aws ecr describe-repositories`.

    A successful login will typically output a "Login Succeeded" message.

4.  **Tag the Docker Image with the ECR Repository URI:**

    Before pushing, you need to tag your local Docker image with the specific URI of your ECR repository. This tells Docker where to push the image. Use the following command, **replacing `<your-ecr-url>` with your ECR repository URI**:

    ```bash
    docker tag yolov8-lambda <your-ecr-url>/yolov8-lambda
    ```

    This command creates an additional tag for your `yolov8-lambda` image, associating it with your ECR repository.

5.  **Push the Docker Image to AWS ECR:**

    Finally, you can push your tagged Docker image to your ECR repository using the following command. **Ensure you replace `<your-ecr-url>` with your ECR repository URI**:

    ```bash
    docker push <your-ecr-url>/yolov8-lambda
    ```

    This command uploads your Docker image to the specified ECR repository in your AWS account. Once the push is complete, you can use this image when configuring your AWS Lambda function to be container image based.
