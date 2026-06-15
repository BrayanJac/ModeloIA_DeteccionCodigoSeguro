const request = require('supertest');
const app = require('./app');

describe('Backend Test', () => {

  test('GET / debe responder', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.text).toBe('Backend funcionando');
  });

  test('GET /health debe responder ok', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
  });

});