import type { Plugin } from "@opencode-ai/plugin"
import { createHash } from "node:crypto"
import { existsSync, readFileSync, mkdirSync, copyFileSync } from "node:fs"
import { join, resolve, basename, dirname } from "node:path"

/**
 * Fable Profile Plugin for OpenCode
 * 
 * Implements behavioral enforcement hooks from Fable 5 working style:
 * - Turn discipline (no ending on promises)
 * - Ground every claim (verify before reporting)
 * - Operating cadence (scale tool calls to complexity)
 * - Task discipline (maintain task lists)
 * - Mistake handling (acknowledge without collapse)
 * - Autonomy calibration (proceed without asking for reversible actions)
 * - Search persistence (continue until answered)
 * 
 * Also includes Auto-Backup hooks:
 * - Pre-write backup (before write/edit)
 * - Post-write verification (after write/edit)
 * - Automatic rollback if verification fails
 * 
 * Based on: https://github.com/rennf93/opus-fable-playbook
 *           https://github.com/elon-choo/fablever
 */

// ============================================================================
// Operating Cadence Tracking
// ============================================================================

const sessionToolCounts = new Map<string, number>()

function getSessionToolCount(sessionID: string): number {
  return sessionToolCounts.get(sessionID) || 0
}

function incrementToolCount(sessionID: string): number {
  const count = getSessionToolCount(sessionID) + 1
  sessionToolCounts.set(sessionID, count)
  return count
}

// ============================================================================
// Auto-Backup State
// ============================================================================

interface BackupState {
  backupPath: string
  originalHash: string
  expectedHash: string
  filePath: string
  resolvedPath: string
}

const pendingBackups = new Map<string, BackupState>()

function stateKey(sessionID: string, callID: string): string {
  return `${sessionID}:${callID}`
}

function calculateHash(content: string): string {
  return createHash("md5").update(content).digest("hex")
}

function backupFile(filePath: string, directory: string): {
  status: string
  backupPath?: string
  hash?: string
  error?: string
} {
  const fullPath = resolve(directory, filePath)

  if (!existsSync(fullPath)) {
    return { status: "skip", error: "File does not exist yet" }
  }

  const fileDir = dirname(fullPath)
  const backupDir = join(fileDir, ".backup")
  if (!existsSync(backupDir)) {
    mkdirSync(backupDir, { recursive: true })
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, "-")
  const fileName = basename(fullPath)
  const backupPath = join(backupDir, `${fileName}.${timestamp}.bak`)

  try {
    copyFileSync(fullPath, backupPath)
    const content = readFileSync(fullPath, "utf-8")
    return { status: "success", backupPath, hash: calculateHash(content) }
  } catch (err: any) {
    return { status: "error", error: err.message || String(err) }
  }
}

function verifyWrite(filePath: string, expectedHash: string): {
  valid: boolean
  actualHash?: string
  error?: string
} {
  try {
    if (!existsSync(filePath)) {
      return { valid: false, error: "File does not exist after write" }
    }
    const content = readFileSync(filePath, "utf-8")
    const actualHash = calculateHash(content)
    return { valid: actualHash === expectedHash, actualHash }
  } catch (err: any) {
    return { valid: false, error: err.message || String(err) }
  }
}

function rollbackFile(backupPath: string, targetPath: string): {
  status: string
  error?: string
} {
  try {
    if (!existsSync(backupPath)) {
      return { status: "error", error: "Backup file not found" }
    }
    copyFileSync(backupPath, targetPath)
    return { status: "success" }
  } catch (err: any) {
    return { status: "error", error: err.message || String(err) }
  }
}

function computeExpectedHash(args: any, tool: string, originalPath: string): string | null {
  try {
    if (tool === "write" && typeof args.content === "string") {
      return calculateHash(args.content)
    }
    if (tool === "edit" && typeof args.oldString === "string" && typeof args.newString === "string") {
      if (!existsSync(originalPath)) return null
      const original = readFileSync(originalPath, "utf-8")
      if (!original.includes(args.oldString)) return null
      const expected = original.replace(args.oldString, args.newString)
      return calculateHash(expected)
    }
    return null
  } catch {
    return null
  }
}

// ============================================================================
// Promise Detection (Turn Discipline)
// ============================================================================

const PROMISE_PATTERNS = [
  /I'll\s+/i,
  /Let me\s+/i,
  /Would you like me to/i,
  /Should I\s+/i,
  /Do you want me to/i,
  /I can\s+.*\?$/i,
  /Next steps?:/i,
  /To proceed:/i,
]

function endsOnPromise(response: string): boolean {
  const lastParagraph = response.split("\n\n").pop() || ""
  return PROMISE_PATTERNS.some(pattern => pattern.test(lastParagraph))
}

// ============================================================================
// Plugin Export
// ============================================================================

export const FableProfile: Plugin = async ({ directory }) => {
  return {
    // Hook 1: Pre-write backup + Operating cadence tracking
    "tool.execute.before": async (input, output) => {
      const sessionID = input.sessionID

      // Auto-Backup: Create backup before write/edit
      if (input.tool === "write" || input.tool === "edit") {
        const args = output.args
        if (args?.filePath) {
          const filePath = args.filePath as string
          if (!filePath.includes(".backup/") && !filePath.includes(".backup\\")) {
            const result = backupFile(filePath, directory)
            if (result.status === "success") {
              const resolvedPath = resolve(directory, filePath)
              const expectedHash = computeExpectedHash(args, input.tool, resolvedPath) || ""
              pendingBackups.set(stateKey(sessionID, input.callID), {
                backupPath: result.backupPath!,
                originalHash: result.hash!,
                expectedHash,
                filePath,
                resolvedPath
              })
              console.log(`[fable-backup] ✓ ${filePath}`)
            }
          }
        }
      }

      // Operating Cadence: Track tool call count
      if (input.tool !== "chat") {
        const count = incrementToolCount(sessionID)
        if (count === 1) {
          console.log("[fable-cadence]  Simple fact query. 1 tool call expected.")
        } else if (count === 3) {
          console.log("[fable-cadence]  Medium complexity. 3-5 tool calls appropriate.")
        } else if (count === 5) {
          console.log("[fable-cadence] 🎯 Deep research. 5-15 tool calls justified.")
        } else if (count === 15) {
          console.log("[fable-cadence] ⚠ High tool call count. Consider Research feature.")
        }
      }
    },

    // Hook 2: Post-write verification + Turn discipline check
    "tool.execute.after": async (input, output) => {
      const sessionID = input.sessionID

      // Auto-Backup: Verify write and rollback if failed
      if (input.tool === "write" || input.tool === "edit") {
        const key = stateKey(sessionID, input.callID)
        const state = pendingBackups.get(key)
        if (state) {
          pendingBackups.delete(key)
          if (state.expectedHash) {
            const result = verifyWrite(state.resolvedPath, state.expectedHash)
            if (result.valid) {
              console.log(`[fable-backup] ✓ verified ${state.filePath}`)
            } else {
              console.error(`[fable-backup]  verify failed ${state.filePath}: ${result.error || `hash ${result.actualHash} ≠ ${state.expectedHash}`}`)
              const rollback = rollbackFile(state.backupPath, state.resolvedPath)
              if (rollback.status === "success") {
                console.log(`[fable-backup] ↩ rollback ${state.filePath}`)
              } else {
                console.error(`[fable-backup] ✗ rollback failed: ${rollback.error}`)
              }
            }
          } else {
            console.log(`[fable-backup] ✓ ${state.filePath} (no hash to verify)`)
          }
        }
      }

      // Turn Discipline: Check if response ends on a promise
      if (input.tool === "chat") {
        const response = output.result as string
        if (response && typeof response === "string" && endsOnPromise(response)) {
          console.log("[fable-turn] ⚠ Response ends on a promise. Consider doing the work instead.")
        }
      }
    },

    // Hook 3: Session Start - Inject Fable reminder
    "session.created": async (input, output) => {
      console.log("[fable-profile] ✓ Fable working style active. Key principles:")
      console.log("  - Verify before responding (Fact-First Protocol)")
      console.log("  - Scale tool calls to complexity (1 vs 3-5 vs 5-15)")
      console.log("  - End on results, not promises (Turn Discipline)")
      console.log("  - Ground every claim in evidence")
      console.log("  - Maintain hierarchical task lists for non-trivial work")
      console.log("  - Auto-backup enabled (pre-write backup + post-write verification)")
    },

    // Hook 4: Pre-compact - Save context
    "experimental.session.compacting": async (input, output) => {
      console.log("[fable-profile] 💾 Session compacting. Ensure important decisions are saved to memory.")
    },

    // Hook 5: Chat message - Placeholder for future enhancements
    "chat.message": async (input, output) => {
      // Future: inject reminders or analyze messages
    },
  }
}

export default FableProfile
