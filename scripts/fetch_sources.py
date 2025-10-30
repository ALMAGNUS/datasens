import pathlib
import requests
from typing import List


def download(urls: List[str], target_dir: str) -> None:
    path = pathlib.Path(target_dir)
    path.mkdir(parents=True, exist_ok=True)
    for url in urls:
        name = url.split("/")[-1]
        out = path / name
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        out.write_bytes(resp.content)
        print(f"Saved {out}")


if __name__ == "__main__":
    download([], "data/raw")


