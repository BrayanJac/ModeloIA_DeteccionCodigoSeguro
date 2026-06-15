const express = require('express');
const app = express();

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Backend funcionando');
});

app.get('/health', (req, res) => {
  res.json({
    status: 'ok'
  });
});

module.exports = app;