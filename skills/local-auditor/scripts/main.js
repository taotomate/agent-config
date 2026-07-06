#!/usr/bin/env node
const { runLocalAudit } = require('local-auditor\scripts\local_runner.js');

/**
 * Main entry point for local-auditor CLI execution.
 */
async function main() {
  const args = process.argv.slice(2);
  const options = {
    batchFiles: []
  };
  
  let isBatchMode = false;

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
    } else if (args[i] === '--dry-run') {
      options.dryRun = true;
    } else if (args[i] === '--incremental') {
      options.incremental = true;
    } else if (args[i] === '--only') {
      options.onlyStages = args[++i];
    } else if (args[i] === '--batch') {
      isBatchMode = true;
      // All remaining arguments are considered target files for the batch
      options.batchFiles = args.slice(i + 1);
      break; 
    }
  }
  
  if (!options.targetPath && !isBatchMode) {
    console.error('\n❌ Error: --target <path> o --batch <paths...> es requerido.\n');
    console.log('Uso 1: node skills/local-auditor/scripts/main.js --target <ruta_archivo> [opciones]');
    console.log('Uso 2: node skills/local-auditor/scripts/main.js [opciones] --batch <ruta1> <ruta2> ...');
    console.log('\nOpciones:');
    console.log('  --local-url <url>      URL del servidor de inferencia local (ej: http://localhost:1234/v1)');
    console.log('  --local-model <model>  Nombre del modelo local a utilizar');
    console.log('  --max-attempts <num>   Límite de intentos de auto-fix por etapa (default: 3)');
    console.log('  --criteria <texto>     Criterios de auditoría personalizados adicionales');
    console.log('  --dry-run              Solo analiza y reporta, no modifica código ni hace git commits');
    console.log('  --incremental          Omite etapas ya aprobadas previamente si el código no cambió');
    console.log('  --only <etapas>        Ejecuta solo etapas específicas separadas por coma (ej: security,semantic)');
    process.exit(1);
  }
  
  try {
    if (isBatchMode) {
      if (options.batchFiles.length === 0) {
        throw new Error('No se especificaron archivos para procesar en modo --batch.');
      }
      
      console.log(`\n📦 INICIANDO BATCH MODE PARA ${options.batchFiles.length} ARCHIVOS...`);
      const results = [];
      
      for (const file of options.batchFiles) {
        const fileOpts = { ...options, targetPath: file };
        try {
          const result = await runLocalAudit(fileOpts);
          results.push({ file, status: result.status });
        } catch (err) {
          console.error(`\n❌ ERROR EN BATCH (${file}):`, err.message);
          results.push({ file, status: 'ERROR_THROWN', error: err.message });
        }
      }
      
      console.log(`\n======================================================`);
      console.log(`📊 RESUMEN FINAL DEL BATCH MODE`);
      console.log(`======================================================`);
      let allPassed = true;
      results.forEach(r => {
        const icon = (r.status === 'APPROVED' || r.status === 'DRY_RUN_COMPLETED') ? '✅' : '❌';
        console.log(`${icon} [${r.status}] ${r.file}`);
        if (r.status !== 'APPROVED' && r.status !== 'DRY_RUN_COMPLETED') allPassed = false;
      });
      process.exit(allPassed ? 0 : 1);
      
    } else {
      const result = await runLocalAudit(options);
      process.exit((result.status === 'APPROVED' || result.status === 'DRY_RUN_COMPLETED') ? 0 : 1);
    }
  } catch (err) {
    console.error('\n❌ ERROR CRÍTICO EN LA AUDITORÍA LOCAL:', err.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
