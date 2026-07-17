import type { Plugin } from "@opencode-ai/plugin"

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
 * Based on: https://github.com/rennf93/opus-fable-playbook
 *           https://github.com/elon-choo/fablever
 */

// Track tool call count per session for operating cadence
const sessionToolCounts = new Map<string, number>()

function getSessionToolCount(sessionID: string): number {
  return sessionToolCounts.get(sessionID) || 0
}

function incrementToolCount(sessionID: string): number {
  const count = getSessionToolCount(sessionID) + 1
  sessionToolCounts.set(sessionID, count)
  return count
}

function resetToolCount(sessionID: string): void {
  sessionToolCounts.delete(sessionID)
}

export const FableProfile: Plugin = async ({ directory }) => {
  return {
    // Hook 1: Turn Discipline - Check if response ends on a promise
    "tool.execute.after": async (input, output) => {
      // Only check chat responses, not tool executions
      if (input.tool !== "chat") return

      const response = output.result as string
      if (!response || typeof response !== "string") return

      // Check for promise endings
      const promisePatterns = [
        /I'll\s+/i,
        /Let me\s+/i,
        /Would you like me to/i,
        /Should I\s+/i,
        /Do you want me to/i,
        /I can\s+.*\?$/i,
        /Next steps?:/i,
        /To proceed:/i,
      ]

      const lastParagraph = response.split("\n\n").pop() || ""
      const endsOnPromise = promisePatterns.some(pattern => pattern.test(lastParagraph))

      if (endsOnPromise) {
        console.log("[fable-profile]  Response ends on a promise. Consider doing the work instead.")
      }
    },

    // Hook 2: Operating Cadence - Track tool call complexity
    "tool.execute.before": async (input, output) => {
      const sessionID = input.sessionID

      // Reset count on new session
      if (getSessionToolCount(sessionID) === 0 && input.tool !== "chat") {
        console.log("[fable-profile] 📊 Session started. Tool calls will be tracked for operating cadence.")
      }

      // Increment and report
      if (input.tool !== "chat") {
        const count = incrementToolCount(sessionID)
        
        // Nudge at complexity thresholds
        if (count === 1) {
          console.log("[fable-profile] 🎯 Simple fact query. 1 tool call expected.")
        } else if (count === 3) {
          console.log("[fable-profile] 🎯 Medium complexity. 3-5 tool calls appropriate.")
        } else if (count === 5) {
          console.log("[fable-profile] 🎯 Deep research. 5-15 tool calls justified.")
        } else if (count === 15) {
          console.log("[fable-profile] ⚠ High tool call count. Consider if Research feature would be better.")
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
      console.log("  - Maintain task lists for non-trivial work")
    },

    // Hook 4: Pre-compact - Save context
    "experimental.session.compacting": async (input, output) => {
      console.log("[fable-profile] 💾 Session compacting. Ensure important decisions are saved to memory.")
    },

    // Hook 5: Chat message - Nudge toward Fable behavior
    "chat.message": async (input, output) => {
      // This hook can be used to inject reminders or analyze messages
      // For now, it's a no-op placeholder for future enhancements
    },
  }
}

export default FableProfile
