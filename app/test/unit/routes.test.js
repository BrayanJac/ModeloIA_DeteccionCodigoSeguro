const express = require('express');
const { setupRoutes } = require('../../routes');
const { dashboardStatus } = require('../../config');

describe('setupRoutes', () => {
  let app;

  beforeEach(() => {
    app = express();
    app.use(express.json());
    setupRoutes(app);
  });

  test('debe registrar la ruta /api/status', () => {
    const routes = app._router.stack
      .filter(layer => layer.route)
      .map(layer => layer.route.path);
    
    expect(routes).toContain('/api/status');
  });

  test('debe registrar la ruta /health', () => {
    const routes = app._router.stack
      .filter(layer => layer.route)
      .map(layer => layer.route.path);
    
    expect(routes).toContain('/health');
  });

  test('debe tener GET method para /api/status', () => {
    const route = app._router.stack
      .find(layer => layer.route && layer.route.path === '/api/status');
    
    expect(route).toBeDefined();
    expect(route.route.methods.get).toBe(true);
  });

  test('debe tener GET method para /health', () => {
    const route = app._router.stack
      .find(layer => layer.route && layer.route.path === '/health');
    
    expect(route).toBeDefined();
    expect(route.route.methods.get).toBe(true);
  });
});
