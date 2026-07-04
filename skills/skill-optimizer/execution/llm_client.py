import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

# Lookup order for OPENROUTER_API_KEY:
#   1. Already present in the environment (os.environ) — highest priority,
#      never overwritten. If you set it at Machine/User level on Windows
#      or export it in your shell, this just works with no .env at all.
#   2. SKILL_OPTIMIZER_ENV_PATH env var, if set, pointing at a .env file.
#   3. A .env file sitting next to this script (execution/.env).
#
# Previously this hardcoded D:\Engram_SDD\Hermes-Nous\hermes-data\.env —
# coupling skill-optimizer to a completely unrelated project's .env
# location, and breaking silently if Hermes-Nous moved or wasn't present
# on the machine. No hardcoded cross-project paths, per the "No hardcoded
# paths" principle already stated in skill_optimizer_lib.py's docstring.


def _default_env_path() -> Path:
    return Path(__file__).resolve().parent / ".env"


def load_env_vars() -> bool:
    """Load variables from a .env file into os.environ.

    Never overwrites a variable that's already set in the real
    environment — explicit env vars always win over .env file contents.
    """
    override_path = os.environ.get("SKILL_OPTIMIZER_ENV_PATH")
    env_path = Path(override_path) if override_path else _default_env_path()

    if not env_path.exists():
        return False

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            if key not in os.environ:
                os.environ[key] = val.strip()
    return True


def query_llm(model: str, prompt: str) -> dict | None:
    """
    Query the OpenRouter API with the given model and prompt.
    `model` may be a comma-separated fallback chain (tried in order).
    Returns a parsed dict from the model's JSON response, or None if
    every model in the chain fails (e.g. no API key, rate limits, all
    free routes currently unavailable).
    """
    load_env_vars()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in environment.", file=sys.stderr)
        return None

    url = "https://openrouter.ai/api/v1/chat/completions"

    # We ask the LLM to output ONLY JSON
    system_prompt = "You are an expert AI software architect evaluating a skill logic. Output strictly valid JSON without markdown wrapping."

    models = [m.strip() for m in model.split(",") if m.strip()]

    for current_model in models:
        data = {
            "model": current_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/taotomate",
            "X-Title": "Proj-Optimizer-Skill"
        }

        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                result = json.loads(response.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
                # It should be raw JSON, but strip markdown if the model hallucinates it
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]

                return json.loads(content.strip())

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"HTTP error querying {current_model}: {e.code} - {error_body}", file=sys.stderr)
            continue
        except urllib.error.URLError as e:
            print(f"Network error querying {current_model}: {e}", file=sys.stderr)
            continue
        except json.JSONDecodeError as e:
            print(f"JSON parsing error from {current_model}: {e}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"Unexpected error querying {current_model}: {e}", file=sys.stderr)
            continue

    print("All fallback models failed.", file=sys.stderr)
    return None


if __name__ == "__main__":
    # For simple CLI testing
    if len(sys.argv) > 2:
        res = query_llm(sys.argv[1], sys.argv[2])
        print(json.dumps(res))
    else:
        print("Usage: python llm_client.py <model> <prompt>")
