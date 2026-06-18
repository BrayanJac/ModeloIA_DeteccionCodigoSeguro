const request = require('supertest');
const app = require('../../app');

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

  test('GET /ruta-inexistente debe retornar 404', async () => {
    const res = await request(app).get('/ruta-inexistente');
    expect(res.statusCode).toBe(404);
  });

  test('GET /api/status debe tener estructura JSON valida', async () => {
    const res = await request(app).get('/api/status');
    expect(res.statusCode).toBe(200);
    expect(res.headers['content-type']).toMatch(/json/);
    expect(res.body).toHaveProperty('project');
    expect(res.body).toHaveProperty('environment');
    expect(res.body).toHaveProperty('model');
    expect(res.body).toHaveProperty('pipeline');
    expect(res.body).toHaveProperty('protections');
    expect(res.body).toHaveProperty('evidence');
  });

  test('GET /health debe tener estructura correcta', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('status');
    expect(res.body).toHaveProperty('service');
    expect(res.body.status).toBe('ok');
    expect(res.body.service).toBe('secure-ci-cd-dashboard');
  });

  test('POST / debe retornar 404 (metodo no permitido)', async () => {
    const res = await request(app).post('/');
    expect(res.statusCode).toBe(404);
  });

  test('POST /api/status debe retornar 404 (metodo no permitido)', async () => {
    const res = await request(app).post('/api/status');
    expect(res.statusCode).toBe(404);
  });

  test('GET / debe tener contenido HTML valido', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.text).toMatch(/<!doctype html>/i);
    expect(res.text).toMatch(/<html/i);
    expect(res.text).toMatch(/<\/html>/);
  });

  test('GET / debe incluir CSS en linea', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.text).toContain('<style>');
    expect(res.text).toContain('</style>');
  });

  test('GET / debe incluir JavaScript del cliente', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.text).toContain('<script>');
    expect(res.text).toContain('</script>');
    expect(res.text).toContain('healthButton');
  });

});
