# OpenRouter Free Models — Complete List (2026-06-08)

Source: https://openrouter.ai/api/v1/models (filtered by pricing=free)
Total: 27 free models

## By Context Length (descending)

| Model | Context | Category | Input | Output |
|-------|---------|----------|-------|--------|
| owl-alpha | 1,048,756 | agentic | text | text |
| lyria-3-pro-preview | 1,048,576 | audio | text,image | text,audio |
| lyria-3-clip-preview | 1,048,576 | audio | text,image | text,audio |
| qwen3-coder:free | 1,048,576 | coding | text | text |
| nemotron-3-ultra-550b-a55b:free | 1,000,000 | general | text | text |
| nemotron-3-super-120b-a12b:free | 1,000,000 | general | text | text |
| laguna-xs.2:free | 262,144 | coding | text | text |
| laguna-m.1:free | 262,144 | coding | text | text |
| kimi-k2.6:free | 262,144 | coding | text,image | text |
| gemma-4-26b-a4b-it:free | 262,144 | general | image,text,video | text |
| gemma-4-31b-it:free | 262,144 | multimodal | image,text,video | text |
| qwen3-next-80b-a3b-instruct:free | 262,144 | lightweight | text | text |
| nemotron-3-nano-omni-30b-a3b-reasoning:free | 256,000 | multimodal | text,audio,image,video | text |
| nemotron-3-nano-30b-a3b:free | 256,000 | lightweight | text | text |
| openrouter/free | 200,000 | general | text,image | text |
| gpt-oss-120b:free | 131,072 | agentic | text | text |
| gpt-oss-20b:free | 131,072 | agentic | text | text |
| glm-4.5-air:free | 131,072 | chat | text | text |
| llama-3.3-70b-instruct:free | 131,072 | chat | text | text |
| llama-3.2-3b-instruct:free | 131,072 | lightweight | text | text |
| hermes-3-llama-3.1-405b:free | 131,072 | agentic | text | text |
| nemotron-3.5-content-safety:free | 128,000 | safety | text,image | text |
| nemotron-nano-12b-v2-vl:free | 128,000 | multimodal | image,text,video | text |
| nemotron-nano-9b-v2:free | 128,000 | lightweight | text | text |
| lfm-2.5-1.2b-thinking:free | 32,768 | reasoning | text | text |
| lfm-2.5-1.2b-instruct:free | 32,768 | chat | text | text |
| dolphin-mistral-24b-venice-edition:free | 32,768 | chat | text | text |

## Notes
- All models have prompt: "0" and completion: "0" pricing
- :free suffix in model ID indicates free tier
- openrouter/free is a meta-router that randomly selects from available free models
- NVIDIA Nemotron models are new additions (2026)
- Audio models (Lyria) have per-song/per-clip pricing despite being listed as free

## Update
Run python update_models_db.py in D:\Engram_SDD\Proj-youtube-scraper-v2\ to refresh.
