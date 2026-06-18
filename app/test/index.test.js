const request = require('supertest');
const app = require('../app');

describe('Backend Test', () => {

  test('GET / debe renderizar el dashboard', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.headers['content-type']).toMatch(/html/);
    expect(res.text).toContain('Secure CI/CD AI Pipeline');
    expect(res.text).toContain('Flujo protegido');
  });

  test('GET /health debe responder ok', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  test('GET /api/status debe exponer el estado del proyecto', async () => {
    const res = await request(app).get('/api/status');
    expect(res.statusCode).toBe(200);
    expect(res.body.project).toBe('Secure CI/CD AI Pipeline');
    expect(res.body.model.accuracy).toBe(0.8268);
    expect(res.body.pipeline).toHaveLength(7);
  });

});
