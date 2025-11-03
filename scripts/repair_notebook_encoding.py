import json
import sys
from pathlib import Path


def clean_string(s: str) -> str:
    # Remove lone surrogates and non-encodable chars by round-tripping
    return s.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")


def clean_obj(o):
    if isinstance(o, str):
        return clean_string(o)
    if isinstance(o, list):
        return [clean_obj(x) for x in o]
    if isinstance(o, dict):
        return {clean_obj(k): clean_obj(v) for k, v in o.items()}
    return o


def repair_notebook(path: Path) -> bool:
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        data = json.loads(raw)
    except Exception as e:
        print(f"[ERROR] Unable to read JSON: {e}")
        return False

    cleaned = clean_obj(data)
    try:
        path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return True
    except Exception as e:
        print(f"[ERROR] Unable to write repaired notebook: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/repair_notebook_encoding.py <notebook_path>")
        sys.exit(2)
    nb_path = Path(sys.argv[1])
    if not nb_path.exists():
        print(f"[ERROR] File not found: {nb_path}")
        sys.exit(1)
    if repair_notebook(nb_path):
        print(f"[OK] Repaired: {nb_path}")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()


