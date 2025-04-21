const fs = require('fs');
const path = require('path');
const FormData = require('form-data');
const axios = require('axios');

module.exports = {
  uploadImage: async function (context, events, done) {
    const filePath = path.resolve(__dirname, 'car.jpg');
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));

    try {
      const response = await axios.post(
        'http://localhost:8000/detect',
        form,
        {
          headers: form.getHeaders(),
          timeout: 30000
        }
      );
      // console.log('✅ Success:', response.status, response.data);
    } catch (error) {
      console.error('❌ Error:', error.response?.status, error.response?.data || error.message);
    }
  }
};