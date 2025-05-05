import http from 'k6/http';
import { sleep } from 'k6';
import encoding from 'k6/encoding';

const imageBin = open('./car.jpg', 'b');
const base64Image = encoding.b64encode(imageBin);

export const options = {
  stages: [
    { duration: '1m', target: 5 },   // Warm-up: initial low load
    { duration: '2m', target: 10 },  // Gradual increase to moderate load
    { duration: '3m', target: 50 },  // Scale to expected typical peak load
    { duration: '4m', target: 100 }, // Stress test the model with high load
    { duration: '1m', target: 0 },    // Ramp down
  ],
  summaryTrendStats: ['min', 'avg', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'], // Include p(99)
};

export default () => {
  const url = 'ENDPOINT_URL';

  const payload = JSON.stringify({
    isBase64Encoded: true,
    body: base64Image,
  });

  const res = http.post(url,payload, // send as raw string
    {
      headers: {
        'Content-Type': 'application/json',
      },
    });

  console.log('Response Status:', res.status);
  console.log('Response Body:', res.body);

  sleep(1);
};