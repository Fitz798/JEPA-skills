# Evidence Index Schema

This document defines the production schema for `metadata/evidence_index.csv`.

## Purpose

The evidence index is the structured backing store for traceable answers in the `jepa-research` skill. Each row represents one evidence item that can support one or more answer claims or actions.

The file is meant to answer two questions reliably:

1. What concrete artifact supports this claim or recommendation?
2. Where exactly inside that artifact should a reader look?

## File Contract

- Format: UTF-8 CSV with header row
- Filename: `metadata/evidence_index.csv`
- Template source: `metadata/evidence_index_template.csv`
- Primary key: `evidence_id`

Each row should describe one evidence item, not one entire answer.

## Schema

| Column | Required | Description |
|---|---|---|
| `evidence_id` | yes | Stable ID for the evidence row. Use `E####` format, for example `E0001`. |
| `evidence_type` | yes | One of `paper`, `code`, `protocol`, `log`, `table`, `figure`, `note`. |
| `paper_id` | conditional | Required when the evidence comes from or is anchored to a paper record in `papers_index.csv` or `paper_catalog.csv`. |
| `arxiv_id` | no | Optional paper identifier when available. |
| `code_id` | conditional | Required when the evidence comes from a code artifact in `code_index.csv`. |
| `artifact_path` | conditional | Repo-relative path or local corpus-relative path to the supporting artifact. Required for `protocol`, `log`, and `note`; recommended for every non-paper row. |
| `locator` | yes | Fine-grained pointer inside the artifact, such as page, section, figure, file, line, or log span. |
| `claim_summary` | yes | Short plain-language summary of the supported fact or recommendation. |
| `claim_scope` | yes | One of `fact`, `method`, `result`, `recommendation`, `failure_mode`, `procedure`. |
| `confidence` | yes | One of `high`, `medium`, `low`. This is confidence in the evidence linkage, not model confidence in a final answer. |
| `status` | yes | One of `verified`, `provisional`, `missing_locator`, `needs_review`. |
| `notes` | no | Free-form notes for caveats, ambiguities, or fill instructions. |

## Requiredness Rules

- `paper_id` is required for `paper`, `table`, and `figure` evidence tied to a paper.
- `code_id` is required for `code` evidence.
- `artifact_path` is required for `protocol`, `log`, and `note` evidence.
- At least one of `paper_id`, `code_id`, or `artifact_path` must be present.

## Allowed Values

### `evidence_type`

- `paper`: claim supported by paper text
- `code`: claim supported by repository code or config
- `protocol`: claim supported by a local protocol or template document
- `log`: claim supported by runtime output or experiment logs
- `table`: claim supported by a paper table
- `figure`: claim supported by a paper figure
- `note`: manually curated project note

### `claim_scope`

- `fact`: descriptive factual statement
- `method`: architecture, objective, masking, or training design statement
- `result`: metric, benchmark, or empirical outcome statement
- `recommendation`: suggested next action or tradeoff
- `failure_mode`: debugging or diagnosis evidence
- `procedure`: concrete run or evaluation step

### `status`

- `verified`: locator checked and usable
- `provisional`: row is usable but still needs a second pass
- `missing_locator`: source artifact is known but the exact location is not filled yet
- `needs_review`: row may be stale, ambiguous, or weakly linked

## Locator Format

Use short, machine-readable locator strings.

Preferred examples:

- paper page: `page:4`
- paper section: `section:3.2`
- paper page range: `page:4-5`
- figure: `figure:2`
- table: `table:1`
- code file: `file:src/train.py`
- code line range: `file:src/train.py#line:120-168`
- config key: `file:configs/ijepa.yaml#key:mask.scale`
- log span: `file:logs/run42.txt#line:1-40`

Avoid placeholder locators like `page:?` in production data. Use `status=missing_locator` if the artifact is known but the exact pointer is not yet available.

## Authoring Rules

1. One row should support one coherent claim summary.
2. Split broad evidence into multiple rows when they point to different locators.
3. Keep `claim_summary` short enough to reuse in answer drafting.
4. Prefer `verified` rows for final answers.
5. Do not use `note` evidence as the only support for factual paper claims.

## Mapping to Skill Outputs

The runtime answer format still uses compact answer-local IDs like `E1`, `E2`, and `E3`. Those answer-local IDs should point back to `evidence_id` rows in the evidence index or to an explicit local artifact path when the evidence index does not yet cover the case.

Recommended answer style:

```markdown
Evidence:
- E1 (paper): E0007 2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper
- E2 (code): E0042 corpus/code/archives/ijepa-main.zip -> file:src/train.py#line:120-168
```

## Starter Examples

```csv
evidence_id,evidence_type,paper_id,arxiv_id,code_id,artifact_path,locator,claim_summary,claim_scope,confidence,status,notes
E0001,paper,2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper,,,corpus/papers/all/2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper.pdf,page:1,I-JEPA is trained by predicting target block representations from context blocks,method,high,verified,
E0002,code,,,ijepa_main,corpus/code/archives/ijepa-main.zip,file:src/train.py#line:1-80,Training entrypoint and runtime wiring for I-JEPA reproduction,procedure,medium,provisional,Line locator assumes extracted archive path mapping is documented separately
E0003,protocol,,,,metadata/eval_protocol_template.md,section:reproduction,Local reproduction protocol template used for run planning,procedure,high,verified,
```

## Open-Source Guidance

The schema and template are safe to publish. The populated `evidence_index.csv` is also safe to publish if it references metadata and repo-relative locators only.

Be careful publishing rows that expose:

- private local absolute paths
- internal experiment logs
- proprietary notes
- third-party artifacts whose redistribution is restricted
