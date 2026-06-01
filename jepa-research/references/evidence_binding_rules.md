# Evidence Binding Rules (v1.1.0)

Use these rules to improve citation quality and traceability.

## Minimum requirement by mode

- `research_qa`: at least 2 paper evidence items.
- `reproduction_plan`: at least 1 paper + 1 code/protocol evidence item.
- `debug_triage`: at least 1 code/protocol evidence item; add paper evidence when method-specific.
- `writing_citation`: every claim must map to at least one paper evidence item.

## Evidence item format

Use compact IDs:

```markdown
Evidence:
- E1 (paper): 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (protocol): metadata/eval_protocol_template.md
```

## Mapping format

```markdown
Actions/Claims:
- A1: lower batch size
- A2: enable AMP

Mapping:
- A1 -> E2
- A2 -> E2
```

## Missing evidence handling

When evidence is unavailable:

```markdown
Mapping:
- A3 -> missing_evidence
```

Then ask for the specific missing artifact (config/log/commit).

## Quality checks before finalizing

1. Does every concrete action/claim have a mapping entry?
2. Do evidence entries point to real local IDs/paths?
3. Is at least one non-paper source used for debug/reproduction answers?
4. Are uncertain claims marked with lower confidence?

