const { dashboardStatus } = require('../config');

const setupRoutes = (app) => {
  // API Routes
  app.get('/api/status', (req, res) => {
    res.json(dashboardStatus);
  });

  app.get('/health', (req, res) => {
    res.json({
      status: 'ok',
      service: 'secure-ci-cd-dashboard'
    });
  });
};

module.exports = { setupRoutes };
