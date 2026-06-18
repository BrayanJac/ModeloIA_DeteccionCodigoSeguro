const formatPercent = (value) => `${(value * 100).toFixed(2)}%`;

const renderMetric = (label, value) => `
  <div class="metric">
    <span>${label}</span>
    <strong>${value}</strong>
  </div>
`;

const renderPipelineStep = (step) => `
  <div class="step">
    <strong>${step.name}</strong>
    <span>${step.state}</span>
    <div class="badge ${step.status === 'warning' ? 'warning' : ''}">${step.status === 'warning' ? 'pendiente' : 'validado'}</div>
  </div>
`;

const renderProtection = (protection) => `
  <li><span class="check-icon">✓</span><span>${protection}</span></li>
`;

const renderEvidenceLink = (label, url, subtitle) => `
  <a class="evidence-link" href="${url}">
    <strong>${label}</strong>
    <span>${subtitle}</span>
  </a>
`;

const renderMetricsSection = (model) => `
  <section class="metrics" aria-label="Metricas principales">
    ${renderMetric('Accuracy', formatPercent(model.accuracy))}
    ${renderMetric('Precision', formatPercent(model.precision))}
    ${renderMetric('Recall', formatPercent(model.recall))}
    ${renderMetric('F1-Score', formatPercent(model.f1Score))}
  </section>
`;

const renderPipelineSection = (pipeline) => `
  <section class="panel">
    <h2>Flujo protegido</h2>
    <div class="workflow">
      ${pipeline.map(renderPipelineStep).join('')}
    </div>
  </section>
`;

const renderProtectionsSection = (protections) => `
  <article class="panel">
    <h2>Controles del pipeline</h2>
    <ul class="checks">
      ${protections.map(renderProtection).join('')}
    </ul>
  </article>
`;

const renderEvidenceSection = (evidence) => `
  <aside class="panel">
    <h2>Evidencia rapida</h2>
    <div class="evidence">
      ${renderEvidenceLink('PR vulnerable', evidence.vulnerablePr, '#14')}
      ${renderEvidenceLink('Workflow fallido', evidence.vulnerableRun, 'GitHub Actions')}
      ${renderEvidenceLink('Estado del sistema', '/api/status', 'API')}
    </div>
  </aside>
`;

module.exports = {
  formatPercent,
  renderMetric,
  renderPipelineStep,
  renderProtection,
  renderEvidenceLink,
  renderMetricsSection,
  renderPipelineSection,
  renderProtectionsSection,
  renderEvidenceSection
};
