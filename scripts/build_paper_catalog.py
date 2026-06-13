import argparse
import csv
from pathlib import Path


CORE_OVERRIDES = {
    "unk_tutorial_on_joint_embedding_predictive_architectures_jepa_foundations_applications_and_future_directions": {
        "modality": "general",
        "task": "tutorial and survey",
        "evidence_level": "secondary",
        "code_id": "",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "no_known_local_code",
        "link_confidence": "medium",
        "notes": "Local corpus contains paper coverage but no dedicated tutorial code archive",
    },
    "2020_neurips_2020_bootstrap_your_own_latent_a_new_approach_to_self_supervised_learning_paper_pdf": {
        "modality": "vision",
        "task": "self-supervised representation learning baseline",
        "evidence_level": "secondary",
        "code_id": "",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "no_known_local_code",
        "link_confidence": "medium",
        "notes": "No BYOL-specific local archive in metadata/code_index.csv",
    },
    "2022_a_path_towards_autonomous_machine_intelligence": {
        "modality": "general",
        "task": "conceptual framing for world models",
        "evidence_level": "secondary",
        "code_id": "",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "no_known_local_code",
        "link_confidence": "medium",
        "notes": "Conceptual framing paper without a corresponding local implementation archive",
    },
    "2023_assran_self_supervised_learning_from_images_with_a_joint_embedding_predictive_architecture_cvpr_2023_paper": {
        "modality": "vision",
        "task": "self-supervised image representation learning",
        "evidence_level": "primary",
        "code_id": "ijepa_main",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "exact_local_match",
        "link_confidence": "high",
        "notes": "Local ijepa archive name and train script align with the I-JEPA paper",
    },
    "2023_mc_jepa_a_joint_embedding_predictive_architecture_for_self_supervised_learning_of_motion_and_content_features": {
        "modality": "video",
        "task": "motion and content representation learning",
        "evidence_level": "primary",
        "code_id": "",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "multiple_local_candidates",
        "link_confidence": "low",
        "notes": "Possible family-level overlap with eb_jepa_main or h_jepa_main but no exact confirmed match yet",
    },
    "2025_audio_jepa_joint_embedding_predictive_architecture_for_audio_representation_learning": {
        "modality": "audio",
        "task": "audio representation learning",
        "evidence_level": "primary",
        "code_id": "",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "no_known_local_code",
        "link_confidence": "medium",
        "notes": "No audio-specific JEPA archive is currently indexed locally",
    },
    "2025_v_jepa_2_self_supervised_video_models_enable_understanding_prediction_and_planning": {
        "modality": "video",
        "task": "video understanding prediction and planning",
        "evidence_level": "primary",
        "code_id": "jepa_main",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "family_match_only",
        "link_confidence": "medium",
        "notes": "Local archive contains a V-JEPA training path but direct version match to V-JEPA-2 is not confirmed",
    },
    "2026_parallel_stochastic_gradient_based_planning_for_world_models": {
        "modality": "general",
        "task": "planning for world models",
        "evidence_level": "secondary",
        "code_id": "",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "no_known_local_code",
        "link_confidence": "medium",
        "notes": "Planning paper has no dedicated local code archive indexed yet",
    },
    "2026_rectified_lpjepa_joint_embedding_predictive_architectures_with_sparse_and_maximum_entropy_representations": {
        "modality": "general",
        "task": "predictive representation learning variants",
        "evidence_level": "primary",
        "code_id": "lejepa_main",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "family_match_only",
        "link_confidence": "low",
        "notes": "LeJEPA archive may be method-family relevant but rectified LpJEPA equivalence is unconfirmed",
    },
    "2026_thinkjepa_empowering_latent_world_models_with_large_vision_language_reasoning_model": {
        "modality": "multimodal",
        "task": "latent world model reasoning",
        "evidence_level": "primary",
        "code_id": "",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "no_known_local_code",
        "link_confidence": "medium",
        "notes": "No local archive clearly matches ThinkJEPA",
    },
    "2026_v_jepa2_1_unlocking_dense_features_in_video": {
        "modality": "video",
        "task": "dense video feature learning",
        "evidence_level": "primary",
        "code_id": "",
        "code_repo_url": "",
        "code_commit": "",
        "code_link_status": "multiple_local_candidates",
        "link_confidence": "low",
        "notes": "Both jepa_main and jepa_main2 appear V-JEPA-related but neither is confirmed as the V-JEPA2.1 implementation",
    },
}


LONG_TAIL_OVERRIDES = {
    "arxiv_2508.02829": {
        "modality": "vision",
        "task": "feature normalization analysis for i-jepa",
        "evidence_level": "analysis",
    },
    "arxiv_2509.12249": {
        "modality": "vision",
        "task": "auxiliary objective ablation for jepa representations",
        "evidence_level": "analysis",
    },
    "arxiv_2509.15470": {
        "modality": "multimodal",
        "task": "multimodal imaging and clinical representation learning",
        "evidence_level": "primary",
    },
    "arxiv_2509.23238": {
        "modality": "audio",
        "task": "audio foundation model representation learning",
        "evidence_level": "primary",
    },
    "arxiv_2512.07168": {
        "modality": "audio",
        "task": "speech representation learning with adaptive attention",
        "evidence_level": "primary",
    },
    "arxiv_2512.10942": {
        "modality": "multimodal",
        "task": "vision-language representation learning",
        "evidence_level": "primary",
    },
    "arxiv_2601.00844": {
        "modality": "general",
        "task": "value-guided action planning with jepa world models",
        "evidence_level": "primary",
    },
    "arxiv_2601.14354": {
        "modality": "video",
        "task": "probabilistic world model with variational jepa",
        "evidence_level": "analysis",
    },
    "arxiv_2605.15466": {
        "modality": "video",
        "task": "interaction-aware masking for causal video prediction",
        "evidence_level": "analysis",
    },
    "arxiv_2605.17165": {
        "modality": "video",
        "task": "auxiliary objective study for video jepa",
        "evidence_level": "analysis",
    },
    "arxiv_2605.25313": {
        "modality": "general",
        "task": "predictive world models in belief space",
        "evidence_level": "primary",
    },
}


def arxiv_url(arxiv_id: str) -> str:
    aid = (arxiv_id or "").strip()
    if not aid:
        return ""
    return f"https://arxiv.org/abs/{aid}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a shareable paper catalog from local papers index.")
    parser.add_argument("--input", required=True, help="Input CSV: papers_index.csv")
    parser.add_argument("--output", required=True, help="Output CSV: paper_catalog.csv")
    args = parser.parse_args()

    inp = Path(args.input)
    out = Path(args.output)

    with inp.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    fieldnames = [
        "paper_id",
        "title",
        "year",
        "arxiv_id",
        "source_url",
        "tier",
        "source_file",
        "paper_path",
        "modality",
        "task",
        "evidence_level",
        "code_id",
        "code_repo_url",
        "code_commit",
        "code_link_status",
        "link_confidence",
        "citation_key",
        "notes",
    ]

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            pid = r.get("paper_id", "")
            arxiv_id = r.get("arxiv_id", "")
            title = r.get("title_guess", "")
            year = r.get("year_guess", "")
            tier = r.get("tier", "")
            source_file = r.get("current_name", "")
            paper_path = (r.get("relative_path", "") or "").replace(".\\", "")
            citation_key = (pid or "").replace("arxiv_", "arxiv")
            override = {}
            override.update(LONG_TAIL_OVERRIDES.get(pid, {}))
            override.update(CORE_OVERRIDES.get(pid, {}))
            writer.writerow(
                {
                    "paper_id": pid,
                    "title": title,
                    "year": year,
                    "arxiv_id": arxiv_id,
                    "source_url": arxiv_url(arxiv_id),
                    "tier": tier,
                    "source_file": source_file,
                    "paper_path": paper_path,
                    "modality": override.get("modality", ""),
                    "task": override.get("task", ""),
                    "evidence_level": override.get("evidence_level", ""),
                    "code_id": override.get("code_id", ""),
                    "code_repo_url": override.get("code_repo_url", ""),
                    "code_commit": override.get("code_commit", ""),
                    "code_link_status": override.get("code_link_status", ""),
                    "link_confidence": override.get("link_confidence", ""),
                    "citation_key": citation_key,
                    "notes": override.get("notes", ""),
                }
            )

    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
