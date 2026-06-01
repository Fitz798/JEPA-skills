# Result Schema (`.jsonl`)

One JSON object per prompt.

```json
{
  "id": "RQ01",
  "mode": "research_qa",
  "prompt": "...",
  "response_path": "optional file path to saved answer",
  "factual_correct": 1,
  "citation_hit": 1,
  "executable": null,
  "debug_hit": null,
  "hallucination": 0,
  "notes": "short evaluator note"
}
```

## Field rules

- `factual_correct`: `0|1|null`
- `citation_hit`: `0|1|null`
- `executable`: `0|1|null` (used mainly for reproduction prompts)
- `debug_hit`: `0|1|null` (used mainly for debug prompts)
- `hallucination`: `0|1` (`1` means invented paper/claim/command)

Use `null` when a metric is not applicable to that prompt type.

