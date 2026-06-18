const express = require('express');
const { dashboardStatus } = require('./config');
const { renderMetricsSection, renderPipelineSection, renderProtectionsSection, renderEvidenceSection, formatPercent } = require('./lib/renderUtils');
const { setupRoutes } = require('./routes');
const app = express();

app.use(express.json());

const renderDashboard = () => `<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${dashboardStatus.project}</title>
    <style>
      :root {
        color-scheme: light;
        --bg: #f5f7f4;
        --panel: #ffffff;
        --ink: #18201c;
        --muted: #607066;
        --line: #dbe3dc;
        --green: #157a52;
        --green-soft: #e6f4ed;
        --amber: #a15c09;
        --amber-soft: #fff3d8;
        --red: #b42318;
        --shadow: 0 14px 30px rgba(24, 32, 28, 0.08);
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        min-height: 100vh;
        background: var(--bg);
        color: var(--ink);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }

      a {
        color: var(--green);
        font-weight: 700;
        text-decoration: none;
      }

      a:hover {
        text-decoration: underline;
      }

      .shell {
        width: min(1180px, calc(100% - 32px));
        margin: 0 auto;
        padding: 28px 0 36px;
      }

      .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 24px;
      }

      .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
      }

      .mark {
        display: grid;
        place-items: center;
        width: 44px;
        height: 44px;
        border-radius: 8px;
        background: var(--green);
        color: #ffffff;
        font-weight: 900;
        letter-spacing: 0;
      }

      h1, h2, h3, p {
        margin: 0;
      }

      h1 {
        font-size: clamp(1.7rem, 3vw, 2.6rem);
        letter-spacing: 0;
        line-height: 1.05;
      }

      .subtitle {
        margin-top: 6px;
        color: var(--muted);
        font-size: 0.98rem;
      }

      .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        min-height: 40px;
        padding: 0 14px;
        border: 1px solid #b6dfca;
        border-radius: 999px;
        background: var(--green-soft);
        color: var(--green);
        font-weight: 800;
        white-space: nowrap;
      }

      .dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: currentColor;
      }

      .hero {
        display: grid;
        grid-template-columns: minmax(0, 1.15fr) minmax(280px, 0.85fr);
        gap: 18px;
        align-items: stretch;
        margin-bottom: 18px;
      }

      .panel,
      .metric,
      .step,
      .evidence-link {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
        box-shadow: var(--shadow);
      }

      .panel {
        padding: 22px;
      }

      .panel h2 {
        margin-bottom: 12px;
        font-size: 1.05rem;
      }

      .summary {
        display: grid;
        gap: 18px;
        align-content: space-between;
      }

      .summary p {
        color: var(--muted);
        line-height: 1.55;
      }

      .actions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 20px;
      }

      .button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 42px;
        padding: 0 16px;
        border: 1px solid var(--green);
        border-radius: 8px;
        background: var(--green);
        color: #ffffff;
        font-weight: 800;
        cursor: pointer;
      }

      .button.secondary {
        background: #ffffff;
        color: var(--green);
      }

      .button:focus-visible,
      a:focus-visible {
        outline: 3px solid #9bd3b8;
        outline-offset: 2px;
      }

      .health-result {
        min-height: 24px;
        margin-top: 12px;
        color: var(--muted);
        font-weight: 700;
      }

      .metrics {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin-bottom: 18px;
      }

      .metric {
        padding: 16px;
      }

      .metric span {
        display: block;
        color: var(--muted);
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
      }

      .metric strong {
        display: block;
        margin-top: 8px;
        font-size: 1.7rem;
        line-height: 1;
      }

      .workflow {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(142px, 1fr));
        gap: 10px;
      }

      .step {
        position: relative;
        min-height: 132px;
        padding: 14px;
      }

      .step strong {
        display: block;
        margin-bottom: 8px;
      }

      .step span {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.35;
      }

      .badge {
        display: inline-flex;
        align-items: center;
        min-height: 24px;
        padding: 0 8px;
        margin-top: 14px;
        border-radius: 999px;
        background: var(--green-soft);
        color: var(--green);
        font-size: 0.75rem;
        font-weight: 900;
        text-transform: uppercase;
      }

      .badge.warning {
        background: var(--amber-soft);
        color: var(--amber);
      }

      .grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(280px, 0.8fr);
        gap: 18px;
        margin-top: 18px;
      }

      .checks {
        display: grid;
        gap: 10px;
        padding: 0;
        margin: 0;
        list-style: none;
      }

      .checks li {
        display: grid;
        grid-template-columns: 28px 1fr;
        align-items: start;
        gap: 10px;
        color: var(--muted);
        line-height: 1.45;
      }

      .check-icon {
        display: grid;
        place-items: center;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: var(--green-soft);
        color: var(--green);
        font-weight: 900;
      }

      .evidence {
        display: grid;
        gap: 10px;
      }

      .evidence-link {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding: 14px;
      }

      .evidence-link span {
        color: var(--muted);
        font-size: 0.88rem;
      }

      @media (max-width: 920px) {
        .hero,
        .grid {
          grid-template-columns: 1fr;
        }

        .metrics {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .workflow {
          grid-template-columns: repeat(3, minmax(0, 1fr));
        }
      }

      @media (max-width: 640px) {
        .shell {
          width: min(100% - 20px, 1180px);
          padding-top: 18px;
        }

        .topbar {
          align-items: flex-start;
          flex-direction: column;
        }

        .metrics,
        .workflow {
          grid-template-columns: 1fr;
        }

        .panel {
          padding: 18px;
        }
      }
    </style>
  </head>
  <body>
    <main class="shell">
      <section class="topbar" aria-label="Estado general">
        <div class="brand">
          <div class="mark" aria-hidden="true">AI</div>
          <div>
            <h1>${dashboardStatus.project}</h1>
            <p class="subtitle">Panel de control para revision segura de codigo, pruebas y despliegue.</p>
          </div>
        </div>
        <div class="status-pill"><span class="dot" aria-hidden="true"></span>API online</div>
      </section>

      <section class="hero">
        <article class="panel summary">
          <div>
            <h2>Revision actual</h2>
            <p>El proyecto valida Pull Requests con un modelo de IA, bloquea codigo vulnerable, exige pruebas antes de promocionar ramas y centraliza evidencia para la entrega.</p>
          </div>
          <div>
            <div class="actions">
              <button class="button" id="healthButton" type="button">Probar API</button>
              <a class="button secondary" href="/api/status">Ver JSON</a>
            </div>
            <div class="health-result" id="healthResult" role="status">Listo para probar el servicio.</div>
          </div>
        </article>

        <aside class="panel">
          <h2>Modelo entrenado</h2>
          <ul class="checks">
            <li><span class="check-icon">✓</span><span>${dashboardStatus.model.featureCount} caracteristicas analizadas.</span></li>
            <li><span class="check-icon">✓</span><span>Nueva senal AST: ${dashboardStatus.model.latestFeature}.</span></li>
            <li><span class="check-icon">✓</span><span>AUC-ROC ${formatPercent(dashboardStatus.model.aucRoc)} en evaluacion.</span></li>
          </ul>
        </aside>
      </section>

      ${renderMetricsSection(dashboardStatus.model)}

      ${renderPipelineSection(dashboardStatus.pipeline)}

      <section class="grid">
        ${renderProtectionsSection(dashboardStatus.protections)}
        ${renderEvidenceSection(dashboardStatus.evidence)}
      </section>
    </main>

    <script>
      const button = document.querySelector('#healthButton');
      const result = document.querySelector('#healthResult');

      button.addEventListener('click', async () => {
        result.textContent = 'Consultando /health...';
        try {
          const response = await fetch('/health');
          const data = await response.json();
          result.textContent = response.ok && data.status === 'ok'
            ? 'Servicio activo: /health respondio correctamente.'
            : 'El servicio respondio, pero requiere revision.';
        } catch (error) {
          result.textContent = 'No se pudo consultar el servicio.';
        }
      });
    </script>
  </body>
</html>`;

app.get('/', (req, res) => {
  res.type('html').send(renderDashboard());
});

// Setup API routes
setupRoutes(app);

module.exports = app;
module.exports.formatPercent = formatPercent;
module.exports.dashboardStatus = dashboardStatus;
module.exports.renderDashboard = renderDashboard;
module.exports.renderMetricsSection = renderMetricsSection;
module.exports.renderPipelineSection = renderPipelineSection;
module.exports.renderProtectionsSection = renderProtectionsSection;
module.exports.renderEvidenceSection = renderEvidenceSection;
