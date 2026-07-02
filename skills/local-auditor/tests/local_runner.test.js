import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'fs';
import path from 'path';

// Mock the double-blind review orchestrator via require.cache to prevent network calls during local_runner tests
const dbOrchestrator = require('../../double-blind-review/scripts/orchestrator');
dbOrchestrator.runDoubleBlindReview = vi.fn().mockResolvedValue({
  report: 'Mocked Double Blind Report',
  telemetries: []
});

// Define dynamic mock functions
const mockCallLLM = vi.fn();
const mockExecSync = vi.fn();

// Require child_process and assign the delegator function before local_runner is required
const childProcess = require('child_process');
const originalExecSync = childProcess.execSync;
childProcess.execSync = (...args) => mockExecSync(...args);

// Require client first and assign the delegator function before local_runner is required
const client = require('../scripts/client');
client.callLLM = (...args) => mockCallLLM(...args);

// Now require local_runner, which will destructure the delegator functions
const { runLocalAudit, ConvergenceError } = require('../scripts/local_runner');

describe('Local Auditor Runner', () => {
  const scratchDir = 'd:/Engram_SDD/scratch';
  const dummyFile = path.join(scratchDir, 'dummy_test_target.js');

  beforeEach(() => {
    mockCallLLM.mockReset();
    mockExecSync.mockReset();
    
    // Default mock execSync behavior: simulate a clean git environment
    mockExecSync.mockImplementation((cmd) => {
      if (cmd.includes('git rev-parse --is-inside-work-tree')) {
        return 'true';
      }
      if (cmd.includes('git ls-files --error-unmatch')) {
        return 'dummy_test_target.js';
      }
      if (cmd.includes('git commit')) {
        return '[main a1b2c3d] test commit';
      }
      return 'ok';
    });

    // Create scratch directory and dummy test file
    if (!fs.existsSync(scratchDir)) {
      fs.mkdirSync(scratchDir, { recursive: true });
    }
    fs.writeFileSync(dummyFile, 'let x = 1;', 'utf8');
  });

  afterEach(() => {
    // Clean up dummy test file
    if (fs.existsSync(dummyFile)) {
      fs.unlinkSync(dummyFile);
    }
    const cacheFile = path.join(scratchDir, '.local_audit_cache.json');
    if (fs.existsSync(cacheFile)) {
      fs.unlinkSync(cacheFile);
    }
    const reports = fs.readdirSync(scratchDir).filter(f => f.startsWith('local_audit_report_'));
    for (const rep of reports) {
      fs.unlinkSync(path.join(scratchDir, rep));
    }
  });

  it('debe graduar exitosamente tras 3 pasadas limpias consecutivas', async () => {
    fs.writeFileSync(dummyFile, 'function hello() { return "world"; }', 'utf8');

    // Mock callLLM to return empty findings for all stages
    mockCallLLM.mockResolvedValue({
      content: '[]',
      actualModel: 'llama-3-8b',
      metrics: {
        duration_ms: 50,
        prompt_tokens: 10,
        completion_tokens: 5,
        speed_tps: 100
      }
    });

    const result = await runLocalAudit({
      targetPath: dummyFile,
      localUrl: 'http://localhost:1234/v1',
      localModel: 'llama-3-8b',
      maxAttempts: 3
    });

    expect(result.status).toBe('APPROVED');
    // Ensure all 4 stages ran for 3 loops = 12 audit calls
    expect(mockCallLLM).toHaveBeenCalledTimes(12);
  });

  it('debe activar auto-fix, hacer checkpoint de Git, reiniciar ciclo y graduar', async () => {
    fs.writeFileSync(dummyFile, 'let x = 1;', 'utf8');

    // Make mockCallLLM return a finding ONLY on the first structural stage call,
    // and empty lists ([]) for all subsequent calls. Also mock the auto-fix response.
    let callCount = 0;
    mockCallLLM.mockImplementation(async (url, model, prompt, systemPrompt) => {
      callCount++;
      if (systemPrompt && systemPrompt.includes('auditor') && prompt.includes('sintaxis') && callCount === 1) {
        // Return 1 finding for first structural call
        return {
          content: JSON.stringify([{ linea: 1, hallazgo: 'Variable x no usada' }]),
          actualModel: 'llama-3-8b',
          metrics: { duration_ms: 10, prompt_tokens: 5, completion_tokens: 2, speed_tps: 200 }
        };
      }
      if (systemPrompt && systemPrompt.includes('refactorizador')) {
        // Return refactored clean code
        return {
          content: '```javascript\nconsole.log(1);\n```',
          actualModel: 'llama-3-8b',
          metrics: { duration_ms: 10, prompt_tokens: 5, completion_tokens: 2, speed_tps: 200 }
        };
      }
      // Clean pass
      return {
        content: '[]',
        actualModel: 'llama-3-8b',
        metrics: { duration_ms: 10, prompt_tokens: 5, completion_tokens: 2, speed_tps: 200 }
      };
    });

    const result = await runLocalAudit({
      targetPath: dummyFile,
      localUrl: 'http://localhost:1234/v1',
      localModel: 'llama-3-8b',
      maxAttempts: 3
    });

    expect(result.status).toBe('APPROVED');
    // Ensure code was updated and markdown format stripped
    const finalCode = fs.readFileSync(dummyFile, 'utf8');
    expect(finalCode).toBe('console.log(1);');
  });

  it('debe lanzar ConvergenceError tras superar el límite de auto-fixes permitidos', async () => {
    fs.writeFileSync(dummyFile, 'let x = 1;', 'utf8');
    
    // Always return findings for structural stage
    mockCallLLM.mockImplementation(async (url, model, prompt, systemPrompt) => {
      if (systemPrompt && systemPrompt.includes('refactorizador')) {
        return {
          content: 'let x = 1;',
          actualModel: 'llama-3-8b',
          metrics: { duration_ms: 10, prompt_tokens: 5, completion_tokens: 2, speed_tps: 200 }
        };
      }
      
      return {
        content: JSON.stringify([{ linea: 1, hallazgo: 'Error infinito' }]),
        actualModel: 'llama-3-8b',
        metrics: { duration_ms: 10, prompt_tokens: 5, completion_tokens: 2, speed_tps: 200 }
      };
    });

    // Should throw ConvergenceError because maxAttempts is 3 and it always fails
    await expect(
      runLocalAudit({
        targetPath: dummyFile,
        localUrl: 'http://localhost:1234/v1',
        localModel: 'llama-3-8b',
        maxAttempts: 3
      })
    ).rejects.toThrow(ConvergenceError);
  });

  it('debe ejecutar modo dry-run reportando hallazgos sin modificar archivos ni git', async () => {
    fs.writeFileSync(dummyFile, 'let x = 1;', 'utf8');

    // Make mockCallLLM return findings
    mockCallLLM.mockResolvedValue({
      content: JSON.stringify([{ linea: 1, hallazgo: 'Test hallazgo' }]),
      actualModel: 'llama-3-8b',
      metrics: { duration_ms: 10, prompt_tokens: 5, completion_tokens: 2, speed_tps: 200 }
    });

    const result = await runLocalAudit({
      targetPath: dummyFile,
      localUrl: 'http://localhost:1234/v1',
      localModel: 'llama-3-8b',
      maxAttempts: 3,
      dryRun: true
    });

    expect(result.status).toBe('DRY_RUN_COMPLETED');
    // Ensure all 4 stages ran once (4 calls) and NO autofix calls
    expect(mockCallLLM).toHaveBeenCalledTimes(4);
    // Code should remain untouched
    const finalCode = fs.readFileSync(dummyFile, 'utf8');
    expect(finalCode).toBe('let x = 1;');
    // No git calls for commits
    expect(mockExecSync).not.toHaveBeenCalledWith(expect.stringContaining('git commit'));
  });

  it('debe ejecutar solo las etapas especificadas (onlyStages)', async () => {
    fs.writeFileSync(dummyFile, 'let x = 1;', 'utf8');

    // Make mockCallLLM return clean passes
    mockCallLLM.mockResolvedValue({
      content: '[]',
      actualModel: 'llama-3-8b',
      metrics: { duration_ms: 10, prompt_tokens: 5, completion_tokens: 2, speed_tps: 200 }
    });

    const result = await runLocalAudit({
      targetPath: dummyFile,
      localUrl: 'http://localhost:1234/v1',
      localModel: 'llama-3-8b',
      maxAttempts: 3,
      onlyStages: ['security', 'semantic']
    });

    expect(result.status).toBe('APPROVED');
    // 2 stages * 3 loops = 6 calls
    expect(mockCallLLM).toHaveBeenCalledTimes(6);
  });

  it('debe saltar etapas ya cacheadas en modo incremental si el hash no cambia', async () => {
    fs.writeFileSync(dummyFile, 'let x = 1;', 'utf8');

    // Ensure empty mock returns
    mockCallLLM.mockResolvedValue({
      content: '[]',
      actualModel: 'llama-3-8b',
      metrics: { duration_ms: 10, prompt_tokens: 5, completion_tokens: 2, speed_tps: 200 }
    });

    // Run first audit with incremental enabled
    const result1 = await runLocalAudit({
      targetPath: dummyFile,
      localUrl: 'http://localhost:1234/v1',
      localModel: 'llama-3-8b',
      maxAttempts: 3,
      incremental: true
    });

    expect(result1.status).toBe('APPROVED');
    // All 4 stages ran 1 time, then cached for loops 2 and 3 = 4 calls
    expect(mockCallLLM).toHaveBeenCalledTimes(4);

    mockCallLLM.mockClear();

    // Run second audit with incremental enabled (same file content, so hash matches)
    const result2 = await runLocalAudit({
      targetPath: dummyFile,
      localUrl: 'http://localhost:1234/v1',
      localModel: 'llama-3-8b',
      maxAttempts: 3,
      incremental: true
    });

    expect(result2.status).toBe('APPROVED');
    // Since cache says it's clean, no LLM calls should be made
    expect(mockCallLLM).toHaveBeenCalledTimes(0);
  });
});
