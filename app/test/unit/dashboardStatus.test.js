const { dashboardStatus } = require('../../config');

describe('dashboardStatus', () => {
  test('debe tener la estructura correcta', () => {
    expect(dashboardStatus).toHaveProperty('project');
    expect(dashboardStatus).toHaveProperty('environment');
    expect(dashboardStatus).toHaveProperty('model');
    expect(dashboardStatus).toHaveProperty('pipeline');
    expect(dashboardStatus).toHaveProperty('protections');
    expect(dashboardStatus).toHaveProperty('evidence');
  });

  test('debe tener valores validos en model', () => {
    expect(dashboardStatus.model).toHaveProperty('accuracy');
    expect(dashboardStatus.model).toHaveProperty('precision');
    expect(dashboardStatus.model).toHaveProperty('recall');
    expect(dashboardStatus.model).toHaveProperty('f1Score');
    expect(dashboardStatus.model).toHaveProperty('aucRoc');
    expect(dashboardStatus.model).toHaveProperty('featureCount');
    expect(dashboardStatus.model).toHaveProperty('latestFeature');

    expect(dashboardStatus.model.accuracy).toBeGreaterThan(0);
    expect(dashboardStatus.model.accuracy).toBeLessThanOrEqual(1);
    expect(dashboardStatus.model.featureCount).toBeGreaterThan(0);
  });

  test('debe tener 7 pasos en el pipeline', () => {
    expect(dashboardStatus.pipeline).toHaveLength(7);
    expect(dashboardStatus.pipeline[0]).toHaveProperty('name');
    expect(dashboardStatus.pipeline[0]).toHaveProperty('state');
    expect(dashboardStatus.pipeline[0]).toHaveProperty('status');
  });

  test('debe tener protecciones definidas', () => {
    expect(dashboardStatus.protections).toBeInstanceOf(Array);
    expect(dashboardStatus.protections.length).toBeGreaterThan(0);
  });

  test('debe tener evidencia con URLs validas', () => {
    expect(dashboardStatus.evidence).toHaveProperty('vulnerablePr');
    expect(dashboardStatus.evidence).toHaveProperty('vulnerableRun');
    expect(dashboardStatus.evidence).toHaveProperty('documentation');

    expect(dashboardStatus.evidence.vulnerablePr).toMatch(/^https?:\/\//);
    expect(dashboardStatus.evidence.vulnerableRun).toMatch(/^https?:\/\//);
  });
});
