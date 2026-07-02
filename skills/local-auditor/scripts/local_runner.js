const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const crypto = require('crypto');
const { compilePrompt, compileFixPrompt } = require('./prompts');
const { parseJsonResponse, parseCleanCode } = require('./parser');
const { callLLM } = require('./client');

// Import double-blind orchestrator for final adversarial validation
let runDoubleBlindReview;
try {
  const dbOrchestrator = require('../../double-blind-review/scripts/orchestrator');
  runDoubleBlindReview = dbOrchestrator.runDoubleBlindReview;
} catch (e) {
  // If double-blind review skill is not installed or available, we will flag it
  runDoubleBlindReview = null;
}

/**
 * Custom Convergence Error for auto-fix loops
 */
class ConvergenceError extends Error {
  constructor(stage, findings) {
    super(`Convergence Failure in stage [${stage}]. Exceeded maximum fix attempts.`);
    this.stage = stage;
    this.findings = findings;
  }
}

/**
 * Checks if Git is available and the target is tracked.
 */
function getGitStatus(targetPath) {
  const dir = path.dirname(targetPath);
  try {
    // Check if inside a git work tree
    execSync('git rev-parse --is-inside-work-tree', { cwd: dir, stdio: 'ignore' });
    
    // Check if the file is tracked or ignored
    try {
      execSync(`git ls-files --error-unmatch "${targetPath}"`, { cwd: dir, stdio: 'ignore' });
      return { available: true, tracked: true };
    } catch (e) {
      // Untracked file
      return { available: true, tracked: false };
    }
  } catch (e) {
    // Git not available or not a repo
    return { available: false, tracked: false };
  }
}

/**
 * Runs a Git commit strictly for the target file, handling any unstaged changes safely.
 */
function gitCommitFile(targetPath, message) {
  const dir = path.dirname(targetPath);
  const fileBasename = path.basename(targetPath);
  try {
    // Add file explicitly to stage it
    execSync(`git add "${targetPath}"`, { cwd: dir });
    
    // Commit only the target file to avoid committing other staged files
    const stdout = execSync(`git commit -m "${message}" -- "${targetPath}"`, { cwd: dir, encoding: 'utf8' });
    
    // Extract commit hash if possible
    const match = stdout.match(/\[\w+\s+([0-9a-f]+)\]/i);
    return match ? match[1] : 'checkpoint';
  } catch (e) {
    // If there is nothing to commit, ignore the error and return status
    const msg = (e.message || '').toLowerCase() + (e.stdout || '').toLowerCase() + (e.stderr || '').toLowerCase();
    if (
      msg.includes('nothing to commit') || 
      msg.includes('clean') || 
      msg.includes('no changes added') || 
      msg.includes('nothing added')
    ) {
      return 'no-changes';
    }
    throw e;
  }
}

/**
 * Physical backup fallback helper
 */
function createPhysicalBackup(targetPath, stage, type) {
  const scratchDir = 'd:/Engram_SDD/scratch';
  if (!fs.existsSync(scratchDir)) {
    fs.mkdirSync(scratchDir, { recursive: true });
  }
  const basename = path.basename(targetPath, path.extname(targetPath));
  const ext = path.extname(targetPath);
  const backupName = `${basename}_${stage}_${type}_${Date.now()}${ext}.bak`;
  const backupPath = path.join(scratchDir, backupName);
  fs.copyFileSync(targetPath, backupPath);
  return backupPath;
}

/**
 * Helper to calculate file hash
 */
function getFileHash(targetPath) {
  const content = fs.readFileSync(targetPath, 'utf8');
  return crypto.createHash('sha256').update(content).digest('hex');
}

/**
 * Cache management for incremental mode
 */
function loadCache(cachePath) {
  try {
    if (fs.existsSync(cachePath)) {
      return JSON.parse(fs.readFileSync(cachePath, 'utf8'));
    }
  } catch (e) {
    // Ignore invalid cache
  }
  return {};
}

function saveCache(cachePath, cacheData) {
  try {
    const dir = path.dirname(cachePath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(cachePath, JSON.stringify(cacheData, null, 2), 'utf8');
  } catch (e) {
    console.warn(`! Advertencia: No se pudo escribir la caché en ${cachePath}`);
  }
}

/**
 * Main Sequential Local Auditor Orchestrator
 */
async function runLocalAudit(options) {
  const {
    targetPath,
    localUrl = process.env.LOCAL_LLM_URL || 'http://localhost:1234/v1',
    localModel = process.env.LOCAL_MODEL || 'llama-3-8b',
    maxAttempts = parseInt(options.maxAttempts || 3, 10),
    customCriteria = '',
    dryRun = false,
    incremental = false,
    incrementalCachePath = 'd:/Engram_SDD/scratch/.local_audit_cache.json',
    onlyStages = null // Can be a string like 'security,semantic' or an array
  } = options;

  if (!targetPath) {
    throw new Error('Target path is required.');
  }

  const resolvedTarget = path.resolve(targetPath);
  if (!fs.existsSync(resolvedTarget)) {
    throw new Error(`Target file not found: ${resolvedTarget}`);
  }

  const fileBasename = path.basename(resolvedTarget);
  console.log(`\n======================================================`);
  console.log(`▶ INICIANDO AUDITORIA LOCAL SECUENCIAL: ${fileBasename}`);
  if (dryRun) console.log(`▶ [MODO DRY-RUN ACTIVADO: No se modificará el archivo]`);
  console.log(`======================================================`);

  const git = getGitStatus(resolvedTarget);
  console.log(`Git Status: ${git.available ? (git.tracked ? 'Trackeado en Git' : 'No trackeado (se trackeará)') : 'No disponible (usando backups físicos)'}`);

  // Track the file in Git if Git is available but file is untracked
  if (git.available && !git.tracked && !dryRun) {
    try {
      execSync(`git add "${resolvedTarget}"`, { cwd: path.dirname(resolvedTarget) });
      console.log(`+ Agregado ${fileBasename} al control de Git.`);
    } catch (e) {
      console.warn(`! Advertencia: No se pudo agregar el archivo a Git.`, e.message);
    }
  }

  const allStages = ['structural', 'semantic', 'security', 'architecture'];
  let stagesToRun = allStages;
  
  if (onlyStages) {
    const onlyArr = Array.isArray(onlyStages) ? onlyStages : onlyStages.split(',').map(s => s.trim());
    stagesToRun = allStages.filter(s => onlyArr.includes(s));
    console.log(`▶ Filtrando etapas: Solo se ejecutarán [${stagesToRun.join(', ')}]`);
  }

  // Handle Incremental Cache
  let auditCache = {};
  let fileHash = '';
  let cachedStages = {};
  
  if (incremental) {
    auditCache = loadCache(incrementalCachePath);
    fileHash = getFileHash(resolvedTarget);
    if (auditCache[resolvedTarget] && auditCache[resolvedTarget].hash === fileHash) {
      cachedStages = auditCache[resolvedTarget].cleanStages || {};
      console.log(`▶ [MODO INCREMENTAL]: Caché detectada y hash coincidente.`);
    } else {
      console.log(`▶ [MODO INCREMENTAL]: Archivo modificado o sin caché. Analizando desde cero.`);
    }
  }

  const auditLogs = [];
  const telemetries = [];
  const fixAttempts = { structural: 0, semantic: 0, security: 0, architecture: 0 };
  let cleanPasses = 0;
  let totalLoops = 0;
  let status = 'APPROVED';
  let convergenceError = null;

  while (cleanPasses < (dryRun ? 1 : 3)) {
    totalLoops++;
    console.log(`\n--- BATCH DE AUDITORÍA CONSECUTIVO #${cleanPasses + 1} (Bucle Global #${totalLoops}) ---`);
    let batchClean = true;

    for (const stage of stagesToRun) {
      if (incremental && cachedStages[stage]) {
        console.log(`✓ Etapa [${stage.toUpperCase()}] saltada (Limpia en caché).`);
        auditLogs.push({ loop: totalLoops, stage: stage, findings: [], action: 'SKIPPED_BY_CACHE' });
        continue;
      }

      console.log(`[Etapa: ${stage.toUpperCase()}] Analizando...`);
      const code = fs.readFileSync(resolvedTarget, 'utf8');
      
      const prompt = compilePrompt(stage, code, customCriteria);
      const result = await callLLM(localUrl, localModel, prompt, 'Eres un auditor técnico meticuloso.');
      const findings = parseJsonResponse(result.content);
      
      telemetries.push({
        loop: totalLoops,
        stage: stage,
        model: result.actualModel || localModel,
        ...result.metrics
      });

      if (findings.length > 0) {
        console.log(`⚠ ¡Hallazgos detectados en [${stage}]! total: ${findings.length}`);
        console.log(JSON.stringify(findings, null, 2));

        batchClean = false;
        
        if (dryRun) {
          console.log(`▶ [DRY-RUN] Omitiendo Auto-Fix para [${stage}].`);
          status = 'DRY_RUN_COMPLETED';
          auditLogs.push({
            loop: totalLoops, stage: stage, findings: findings, action: 'DRY_RUN_REPORTED'
          });
          continue; // Move to the next stage to just report
        }

        fixAttempts[stage]++;

        if (fixAttempts[stage] > maxAttempts) {
          status = 'CONVERGENCE_FAILED';
          convergenceError = new ConvergenceError(stage, findings);
          auditLogs.push({
            loop: totalLoops, stage: stage, findings: findings, action: 'LIMIT_EXCEEDED',
            details: `Excedió el límite de ${maxAttempts} intentos.`
          });
          break;
        }

        // Git Pre-Fix Checkpoint
        let preFixRef = 'N/A';
        if (git.available) {
          preFixRef = gitCommitFile(resolvedTarget, `pre-fix: local-auditor ${stage} checkpoint for ${fileBasename}`);
          console.log(`✓ Git Checkpoint PRE-FIX: ${preFixRef}`);
        } else {
          preFixRef = createPhysicalBackup(resolvedTarget, stage, 'pre');
          console.log(`✓ Backup físico creado PRE-FIX: ${path.basename(preFixRef)}`);
        }

        // Run Auto-Fix refactoring
        console.log(`[Auto-Fix: ${stage.toUpperCase()}] Refactorizando código para corregir los hallazgos...`);
        const fixPrompt = compileFixPrompt(code, findings, stage);
        const fixResult = await callLLM(localUrl, localModel, fixPrompt, 'Eres un refactorizador de código experto.');
        
        telemetries.push({
          loop: totalLoops,
          stage: `${stage}_fix`,
          model: fixResult.actualModel || localModel,
          ...fixResult.metrics
        });

        const correctedCode = parseCleanCode(fixResult.content);
        if (!correctedCode) {
          console.error(`❌ Error: El modelo retornó un código vacío o corrupto.`);
          status = 'FIX_FAILED';
          break;
        }

        // Write corrected code
        fs.writeFileSync(resolvedTarget, correctedCode, 'utf8');

        // Git Post-Fix Checkpoint
        let postFixRef = 'N/A';
        if (git.available) {
          postFixRef = gitCommitFile(resolvedTarget, `fix: local-auditor ${stage} auto-applied fixes for ${fileBasename}`);
          console.log(`✓ Git Checkpoint POST-FIX: ${postFixRef}`);
        } else {
          postFixRef = createPhysicalBackup(resolvedTarget, stage, 'post');
          console.log(`✓ Backup físico creado POST-FIX: ${path.basename(postFixRef)}`);
        }

        auditLogs.push({
          loop: totalLoops, stage: stage, findings: findings, action: 'AUTO_FIXED',
          preFixRef, postFixRef
        });

        // SHORT-CIRCUIT & RESET: reiniciar desde Stage 1 (solo si no es dry run)
        console.log(`↺ Reiniciando ciclo de auditoría desde ETAPA 1 para prevenir regresiones.`);
        cleanPasses = 0;
        // Invalidate cache for remaining stages if code was modified
        if (incremental) {
          cachedStages = {}; 
        }
        break; 
      } else {
        console.log(`✓ Etapa [${stage.toUpperCase()}] limpia de hallazgos.`);
        auditLogs.push({ loop: totalLoops, stage: stage, findings: [], action: 'PASSED' });
        // Mark stage as clean dynamically
        if (incremental) {
          cachedStages[stage] = true;
        }
      }
    }

    if (status !== 'APPROVED' && status !== 'DRY_RUN_COMPLETED') {
      break; // Exit if failed to converge or fix
    }

    if (batchClean) {
      cleanPasses++;
      if (!dryRun) {
        console.log(`✓ BATCH COMPLETO LIMPIO! Clean Passes acumulados: ${cleanPasses}/3`);
      }
    }

    if (dryRun) {
      // En modo dry-run, solo hacemos un barrido independientemente de los hallazgos
      break;
    }
  }

  // Update Incremental Cache if completely approved
  if (incremental && status === 'APPROVED') {
    auditCache[resolvedTarget] = {
      hash: getFileHash(resolvedTarget),
      cleanStages: cachedStages,
      lastAudit: new Date().toISOString()
    };
    saveCache(incrementalCachePath, auditCache);
    console.log(`✓ Caché incremental actualizada.`);
  }

  // ----------------------------------------------------
  // Graduación: Invocación a Double-Blind Review
  // ----------------------------------------------------
  let doubleBlindReport = null;
  if (status === 'APPROVED' && runDoubleBlindReview && !dryRun) {
    console.log(`\n======================================================`);
    console.log(`🎓 ¡GRADUADO! Superados los 3 batches limpios locales.`);
    console.log(`🚀 Iniciando QA Adversarial Double-Blind Review en la nube...`);
    console.log(`======================================================`);
    try {
      const dbResult = await runDoubleBlindReview({
        targetPath: resolvedTarget,
        customCriteria
      });
      doubleBlindReport = dbResult.report;
      console.log(`✓ Double-Blind Review completado con éxito.`);
    } catch (e) {
      console.error(`! Advertencia: Falló el Double-Blind Review adversarial en la nube:`, e.message);
      doubleBlindReport = `Fallo en revisión de nube: ${e.message}`;
    }
  } else if (!runDoubleBlindReview) {
    console.warn(`! Nota: Skill double-blind-review no encontrada o no se pudo importar. Omitiendo graduación en la nube.`);
  }

  // ----------------------------------------------------
  // Compilación de Reporte final Markdown (Artifact)
  // ----------------------------------------------------
  const reportMarkdown = compileReportMarkdown({
    fileBasename,
    resolvedTarget,
    status,
    totalLoops,
    fixAttempts,
    auditLogs,
    telemetries,
    doubleBlindReport,
    convergenceError
  });

  const scratchDir = 'd:/Engram_SDD/scratch';
  if (!fs.existsSync(scratchDir)) {
    fs.mkdirSync(scratchDir, { recursive: true });
  }
  const reportPath = path.join(scratchDir, `local_audit_report_${path.basename(resolvedTarget, path.extname(resolvedTarget))}.md`);
  fs.writeFileSync(reportPath, reportMarkdown, 'utf8');

  console.log(`\n======================================================`);
  console.log(`📝 REPORTE GENERADO EN: ${reportPath}`);
  console.log(`======================================================\n`);
  
  // Display the Markdown report directly on the console
  console.log(reportMarkdown);

  if (convergenceError) {
    throw convergenceError;
  }

  return {
    status,
    reportPath,
    reportMarkdown,
    doubleBlindReport
  };
}

/**
 * Helper to compile the markdown report
 */
function compileReportMarkdown(data) {
  const {
    fileBasename,
    resolvedTarget,
    status,
    totalLoops,
    fixAttempts,
    auditLogs,
    telemetries,
    doubleBlindReport,
    convergenceError
  } = data;

  const totalDuration = telemetries.reduce((acc, t) => acc + t.duration_ms, 0);
  const totalTokens = telemetries.reduce((acc, t) => acc + t.prompt_tokens + t.completion_tokens, 0);

  let statusBadge = '🟢 APROBADO Y GRADUADO';
  if (status === 'CONVERGENCE_FAILED') {
    statusBadge = '🔴 FALLÓ POR CONVERGENCIA';
  } else if (status === 'FIX_FAILED') {
    statusBadge = '🔴 FALLÓ POR AUTO-FIX';
  } else if (status === 'DRY_RUN_COMPLETED') {
    statusBadge = '🟡 DRY-RUN COMPLETADO (Reporte de hallazgos sin modificar)';
  }

  let markdown = `> [!NOTE]
> **Identity**: Antigravity | **Context**: Local | **Role**: QA Auditor

# 📊 Reporte Técnico de Auditoría Local: \`${fileBasename}\`

## 📈 Resumen Ejecutivo

| Métrica | Detalle |
| :--- | :--- |
| **Archivo Auditado** | [\`${fileBasename}\`](file:///${resolvedTarget.replace(/\\/g, '/')}) |
| **Estado Final** | **${statusBadge}** |
| **Bucles Totales** | ${totalLoops} ciclos |
| **Duración Acumulada** | ${(totalDuration / 1000).toFixed(2)} segundos |
| **Tokens Consumidos** | ${totalTokens.toLocaleString()} tokens |
| **Ruta del Reporte** | \`${resolvedTarget}\` |

---

## 🛠️ Intentos de Auto-Fix por Etapa

| Etapa | Reintentos Aplicados | Límite Máximo |
| :--- | :---: | :---: |
| **Auditoría Estructural (structural)** | ${fixAttempts.structural} | 3 |
| **Auditoría Semántica (semantic)** | ${fixAttempts.semantic} | 3 |
| **Auditoría de Seguridad (security)** | ${fixAttempts.security} | 3 |
| **Auditoría de Arquitectura (architecture)** | ${fixAttempts.architecture} | 3 |

---

## 📜 Historial Detallado de Hallazgos y Checkpoints

`;

  if (auditLogs.length === 0) {
    markdown += `*✓ El archivo pasó todas las etapas limpiamente en la primera pasada sin requerir ninguna modificación.*`;
  } else {
    markdown += `| Ciclo | Etapa | Estado / Acción | Hallazgos Detectados | Checkpoint PRE-FIX | Checkpoint POST-FIX |\n`;
    markdown += `| :---: | :--- | :--- | :--- | :--- | :--- |\n`;

    auditLogs.forEach(log => {
      const findingsSummary = log.findings.length > 0 
        ? log.findings.map(f => `• [Línea ${f.linea || '?'}] ${f.hallazgo}`).join('<br>')
        : '✓ Limpio';
      
      const preRef = log.preFixRef ? (log.preFixRef.length === 7 || log.preFixRef.length === 8 || log.preFixRef.length === 40 ? `\`${log.preFixRef}\`` : `_Backup físico_`) : '-';
      const postRef = log.postFixRef ? (log.postFixRef.length === 7 || log.postFixRef.length === 8 || log.postFixRef.length === 40 ? `\`${log.postFixRef}\`` : `_Backup físico_`) : '-';

      markdown += `| ${log.loop} | **${log.stage}** | \`${log.action}\` | ${findingsSummary} | ${preRef} | ${postRef} |\n`;
    });
  }

  markdown += `\n\n---\n\n## ⚡ Telemetría y Eficiencia del Modelo Local\n\n`;

  // Aggregate telemetry by stage
  const stageEfficiency = {};
  telemetries.forEach(t => {
    // Treat fix stages mapped to their parent for grouping if needed, but separate is finer
    const baseStage = t.stage;
    if (!stageEfficiency[baseStage]) {
      stageEfficiency[baseStage] = { tokens: 0, duration: 0, calls: 0 };
    }
    stageEfficiency[baseStage].tokens += t.prompt_tokens + t.completion_tokens;
    stageEfficiency[baseStage].duration += t.duration_ms;
    stageEfficiency[baseStage].calls += 1;
  });

  markdown += `### Eficiencia de Inferencia por Etapa\n\n`;
  markdown += `| Etapa | Invocaciones | Duración Total (ms) | Tokens Consumidos |\n`;
  markdown += `| :--- | :---: | :---: | :---: |\n`;
  for (const [stageName, data] of Object.entries(stageEfficiency)) {
    markdown += `| \`${stageName}\` | ${data.calls} | ${data.duration} | ${data.tokens.toLocaleString()} |\n`;
  }

  markdown += `\n### Desglose Completo de Invocaciones\n\n`;
  markdown += `| Ciclo | Etapa / Operación | Modelo Involucrado | Duración (ms) | Tokens Entrada | Tokens Salida | Velocidad (TPS) |\n`;
  markdown += `| :---: | :--- | :--- | :---: | :---: | :---: | :---: |\n`;

  telemetries.forEach(t => {
    markdown += `| ${t.loop} | \`${t.stage}\` | ${t.model} | ${t.duration_ms} | ${t.prompt_tokens} | ${t.completion_tokens} | ${t.speed_tps} tps |\n`;
  });

  if (convergenceError) {
    markdown += `\n\n> [!CAUTION]\n> **ERROR DE CONVERGENCIA DETECTADO**\n> El modelo local no pudo resolver de manera autónoma los hallazgos en la etapa **${convergenceError.stage}** tras agotar los intentos máximos permitidos. Se requiere intervención y corrección manual en el archivo.\n`;
  }

  if (doubleBlindReport) {
    markdown += `\n\n---\n\n## 🎓 Reporte de Graduación: Double-Blind Review (Nube)\n\n${doubleBlindReport}\n`;
  }

  return markdown;
}

module.exports = {
  runLocalAudit,
  ConvergenceError
};

// CLI execution handling
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--target' || args[i] === '-t') {
      options.targetPath = args[++i];
    } else if (args[i] === '--local-url') {
      options.localUrl = args[++i];
    } else if (args[i] === '--local-model') {
      options.localModel = args[++i];
    } else if (args[i] === '--max-attempts') {
      options.maxAttempts = args[++i];
    } else if (args[i] === '--criteria') {
      options.customCriteria = args[++i];
    }
  }
  
  if (!options.targetPath) {
    console.error('Error: --target <path> es requerido.');
    process.exit(1);
  }
  
  runLocalAudit(options)
    .then(result => {
      process.exit(result.status === 'APPROVED' ? 0 : 1);
    })
    .catch(err => {
      console.error('\n❌ ERROR EN LA AUDITORÍA LOCAL:', err.message);
      process.exit(1);
    });
}
