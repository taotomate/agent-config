/**
 * Robustly parses JSON from LLM output.
 */
function parseJsonResponse(text) {
  if (!text || typeof text !== 'string') return [];
  
  const trimmed = text.trim();
  
  // 1. Try direct parsing
  try {
    const parsed = JSON.parse(trimmed);
    if (Array.isArray(parsed)) return parsed;
  } catch (e) {}

  // 2. Try parsing contents of markdown code blocks
  const blockMatch = text.match(/```(?:json)?([\s\S]*?)```/);
  if (blockMatch) {
    try {
      const parsed = JSON.parse(blockMatch[1].trim());
      if (Array.isArray(parsed)) return parsed;
    } catch (e) {}
  }

  // 3. Try parsing using first '[' and last ']' boundaries
  const startIndex = text.indexOf('[');
  const endIndex = text.lastIndexOf(']');
  if (startIndex !== -1 && endIndex !== -1 && endIndex > startIndex) {
    try {
      const parsed = JSON.parse(text.substring(startIndex, endIndex + 1));
      if (Array.isArray(parsed)) return parsed;
    } catch (e) {}
  }

  return [];
}

function parseCleanCode(text) {
  if (!text || typeof text !== 'string') return '';

  const trimmed = text.trim();

  const firstIndex = trimmed.indexOf('```');
  const lastIndex = trimmed.lastIndexOf('```');

  if (firstIndex !== -1 && lastIndex !== -1 && lastIndex > firstIndex) {
    const codeSegment = trimmed.substring(firstIndex + 3, lastIndex);
    return codeSegment.replace(/^(javascript|typescript|js|ts)?\s*\n/i, '').trim();
  }

  return trimmed;
}

module.exports = {
  parseJsonResponse,
  parseCleanCode
};
