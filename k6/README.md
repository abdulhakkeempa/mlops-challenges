## Running Load Tests with Grafana k6

To execute load tests against your deployed API endpoints using Grafana k6, follow these steps:

1.  **Pull the k6 Docker Image:**

    Begin by ensuring you have the k6 Docker image on your local machine. Open your terminal and run the following command:

    ```bash
    docker pull grafana/k6
    ```

    This command will download the latest k6 image from Docker Hub if it's not already present.

2.  **Define Your Load Test Configuration:**

    Next, you need to define the parameters of your load test in a JavaScript file. Create a file named `load-test.js` (or any name you prefer with a `.js` extension) in your project directory. This file will contain the test сценарио, including the number of virtual users, duration, and the API endpoints to target.

    **Example `load-test.js`:**

    ```javascript
    import http from 'k6/http';
    import { sleep } from 'k6';

    export const options = {
      stages: [
        { duration: '1m', target: 5 },   // Warm-up: 1 minute, starting with 5 virtual users
        { duration: '2m', target: 10 },  // Ramp-up: 2 minutes, increasing to 10 virtual users
        { duration: '3m', target: 50 },  // Peak Load: 3 minutes at 50 virtual users
        { duration: '4m', target: 100 }, // Stress Test: 4 minutes at 100 virtual users
        { duration: '1m', target: 0 },   // Ramp-down: 1 minute, decreasing to 0 virtual users
      ],
    };

    export default function () {
      const res = http.get('YOUR_API_ENDPOINT_HERE'); // Replace with your actual API endpoint
      // You can add more requests and assertions here
      sleep(1); // Add a small pause between iterations
    }
    ```

    **Remember to replace `'YOUR_API_ENDPOINT_HERE'` with the actual URL of the API endpoint you want to test.** You can customize the `options` section to define different load patterns and add more complex test logic within the `default` function.

3.  **Run the Load Test:**

    Once your `load-test.js` file is configured, you can execute the load test using the k6 Docker container. Navigate to the directory containing your `load-test.js` file in your terminal and run the following command:

    ```bash
    docker run --rm -i -v ${PWD}:/app -w /app grafana/k6 run -o json=/app/fargate_result.json /app/load-test.js
    ```

    Let's break down this command:

    -   `docker run`: This is the standard Docker command to run a container.
    -   `--rm`: This flag automatically removes the container once it finishes execution, keeping your system clean.
    -   `-i`: This flag keeps STDIN open even if not attached, which is useful for interactive processes (though less so in this specific command).
    -   `-v ${PWD}:/app`: This is a volume mount. `${PWD}` represents your current working directory on the host machine, and it's being mounted to the `/app` directory inside the Docker container. This allows the k6 container to access your `load-test.js` file.
    -   `-w /app`: This sets the working directory inside the Docker container to `/app`, so k6 can directly find your test script.
    -   `grafana/k6`: This specifies the Docker image to use (the k6 image you pulled earlier).
    -   `run`: This is the k6 command to execute a test script.
    -   `-o json=/app/fargate_result.json`: This flag tells k6 to output the test results in JSON format to a file named `fargate_result.json` within
