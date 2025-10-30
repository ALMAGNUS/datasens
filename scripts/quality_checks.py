import pandas as pd
from typing import Dict


def basic_checks(df: pd.DataFrame) -> Dict[str, int]:
    return {
        "row_count": len(df),
        "null_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


if __name__ == "__main__":
    print("quality_checks: ready")


