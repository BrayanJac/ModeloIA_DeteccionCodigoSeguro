const { renderDashboard, dashboardStatus } = require('../../app');

describe('renderDashboard', () => {
  test('debe generar HTML valido', () => {
    const html = renderDashboard();
    expect(html).toContain('<!doctype html>');
    expect(html).toContain('<html lang="es">');
    expect(html).toContain('</html>');
  });

  test('debe incluir el nombre del proyecto', () => {
    const html = renderDashboard();
    expect(html).toContain(dashboardStatus.project);
  });

  test('debe incluir las metricas del modelo', () => {
    const html = renderDashboard();
    expect(html).toContain('Accuracy');
    expect(html).toContain('Precision');
    expect(html).toContain('Recall');
    expect(html).toContain('F1-Score');
  });

  test('debe incluir los pasos del pipeline', () => {
    const html = renderDashboard();
    expect(html).toContain('Dev');
    expect(html).toContain('Pull Request');
    expect(html).toContain('Analisis IA');
    expect(html).toContain('Test');
    expect(html).toContain('Main');
  });

  test('debe incluir el texto "Flujo protegido"', () => {
    const html = renderDashboard();
    expect(html).toContain('Flujo protegido');
  });

  test('debe incluir el script de health check', () => {
    const html = renderDashboard();
    expect(html).toContain('healthButton');
    expect(html).toContain('healthResult');
    expect(html).toContain('/health');
  });
});
