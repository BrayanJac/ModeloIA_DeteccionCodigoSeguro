const dashboardStatus = {
  project: 'Secure CI/CD AI Pipeline',
  environment: 'demo',
  model: {
    accuracy: 0.8268,
    precision: 0.8271,
    recall: 0.8213,
    f1Score: 0.8242,
    aucRoc: 0.9142,
    featureCount: 3054,
    latestFeature: 'ast_depth'
  },
  pipeline: [
    { name: 'Dev', state: 'Base de trabajo', status: 'ready' },
    { name: 'Pull Request', state: 'Revision obligatoria', status: 'ready' },
    { name: 'Analisis IA', state: 'Bloquea codigo vulnerable', status: 'ready' },
    { name: 'Test', state: 'Promocion validada', status: 'ready' },
    { name: 'Main', state: 'Merge controlado', status: 'ready' },
    { name: 'Branch Rules', state: 'Requiere token admin en GitHub', status: 'ready' },
    { name: 'Deploy', state: 'Vercel pendiente de acceso publico', status: 'ready' }
  ],
  protections: [
    'Script preparado para bloquear push directo con reglas de ramas',
    'Promocion dev -> test solo desde Pull Request',
    'Promocion test -> main solo desde workflow validado',
    'Notificaciones por Telegram y comentarios en Pull Request'
  ],
  evidence: {
    vulnerablePr: 'https://github.com/BrayanJac/ModeloIA_DeteccionCodigoSeguro/pull/14',
    vulnerableRun: 'https://github.com/BrayanJac/ModeloIA_DeteccionCodigoSeguro/actions/runs/27707771204',
    documentation: 'docs/evidence.md'
  }
};

module.exports = { dashboardStatus };
