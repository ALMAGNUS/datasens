import json
import pathlib
from datetime import datetime


def write_snapshot(manifest_dir: str = "logs", docs_dir: str = "docs") -> None:
    ts = datetime.now()
    day = ts.strftime("%Y%m%d")
    manifest_path = pathlib.Path(manifest_dir) / f"manifest_{day}.json"
    content = {
        "milestone": "snapshot",
        "date": ts.isoformat(),
    }
    manifest_path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    readme = pathlib.Path(docs_dir) / "README_project_timeline.md"
    readme.write_text("# DataSens Project Timeline\n\nUpdated: " + ts.isoformat(), encoding="utf-8")


if __name__ == "__main__":
    write_snapshot()
    print("Snapshot and README updated.")


