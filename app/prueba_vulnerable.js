const express = require('express');
const app = express();

app.get('/search', (req, res) => {
  const query = req.query.q;
  const result = eval(query);
  res.send('Resultado: ' + result);
});

app.listen(3000);