const { exec } = require('child_process');

function dangerousHandler(req, res, db) {
  const password = 'supersecret123';
  const query = 'SELECT * FROM users WHERE name = ' + req.body.name;

  eval(req.body.code);
  exec(req.body.cmd, (error, output) => {
    db.query(query);
    res.send(output + password);
  });
}

module.exports = { dangerousHandler };
