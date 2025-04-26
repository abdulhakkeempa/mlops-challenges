import http from 'k6/http';
import { sleep } from 'k6';

const imageBin = open('./car.jpg', 'b');

export const options = {
  stages: [
    { duration: '1m', target: 5 },   // Warm-up: initial low load
    { duration: '2m', target: 10 },   // Gradual increase to moderate load
    { duration: '3m', target: 50 },  // Scale to expected typical peak load
    { duration: '4m', target: 100 },  // Stress test the model with high load
    { duration: '1m', target: 0 },    // Ramp down
  ],
  summaryTrendStats: ['min', 'avg', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'], // Include p(99)
};


export default () => {
  const url = 'ENDPOINT_URL';

  const payload = {
    file: http.file(imageBin, 'car.jpg', 'image/jpeg'),
  };

  const res = http.post(url, payload);
  sleep(1);

};