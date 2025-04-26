import base64
import requests
import time
import threading
from collections import deque
import numpy as np

# Configuration
url = "ENDPOINT_URL"
image_path = "car.jpg"
total_requests = 3000
ramp_up_duration = 10
num_threads_at_peak = 20

# Calculate the delay between starting threads
if num_threads_at_peak > 0:
    thread_start_delay = ramp_up_duration / num_threads_at_peak
else:
    thread_start_delay = 0

# Read and encode the image once
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

payload = {
    "isBase64Encoded": True,
    "body": encoded_string
}
headers = {'Content-Type': 'application/json'}

request_latencies = deque()
successful_requests = 0
failed_requests = 0

def send_request(request_id):
    global successful_requests, failed_requests
    start_time = time.time()
    try:
        response = requests.post(url, json=payload, headers=headers)
        end_time = time.time()
        duration = end_time - start_time
        request_latencies.append(duration)
        print(f"Thread {threading.get_ident()} - Request {request_id}: Duration: {duration:.4f} seconds: Output: {response.text}")
        if response.status_code == 200:
            successful_requests += 1
            # Optionally print success details
            # print(f"Thread {threading.get_ident()} - Request {request_id}: Success, Duration: {duration:.4f} seconds")
        else:
            failed_requests += 1
            print(f"Thread {threading.get_ident()} - Request {request_id}: Failed with status {response.status_code}, Duration: {duration:.4f} seconds, Response: {response.text}")

    except requests.exceptions.RequestException as e:
        failed_requests += 1
        end_time = time.time()
        duration = end_time - start_time
        request_latencies.append(duration)
        print(f"Thread {threading.get_ident()} - Request {request_id} failed: {e}, Duration: {duration:.4f} seconds")

def main():
    threads = []
    requests_sent = 0
    start_time = time.time()

    while requests_sent < total_requests:
        if threading.active_count() - threading.main_thread().daemon < num_threads_at_peak:
            thread = threading.Thread(target=send_request, args=(requests_sent + 1,))
            threads.append(thread)
            thread.start()
            requests_sent += 1
            time.sleep(thread_start_delay)
        else:
            time.sleep(0.1)

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_duration = end_time - start_time
    throughput = successful_requests / total_duration if total_duration > 0 else 0

    latencies_array = np.array(list(request_latencies))

    avg_latency = np.mean(latencies_array) if latencies_array.size > 0 else 0
    latency_50 = np.percentile(latencies_array, 50) if latencies_array.size > 0 else 0
    latency_90 = np.percentile(latencies_array, 90) if latencies_array.size > 0 else 0
    latency_99 = np.percentile(latencies_array, 99) if latencies_array.size > 0 else 0

    print(f"\n--- Load Test Results ---")
    print(f"Total Requests Sent: {total_requests}")
    print(f"Successful Requests: {successful_requests}")
    print(f"Failed Requests: {failed_requests}")
    print(f"Throughput: {throughput:.2f} requests/second")
    print(f"Latency Average: {avg_latency:.4f} seconds")
    print(f"Latency 50th Percentile (p50): {latency_50:.4f} seconds")
    print(f"Latency 90th Percentile (p90): {latency_90:.4f} seconds")
    print(f"Latency 99th Percentile (p99): {latency_99:.4f} seconds")
    print(f"Ramp-up Duration: {ramp_up_duration:.2f} seconds")
    print(f"Peak Concurrency: {num_threads_at_peak} threads")
    print(f"Total Test Duration: {total_duration:.2f} seconds")

if __name__ == "__main__":
    main()