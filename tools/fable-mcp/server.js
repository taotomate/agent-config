#!/usr/bin/env node

/**
 * Fable Profile MCP Server
 * 
 * Zero-dependency MCP server implementing Fable 5 behavioral enforcement:
 * - fable_lint: Check if a message/plan complies with Fable rules
 * - fable_status: Report if Fable profile is active
 * - get_fable_profile: Return the steering profile
 * 
 * Based on: https://github.com/elon-choo/fablever
 * 
 * Usage: node server.js (stdio transport)
 */

import { createServer } from "node:http"

// Fable profile content (compact version)
const FABLE_PROFILE = `# Fable Working Style

You are working in the **Fable working style** — the disposition Claude Fable 5 brings to agentic work.

**Core principles:**
1. **Act when you have enough to act** — Don't re-derive facts, don't narrate options you won't pursue
2. **Lead with the outcome** — First sentence answers "what happened" or "what did you find"
3. **Don't over-build** — No features beyond what the task requires
4. **Report findings, then stop** — Don't apply fixes until asked
5. **Ground every progress claim** — Audit each claim against actual tool results
6. **Gate the deliverable** — Run acceptance check before presenting
7. **Keep a grounded decision trail** — Evidence ledger, not narrated reasoning
8. **Stop only when genuinely blocked** — Don't end on promises

**Verification scales with blast radius:**
- Trivial text edits: no test needed
- Local behavior changes: targeted checks
- Shared contracts/high-stakes: broader verification

**When any principle conflicts with safety/destructive action/explicit project rule → that constraint wins.**
`

// Fable lint rules
const LINT_RULES = [
  {
    id: "arrow-chain",
    pattern: /→|=>|->/g,
    message: "Avoid arrow chains (A → B → C). Use plain prose.",
    severity: "warning"
  },
  {
    id: "ending-on-permission",
    pattern: /(Would you like me to|Should I|Do you want me to|Can I)\?$/im,
    message: "Don't end on permission-asking. Do the work or stop.",
    severity: "error"
  },
  {
    id: "intent-without-action",
    pattern: /^(I'll|Let me|I will)\s+/im,
    message: "Don't narrate intent. Just do it.",
    severity: "warning"
  },
  {
    id: "scope-creep",
    pattern: /(while I'm at it|might as well|also fix|also add|also update)/i,
    message: "Don't add features beyond what the task requires.",
    severity: "warning"
  },
  {
    id: "over-formatting",
    pattern: /^(\*\*|##|\- |\d+\. ){5,}/m,
    message: "Avoid over-formatting. Use prose by default.",
    severity: "info"
  },
  {
    id: "filler-phrase",
    pattern: /^(Great question|Excellent point|Let me help|Sure!|Absolutely!)/im,
    message: "No filler phrases. State substance directly.",
    severity: "error"
  },
  {
    id: "promise-ending",
    pattern: /(I'll|Let me know when|Would you like me to)\s+.*$/im,
    message: "Don't end on a promise. End on a result or clear blocker.",
    severity: "error"
  }
]

// MCP server state
let isActive = true
let costMode = "auto"
let reviewerPreset = "claude-only"

// JSON-RPC 2.0 handler
function handleRequest(req, res) {
  let body = ""
  req.on("data", chunk => { body += chunk })
  req.on("end", () => {
    try {
      const request = JSON.parse(body)
      const response = handleMethod(request)
      res.writeHead(200, { "Content-Type": "application/json" })
      res.end(JSON.stringify(response))
    } catch (err) {
      res.writeHead(400, { "Content-Type": "application/json" })
      res.end(JSON.stringify({
        jsonrpc: "2.0",
        error: { code: -32700, message: "Parse error" },
        id: null
      }))
    }
  })
}

function handleMethod(request) {
  const { method, params, id } = request

  switch (method) {
    case "tools/list":
      return {
        jsonrpc: "2.0",
        result: {
          tools: [
            {
              name: "fable_lint",
              description: "Check if a draft message/plan complies with Fable principles",
              inputSchema: {
                type: "object",
                properties: {
                  text: { type: "string", description: "Text to lint" }
                },
                required: ["text"]
              }
            },
            {
              name: "fable_status",
              description: "Check if Fable profile is active and current settings",
              inputSchema: {
                type: "object",
                properties: {}
              }
            },
            {
              name: "get_fable_profile",
              description: "Get the Fable steering profile",
              inputSchema: {
                type: "object",
                properties: {
                  variant: {
                    type: "string",
                    enum: ["core", "compact", "full"],
                    default: "compact"
                  }
                }
              }
            }
          ]
        },
        id
      }

    case "tools/call":
      return handleToolCall(params, id)

    default:
      return {
        jsonrpc: "2.0",
        error: { code: -32601, message: `Method not found: ${method}` },
        id
      }
  }
}

function handleToolCall(params, id) {
  const { name, arguments: args } = params

  switch (name) {
    case "fable_lint":
      return lintText(args.text, id)

    case "fable_status":
      return {
        jsonrpc: "2.0",
        result: {
          content: [{
            type: "text",
            text: JSON.stringify({
              active: isActive,
              costMode,
              reviewerPreset,
              version: "1.0.0"
            }, null, 2)
          }]
        },
        id
      }

    case "get_fable_profile":
      const variant = args.variant || "compact"
      return {
        jsonrpc: "2.0",
        result: {
          content: [{
            type: "text",
            text: FABLE_PROFILE
          }]
        },
        id
      }

    default:
      return {
        jsonrpc: "2.0",
        error: { code: -32602, message: `Unknown tool: ${name}` },
        id
      }
  }
}

function lintText(text, id) {
  const violations = []

  for (const rule of LINT_RULES) {
    const matches = text.match(rule.pattern)
    if (matches) {
      violations.push({
        rule: rule.id,
        message: rule.message,
        severity: rule.severity,
        count: matches.length
      })
    }
  }

  const hasErrors = violations.some(v => v.severity === "error")
  const status = hasErrors ? "BLOCK" : "PASS"

  return {
    jsonrpc: "2.0",
    result: {
      content: [{
        type: "text",
        text: JSON.stringify({
          status,
          violations,
          summary: `${violations.length} issue(s) found`
        }, null, 2)
      }]
    },
    id
  }
}

// Start server
const PORT = process.env.FABLE_MCP_PORT || 3456
const server = createServer(handleRequest)

server.listen(PORT, () => {
  console.log(`[fable-mcp] Server listening on port ${PORT}`)
  console.log(`[fable-mcp] Tools: fable_lint, fable_status, get_fable_profile`)
})

// Graceful shutdown
process.on("SIGINT", () => {
  console.log("[fable-mcp] Shutting down...")
  server.close()
  process.exit(0)
})

process.on("SIGTERM", () => {
  console.log("[fable-mcp] Shutting down...")
  server.close()
  process.exit(0)
})
