#!/usr/bin/env python
"""
Pipeline d'annotation automatique (spaCy + YAKE) pour le dataset GOLD.

Usage:
    python scripts/apply_annotation_pipeline.py \
        --input data/gold/dataset_ia/datasens_dataset_ia_*.parquet \
        --output-dir data/dataset/annotated \
        --spacy-model fr_core_news_md \
        --limit 0 \
        --write-db
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import spacy
import yake
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

UTC = timezone.utc
TIMESTAMP = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def detect_project_root(start: Path) -> Path:
    candidates = [start] + list(start.parents)
    for candidate in candidates:
        if (candidate / ".git").exists():
            return candidate.resolve()
    for candidate in candidates:
        if (candidate / "docker-compose.yml").exists() or (candidate / "pyproject.toml").exists():
            return candidate.resolve()
    for candidate in candidates:
        if (candidate / "docs").exists() and (candidate / "notebooks").exists():
            return candidate.resolve()
    return start.resolve()


def load_env(project_root: Path) -> None:
    env_path = project_root / ".env"
    if not load_dotenv(env_path):
        print(f"[WARN] Fichier .env introuvable à {env_path}. Variables système utilisées.", file=sys.stderr)


def discover_latest_dataset(dataset_dir: Path) -> Optional[Path]:
    candidates = list(dataset_dir.glob("datasens_gold_*ai_ready*.parquet"))
    if not candidates:
        candidates = list(dataset_dir.glob("datasens_gold_*.parquet"))
    if not candidates:
        candidates = list(dataset_dir.glob("datasens_dataset_ia_*.parquet"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


# ---------------------------------------------------------------------------
# Annotation logic
# ---------------------------------------------------------------------------

POSITIVE_WORDS = {
    "heureux",
    "joyeux",
    "satisfait",
    "optimiste",
    "positif",
    "confiant",
    "apaisé",
    "enthousiaste",
    "excellent",
    "favorable",
    "espoir",
    "espoir",
    "progrès",
}

NEGATIVE_WORDS = {
    "triste",
    "colère",
    "furieux",
    "angoissé",
    "crainte",
    "peur",
    "inquiet",
    "mécontent",
    "déçu",
    "critique",
    "crise",
    "tension",
    "stress",
}


@dataclass
class AnnotationResult:
    id_doc: int
    polarity: str
    intensity: float
    keywords: List[str]
    entities: List[Dict[str, str]]
    summary: str


class AnnotationEngine:
    def __init__(self, spacy_model: str = "fr_core_news_md") -> None:
        print(f"[INFO] Chargement modèle spaCy ({spacy_model})...")
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError as exc:
            raise RuntimeError(
                f"Modèle spaCy '{spacy_model}' introuvable. "
                "Installez-le avec : python -m spacy download fr_core_news_md"
            ) from exc

        print("[INFO] Initialisation YAKE...")
        self.kw_extractor = yake.KeywordExtractor(lan="fr", n=3, dedupLim=0.7, top=10, features=None)
        print("[OK] Moteurs spaCy et YAKE prêts")

    def annotate_text(self, text: str) -> AnnotationResult:
        doc = self.nlp(text)
        entities = [
            {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char} for ent in doc.ents
        ]

        keywords_raw = self.kw_extractor.extract_keywords(text)
        keywords = []
        for kw in keywords_raw:
            if len(kw) >= 2:
                try:
                    keywords.append(str(kw[1]))
                except (ValueError, TypeError):
                    continue

        polarity, intensity = self._estimate_sentiment([token.lemma_.lower() for token in doc if token.is_alpha])

        summary_parts = []
        if keywords:
            summary_parts.append(f"Keywords: {', '.join(keywords[:5])}")
        if entities:
            summary_parts.append(
                "Entities: "
                + ", ".join(f"{ent['text']} ({ent['label']})" for ent in entities[:5])
            )
        summary = " | ".join(summary_parts)

        return AnnotationResult(
            id_doc=-1,
            polarity=polarity,
            intensity=round(intensity, 3),
            keywords=keywords,
            entities=entities,
            summary=summary,
        )

    @staticmethod
    def _estimate_sentiment(tokens: List[str]) -> tuple[str, float]:
        if not tokens:
            return "neutre", 0.0
        positives = sum(1 for token in tokens if token in POSITIVE_WORDS)
        negatives = sum(1 for token in tokens if token in NEGATIVE_WORDS)
        total = positives + negatives

        if total == 0:
            return "neutre", 0.1

        polarity = "positive" if positives > negatives else "negative"
        if positives == negatives:
            polarity = "neutre"

        intensity = min(1.0, total / max(len(tokens), 1))
        return polarity, intensity


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def init_engine() -> Optional[Engine]:
    try:
        pg_host = os.getenv("POSTGRES_HOST", "localhost")
        pg_port = os.getenv("POSTGRES_PORT", "5432")
        pg_db = os.getenv("POSTGRES_DB", "datasens")
        pg_user = os.getenv("POSTGRES_USER", "ds_user")
        pg_pass = os.getenv("POSTGRES_PASS", "ds_pass")
        pg_url = f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
        engine = create_engine(pg_url, future=True)
        # quick test
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as exc:
        print(f"[WARN] Connexion PostgreSQL impossible : {exc}")
        return None


def upsert_annotations(engine: Engine, annotations: List[AnnotationResult], batch_tag: str) -> None:
    if not annotations:
        return
    with engine.begin() as conn:
        conn.execute(text("SET search_path TO datasens, public"))
        for ann in annotations:
            conn.execute(
                text(
                    """
                    INSERT INTO t05_annotation (id_doc, intensity, polarity, date_annotation, id_user)
                    VALUES (:id_doc, :intensity, :polarity, NOW(), NULL)
                    """
                ),
                {"id_doc": ann.id_doc, "intensity": ann.intensity, "polarity": ann.polarity},
            )
        conn.execute(
            text(
                """
                INSERT INTO t30_pipeline (nom, description, owner)
                VALUES (:nom, :desc, 'annotation_bot')
                ON CONFLICT DO NOTHING
                """
            ),
            {
                "nom": f"E2_ANNOTATION_{batch_tag}",
                "desc": "Pipeline automatique spaCy+YAKE",
            },
        )


# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------

def annotate_dataset(
    df: pd.DataFrame,
    engine: AnnotationEngine,
    limit: int = 0,
) -> pd.DataFrame:
    rows = []
    for idx, row in df.iterrows():
        text_value = str(row.get("texte") or row.get("texte_nettoye") or "")
        if not text_value.strip():
            rows.append(
                {
                    "annotation_keywords_yake": json.dumps([]),
                    "annotation_entities_spacy": json.dumps([]),
                    "annotation_polarity": "neutre",
                    "annotation_intensity": 0.0,
                    "annotation_summary": "",
                }
            )
            continue

        ann = engine.annotate_text(text_value)
        ann.id_doc = int(row.get("id_doc", -1))
        rows.append(
            {
                "annotation_keywords_yake": json.dumps(ann.keywords, ensure_ascii=False),
                "annotation_entities_spacy": json.dumps(ann.entities, ensure_ascii=False),
                "annotation_polarity": ann.polarity,
                "annotation_intensity": ann.intensity,
                "annotation_summary": ann.summary,
            }
        )

        if limit and idx + 1 >= limit:
            break

    annotations_df = pd.DataFrame(rows)
    result_df = pd.concat([df.reset_index(drop=True), annotations_df], axis=1)
    return result_df


def save_outputs(df: pd.DataFrame, output_dir: Path, base_name: str) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = output_dir / f"{base_name}.parquet"
    csv_path = output_dir / f"{base_name}.csv"

    df.to_parquet(parquet_path, index=False)
    df.to_csv(csv_path, index=False, encoding="utf-8")

    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "rows": len(df),
        "parquet": str(parquet_path),
        "csv": str(csv_path),
    }
    manifest_path = output_dir / f"{base_name}_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"parquet": str(parquet_path), "csv": str(csv_path), "manifest": str(manifest_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Annotation automatique spaCy + YAKE du dataset GOLD.")
    parser.add_argument("--input", type=Path, help="Chemin vers le dataset (Parquet/CSV).")
    parser.add_argument("--output-dir", type=Path, default=Path("data/dataset/annotated"))
    parser.add_argument("--spacy-model", default="fr_core_news_md")
    parser.add_argument("--limit", type=int, default=0, help="Limiter le nombre de lignes (0 = tout).")
    parser.add_argument("--write-db", action="store_true", help="Insérer les annotations dans PostgreSQL (t05_annotation).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = detect_project_root(Path.cwd())
    os.chdir(project_root)
    load_env(project_root)

    dataset_path = args.input
    dataset_dir = project_root / "data" / "dataset"
    if not dataset_path:
        dataset_path = discover_latest_dataset(dataset_dir)
        if not dataset_path:
            raise SystemExit(f"Aucun dataset trouvé dans {dataset_dir}")
    dataset_path = dataset_path.resolve()

    print(f"[INFO] Dataset utilisé : {dataset_path}")
    if dataset_path.suffix == ".parquet":
        df = pd.read_parquet(dataset_path)
    elif dataset_path.suffix == ".csv":
        df = pd.read_csv(dataset_path)
    else:
        raise SystemExit(f"Format non supporté : {dataset_path.suffix}")

    if args.limit and args.limit < len(df):
        df = df.head(args.limit)
        print(f"[INFO] Mode échantillon : {len(df)} lignes")

    engine = AnnotationEngine(spacy_model=args.spacy_model)
    annotated_df = annotate_dataset(df, engine, limit=0)

    base_name = f"datasens_gold_annotated_{TIMESTAMP}"
    outputs = save_outputs(annotated_df, args.output_dir, base_name)
    print(f"[OK] Dataset annoté écrit dans {outputs['parquet']} et {outputs['csv']}")

    if args.write_db:
        sql_engine = init_engine()
        if not sql_engine:
            print("[WARN] Impossible d'insérer les annotations en base (connexion échouée).")
        else:
            annotations = []
            for _, row in annotated_df.iterrows():
                try:
                    annotations.append(
                        AnnotationResult(
                            id_doc=int(row.get("id_doc")),
                            polarity=row.get("annotation_polarity", "neutre"),
                            intensity=float(row.get("annotation_intensity", 0.0)),
                            keywords=json.loads(row.get("annotation_keywords_yake", "[]")),
                            entities=json.loads(row.get("annotation_entities_spacy", "[]")),
                            summary=row.get("annotation_summary", ""),
                        )
                    )
                except Exception:
                    continue
            upsert_annotations(sql_engine, annotations, batch_tag=TIMESTAMP)
            print("[OK] Annotations insérées dans PostgreSQL (t05_annotation)")

    print("[DONE] Pipeline d'annotation terminé.")


if __name__ == "__main__":
    main()

