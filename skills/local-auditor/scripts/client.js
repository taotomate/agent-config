const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Helper to load api key from process.env or .env file
function getApiKey() {
  if (process.env.LM_STUDIO_API_KEY) return process.env.LM_STUDIO_API_KEY;
  if (process.env.LOCAL_LLM_API_KEY) return process.env.LOCAL_LLM_API_KEY;
  
  // Look in zettelkasten-daemon/.env
  try {
    const daemonEnvPath = 'd:/Engram_SDD/zettelkasten-daemon/.env';
    if (fs.existsSync(daemonEnvPath)) {
      const content = fs.readFileSync(daemonEnvPath, 'utf8');
      const match = content.match(/LM_STUDIO_API_KEY\s*=\s*(.+)/);
      if (match && match[1]) {
        return match[1].trim();
      }
    }
  } catch (e) {
    // Ignore error
  }
  return null;
}

/**
 * Call local LM Studio completion API with token metrics extraction.
 */
async function callLLM(endpointUrl, model, prompt, systemPrompt = 'You are a helpful assistant.') {
  const start = Date.now();
  
  const payload = {
    model: model,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: prompt }
    ],
    temperature: 0.1
  };
  
  const headers = { 'Content-Type': 'application/json' };
  const apiKey = getApiKey();
  if (apiKey) {
    headers['Authorization'] = `Bearer ${apiKey}`;
  }
  
  const response = await axios.post(`${endpointUrl}/chat/completions`, payload, { headers });
  
  const duration = Date.now() - start;
  
  const data = response.data;
  const choice = data.choices[0];
  const content = choice.message.content;
  const actualModel = data.model || model;
  
  const usage = data.usage || { prompt_tokens: 0, completion_tokens: 0 };
  const promptTokens = usage.prompt_tokens;
  const completionTokens = usage.completion_tokens;
  
  const speed = completionTokens > 0 ? (completionTokens / (duration / 1000)) : 0;
  
  return {
    content,
    actualModel,
    metrics: {
      duration_ms: duration,
      prompt_tokens: promptTokens,
      completion_tokens: completionTokens,
      speed_tps: parseFloat(speed.toFixed(2))
    }
  };
}

module.exports = {
  callLLM
};

