import argparse
import json


def get_model_for_tier(tier: str) -> str:
    """Maps an abstract tier to a comma-separated OpenRouter fallback chain.

    OpenRouter's free-tier roster rotates constantly — providers add and
    remove ':free' routes without notice. Each chain below ends in
    'openrouter/free', an auto-router that picks whatever free model is
    currently available, as a last resort before the whole chain fails.
    If functional_score keeps coming back 0.0, re-check
    https://openrouter.ai/models for what's actually still free.

    Previously the same model ('google/gemma-4-26b-a4b-it:free') appeared
    in BOTH the fast and high chains — that's fixed here, each tier has
    its own non-overlapping list.
    """
    fast_models = (
        "meta-llama/llama-3.2-3b-instruct:free,"
        "openai/gpt-oss-20b:free,"
        "liquid/lfm-2.5-1.2b-instruct:free,"
        "openrouter/free"
    )
    high_models = (
        "meta-llama/llama-3.3-70b-instruct:free,"
        "nousresearch/hermes-3-llama-3.1-405b:free,"
        "google/gemma-4-26b-a4b-it:free,"
        "openai/gpt-oss-120b:free,"
        "openrouter/free"
    )

    if tier == "fast":
        return fast_models
    elif tier == "medium":
        return fast_models
    elif tier == "high":
        return high_models
    else:
        # Default to fast if unknown
        return fast_models


def main():
    parser = argparse.ArgumentParser(description="Resolve LLM model from tier")
    parser.add_argument("tier", type=str, help="Tier: fast, medium, high")
    args = parser.parse_args()

    model = get_model_for_tier(args.tier)
    output = {
        "status": "success",
        "data": {
            "model": model,
            "tier_requested": args.tier
        }
    }

    # Strictly output one JSON line as per project rules
    print(json.dumps(output))


if __name__ == "__main__":
    main()
