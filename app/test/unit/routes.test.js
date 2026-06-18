const express = require('express');
const request = require('supertest');
const { setupRoutes } = require('../../routes');
const { dashboardStatus } = require('../../config');

describe('setupRoutes', () => {
  let app;

  beforeEach(() => {
    app = express();
    app.use(express.json());
    setupRoutes(app);
  });

  test('debe registrar la ruta /api/status', async () => {
    const response = await request(app).get('/api/status');
    expect(response.status).toBe(200);
    expect(response.body).toEqual(dashboardStatus);
  });

  test('debe registrar la ruta /health', async () => {
    const response = await request(app).get('/health');
    expect(response.status).toBe(200);
    expect(response.body).toEqual({
      status: 'ok',
      service: 'secure-ci-cd-dashboard'
    });
  });

  test('debe tener GET method para /api/status', async () => {
    const response = await request(app).get('/api/status');
    expect(response.status).toBe(200);
  });

  test('debe tener GET method para /health', async () => {
    const response = await request(app).get('/health');
    expect(response.status).toBe(200);
  });
});
