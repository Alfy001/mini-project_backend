const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();
const port = 4000; // Node.js server port
const pythonServerUrl = 'http://192.168.121.3:6547'; // Python server URL

// Middleware to parse JSON and URL-encoded data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Proxy GET request to Python server with logging
app.get('/hr', async (req, res) => {
    try {
        console.log('Fetching heart rate from Python server...');
        const response = await axios.get(`${pythonServerUrl}/hr`);
        
        // Parse the response as a string and convert to a number
        const hr = parseInt(response.data, 10);
        
        // Validate the heart rate value
        if (isNaN(hr) || hr < 0) {
            throw new Error('Invalid heart rate value received from Python server');
        }
        
        console.log('Heart rate data:', hr);
        res.send(hr.toString()); // Send the heart rate as a string
    } catch (err) {
        console.error('Error fetching heart rate:', err.message);
        console.error('Error details:', err.response ? err.response.data : 'No response data');
        res.status(500).send('Error fetching heart rate');
    }
});
// Proxy POST request to Python server
app.post('/hr', async (req, res) => {
    try {
        const response = await axios.post(`${pythonServerUrl}/`, `bpm=${req.body.bpm}`);
        res.send(response.data);
    } catch (err) {
        res.status(500).send('Error updating heart rate');
    }
});

// Serve static files (e.g., React build files)
app.use(express.static(path.join(__dirname, 'public')));

// Start the Node.js server
app.listen(port, () => {
    console.log(`Node.js server running at http://192.168.121.3:${port}`);
});