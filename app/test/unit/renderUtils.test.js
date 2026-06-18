const {
  formatPercent,
  renderMetric,
  renderPipelineStep,
  renderProtection,
  renderEvidenceLink,
  renderMetricsSection,
  renderPipelineSection,
  renderProtectionsSection,
  renderEvidenceSection
} = require('../../lib/renderUtils');

describe('renderUtils', () => {
  describe('formatPercent', () => {
    test('debe convertir decimal a porcentaje con 2 decimales', () => {
      expect(formatPercent(0.8268)).toBe('82.68%');
    });

    test('debe manejar 0 correctamente', () => {
      expect(formatPercent(0)).toBe('0.00%');
    });

    test('debe manejar 1 correctamente', () => {
      expect(formatPercent(1)).toBe('100.00%');
    });

    test('debe redondear correctamente', () => {
      expect(formatPercent(0.8268)).toBe('82.68%');
      expect(formatPercent(0.8271)).toBe('82.71%');
    });
  });

  describe('renderMetric', () => {
    test('debe renderizar una metrica con label y valor', () => {
      const result = renderMetric('Accuracy', '82.68%');
      expect(result).toContain('Accuracy');
      expect(result).toContain('82.68%');
      expect(result).toContain('metric');
    });

    test('debe incluir la clase metric', () => {
      const result = renderMetric('Test', 'Value');
      expect(result).toContain('class="metric"');
    });
  });

  describe('renderPipelineStep', () => {
    test('debe renderizar un paso del pipeline', () => {
      const step = { name: 'Dev', state: 'Base de trabajo', status: 'ready' };
      const result = renderPipelineStep(step);
      expect(result).toContain('Dev');
      expect(result).toContain('Base de trabajo');
      expect(result).toContain('validado');
    });

    test('debe mostrar pendiente cuando status es warning', () => {
      const step = { name: 'Test', state: 'En progreso', status: 'warning' };
      const result = renderPipelineStep(step);
      expect(result).toContain('pendiente');
      expect(result).toContain('warning');
    });
  });

  describe('renderProtection', () => {
    test('debe renderizar una proteccion con check icon', () => {
      const result = renderProtection('Proteccion de prueba');
      expect(result).toContain('Proteccion de prueba');
      expect(result).toContain('check-icon');
      expect(result).toContain('✓');
    });
  });

  describe('renderEvidenceLink', () => {
    test('debe renderizar un enlace de evidencia', () => {
      const result = renderEvidenceLink('PR vulnerable', 'https://example.com', '#14');
      expect(result).toContain('PR vulnerable');
      expect(result).toContain('https://example.com');
      expect(result).toContain('#14');
      expect(result).toContain('evidence-link');
    });
  });

  describe('renderMetricsSection', () => {
    test('debe renderizar la seccion de metricas', () => {
      const model = {
        accuracy: 0.8268,
        precision: 0.8271,
        recall: 0.8213,
        f1Score: 0.8242
      };
      const result = renderMetricsSection(model);
      expect(result).toContain('Accuracy');
      expect(result).toContain('Precision');
      expect(result).toContain('Recall');
      expect(result).toContain('F1-Score');
      expect(result).toContain('82.68%');
      expect(result).toContain('metrics');
    });
  });

  describe('renderPipelineSection', () => {
    test('debe renderizar la seccion del pipeline', () => {
      const pipeline = [
        { name: 'Dev', state: 'Base de trabajo', status: 'ready' },
        { name: 'Test', state: 'Promocion validada', status: 'ready' }
      ];
      const result = renderPipelineSection(pipeline);
      expect(result).toContain('Flujo protegido');
      expect(result).toContain('Dev');
      expect(result).toContain('Test');
      expect(result).toContain('workflow');
    });
  });

  describe('renderProtectionsSection', () => {
    test('debe renderizar la seccion de protecciones', () => {
      const protections = [
        'Proteccion 1',
        'Proteccion 2'
      ];
      const result = renderProtectionsSection(protections);
      expect(result).toContain('Controles del pipeline');
      expect(result).toContain('Proteccion 1');
      expect(result).toContain('Proteccion 2');
      expect(result).toContain('checks');
    });
  });

  describe('renderEvidenceSection', () => {
    test('debe renderizar la seccion de evidencia', () => {
      const evidence = {
        vulnerablePr: 'https://example.com/pr',
        vulnerableRun: 'https://example.com/run'
      };
      const result = renderEvidenceSection(evidence);
      expect(result).toContain('Evidencia rapida');
      expect(result).toContain('PR vulnerable');
      expect(result).toContain('Workflow fallido');
      expect(result).toContain('Estado del sistema');
    });
  });
});
