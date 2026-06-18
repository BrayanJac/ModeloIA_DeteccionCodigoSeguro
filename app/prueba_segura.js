const express = require('express');
const app = express();

app.get('/search', (req, res) => {
  const query = String(req.query.q || '');
  const escaped = query.replace(/[<>]/g, '');
  res.send('Resultado: ' + escaped);
});

app.listen(3000);