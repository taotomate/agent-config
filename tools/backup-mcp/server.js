import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import * as fs from "fs";
import * as path from "path";
import * as crypto from "crypto";

const BACKUP_DIR = ".mimocode/backups";

function calculateHash(content) {
  return crypto.createHash("md5").update(content).digest("hex");
}

const server = new McpServer({
  name: "backup-mcp",
  version: "1.0.0",
});

server.tool(
  "backup_file",
  "Create a backup of a file before modification",
  { file_path: z.string().describe("Path to the file to backup") },
  async ({ file_path }) => {
    const workspace = process.cwd();
    const fullPath = path.resolve(workspace, file_path);

    if (!fs.existsSync(fullPath)) {
      return { content: [{ type: "text", text: `File does not exist: ${file_path}` }] };
    }

    const backupDir = path.join(workspace, BACKUP_DIR);
    if (!fs.existsSync(backupDir)) {
      fs.mkdirSync(backupDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const fileName = path.basename(fullPath);
    const backupPath = path.join(backupDir, `${fileName}.${timestamp}.bak`);

    try {
      fs.copyFileSync(fullPath, backupPath);
      const content = fs.readFileSync(fullPath, "utf-8");
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            status: "success",
            backup_path: backupPath,
            original_path: fullPath,
            hash: calculateHash(content),
            size: content.length,
          }),
        }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `Backup failed: ${err.message}` }] };
    }
  }
);

server.tool(
  "verify_write",
  "Verify that a file was written correctly",
  {
    file_path: z.string().describe("Path to the file to verify"),
    expected_hash: z.string().optional().describe("Expected MD5 hash (optional)"),
    expected_content: z.string().optional().describe("Expected content (optional)"),
  },
  async ({ file_path, expected_hash, expected_content }) => {
    const workspace = process.cwd();
    const fullPath = path.resolve(workspace, file_path);

    if (!fs.existsSync(fullPath)) {
      return { content: [{ type: "text", text: JSON.stringify({ valid: false, reason: "File does not exist" }) }] };
    }

    const content = fs.readFileSync(fullPath, "utf-8");
    const actualHash = calculateHash(content);

    if (expected_hash && actualHash !== expected_hash) {
      return { content: [{ type: "text", text: JSON.stringify({ valid: false, reason: "Hash mismatch", expected: expected_hash, actual: actualHash }) }] };
    }

    if (expected_content && content !== expected_content) {
      return { content: [{ type: "text", text: JSON.stringify({ valid: false, reason: "Content mismatch" }) }] };
    }

    return { content: [{ type: "text", text: JSON.stringify({ valid: true, hash: actualHash, size: content.length }) }] };
  }
);

server.tool(
  "rollback_file",
  "Restore a file from backup",
  {
    backup_path: z.string().describe("Path to the backup file"),
    target_path: z.string().describe("Path to restore to"),
  },
  async ({ backup_path, target_path }) => {
    const workspace = process.cwd();
    const fullBackupPath = path.resolve(workspace, backup_path);
    const fullTargetPath = path.resolve(workspace, target_path);

    if (!fs.existsSync(fullBackupPath)) {
      return { content: [{ type: "text", text: `Backup file does not exist: ${backup_path}` }] };
    }

    try {
      fs.copyFileSync(fullBackupPath, fullTargetPath);
      return { content: [{ type: "text", text: JSON.stringify({ status: "success", restored: fullTargetPath }) }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Rollback failed: ${err.message}` }] };
    }
  }
);

server.tool(
  "list_backups",
  "List all backups in the backup directory",
  {},
  async () => {
    const workspace = process.cwd();
    const backupDir = path.join(workspace, BACKUP_DIR);

    if (!fs.existsSync(backupDir)) {
      return { content: [{ type: "text", text: JSON.stringify({ backups: [] }) }] };
    }

    const files = fs.readdirSync(backupDir).filter(f => f.endsWith(".bak"));
    const backups = files.map(f => {
      const stats = fs.statSync(path.join(backupDir, f));
      return { name: f, size: stats.size, modified: stats.mtime.toISOString() };
    });

    return { content: [{ type: "text", text: JSON.stringify({ backups }) }] };
  }
);

server.tool(
  "clean_backups",
  "Remove backups older than specified days",
  { older_than_days: z.number().describe("Remove backups older than this many days") },
  async ({ older_than_days }) => {
    const workspace = process.cwd();
    const backupDir = path.join(workspace, BACKUP_DIR);

    if (!fs.existsSync(backupDir)) {
      return { content: [{ type: "text", text: JSON.stringify({ removed: 0 }) }] };
    }

    const cutoff = Date.now() - older_than_days * 24 * 60 * 60 * 1000;
    const files = fs.readdirSync(backupDir).filter(f => f.endsWith(".bak"));
    let removed = 0;

    for (const f of files) {
      const filePath = path.join(backupDir, f);
      const stats = fs.statSync(filePath);
      if (stats.mtimeMs < cutoff) {
        fs.unlinkSync(filePath);
        removed++;
      }
    }

    return { content: [{ type: "text", text: JSON.stringify({ removed }) }] };
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("backup-mcp server running on stdio");
}

main().catch(console.error);
