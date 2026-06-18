const { formatPercent } = require('../../lib/renderUtils');

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

  test('debe maneval valores pequenos', () => {
    expect(formatPercent(0.001)).toBe('0.10%');
  });
});
