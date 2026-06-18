const { dashboardStatus } = require('../../config');

describe('Validacion de datos', () => {
  describe('dashboardStatus.model', () => {
    test('accuracy debe estar entre 0 y 1', () => {
      expect(dashboardStatus.model.accuracy).toBeGreaterThanOrEqual(0);
      expect(dashboardStatus.model.accuracy).toBeLessThanOrEqual(1);
    });

    test('precision debe estar entre 0 y 1', () => {
      expect(dashboardStatus.model.precision).toBeGreaterThanOrEqual(0);
      expect(dashboardStatus.model.precision).toBeLessThanOrEqual(1);
    });

    test('recall debe estar entre 0 y 1', () => {
      expect(dashboardStatus.model.recall).toBeGreaterThanOrEqual(0);
      expect(dashboardStatus.model.recall).toBeLessThanOrEqual(1);
    });

    test('f1Score debe estar entre 0 y 1', () => {
      expect(dashboardStatus.model.f1Score).toBeGreaterThanOrEqual(0);
      expect(dashboardStatus.model.f1Score).toBeLessThanOrEqual(1);
    });

    test('aucRoc debe estar entre 0 y 1', () => {
      expect(dashboardStatus.model.aucRoc).toBeGreaterThanOrEqual(0);
      expect(dashboardStatus.model.aucRoc).toBeLessThanOrEqual(1);
    });

    test('featureCount debe ser un numero positivo', () => {
      expect(dashboardStatus.model.featureCount).toBeGreaterThan(0);
      expect(typeof dashboardStatus.model.featureCount).toBe('number');
    });

    test('latestFeature debe ser un string no vacio', () => {
      expect(typeof dashboardStatus.model.latestFeature).toBe('string');
      expect(dashboardStatus.model.latestFeature.length).toBeGreaterThan(0);
    });
  });

  describe('dashboardStatus.pipeline', () => {
    test('cada paso debe tener name, state y status', () => {
      dashboardStatus.pipeline.forEach(step => {
        expect(step).toHaveProperty('name');
        expect(step).toHaveProperty('state');
        expect(step).toHaveProperty('status');
        expect(typeof step.name).toBe('string');
        expect(typeof step.state).toBe('string');
        expect(typeof step.status).toBe('string');
      });
    });

    test('status debe ser ready o warning', () => {
      dashboardStatus.pipeline.forEach(step => {
        expect(['ready', 'warning']).toContain(step.status);
      });
    });

    test('name no debe estar vacio', () => {
      dashboardStatus.pipeline.forEach(step => {
        expect(step.name.length).toBeGreaterThan(0);
      });
    });
  });

  describe('dashboardStatus.protections', () => {
    test('cada proteccion debe ser un string no vacio', () => {
      dashboardStatus.protections.forEach(protection => {
        expect(typeof protection).toBe('string');
        expect(protection.length).toBeGreaterThan(0);
      });
    });

    test('no debe haber protecciones duplicadas', () => {
      const uniqueProtections = new Set(dashboardStatus.protections);
      expect(uniqueProtections.size).toBe(dashboardStatus.protections.length);
    });
  });

  describe('dashboardStatus.evidence', () => {
    test('vulnerablePr debe ser una URL valida', () => {
      expect(dashboardStatus.evidence.vulnerablePr).toMatch(/^https?:\/\//);
    });

    test('vulnerableRun debe ser una URL valida', () => {
      expect(dashboardStatus.evidence.vulnerableRun).toMatch(/^https?:\/\//);
    });

    test('documentation debe ser un string', () => {
      expect(typeof dashboardStatus.evidence.documentation).toBe('string');
    });
  });

  describe('dashboardStatus general', () => {
    test('project debe ser un string no vacio', () => {
      expect(typeof dashboardStatus.project).toBe('string');
      expect(dashboardStatus.project.length).toBeGreaterThan(0);
    });

    test('environment debe ser un string no vacio', () => {
      expect(typeof dashboardStatus.environment).toBe('string');
      expect(dashboardStatus.environment.length).toBeGreaterThan(0);
    });
  });
});
