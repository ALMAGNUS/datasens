import pathlib


def export_html(report_html: str, out_path: str = "docs/dashboard.html") -> None:
    path = pathlib.Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report_html, encoding="utf-8")


if __name__ == "__main__":
    export_html("<h1>DataSens</h1>")
    print("Dashboard exported.")


