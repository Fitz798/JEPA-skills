# Paper-Code Linking Policy

This document defines how `metadata/paper_catalog.csv` should express links between paper records and local code artifacts.

## Goal

Paper-code links should help reproduction and debugging without overstating certainty.

The catalog must distinguish between:

- exact local matches
- family-level but ambiguous candidates
- no known local code

## Fields

Use these `paper_catalog.csv` fields together:

- `code_id`
- `code_link_status`
- `link_confidence`
- `notes`

## Allowed `code_link_status` Values

- `exact_local_match`: the local archive is a confident direct match for the paper
- `family_match_only`: the local archive is relevant to the same method family, but not confirmed as the paper's direct implementation
- `multiple_local_candidates`: more than one local archive may be relevant and no single one should be preferred yet
- `no_known_local_code`: no matching local archive is currently known in `metadata/code_index.csv`

## Fill Rules

1. Set `code_id` only when one local archive is the best current choice.
2. Use `exact_local_match` only when the archive name or contents strongly support the mapping.
3. Use `family_match_only` when the archive is relevant but version, variant, or authorship is uncertain.
4. Use `multiple_local_candidates` when several archives are plausible and manual review is still needed.
5. Use `no_known_local_code` when nothing in `metadata/code_index.csv` is a reasonable match.
6. Use `notes` to explain ambiguous mappings.

## Current Conservative Policy for v1.2.0

For this release, prefer under-linking to over-linking.

- Exact I-JEPA mapping is acceptable when linked to `ijepa_main`.
- Other core papers should remain explicitly unresolved unless the local archive clearly matches.
- Do not treat a same-family archive as an exact implementation unless the evidence is strong.
