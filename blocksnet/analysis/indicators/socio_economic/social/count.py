import pandas as pd
from .indicator import SocialIndicator


def calculate_count(count_df: pd.DataFrame, indicator: SocialIndicator) -> float | None:
    name = indicator.meta.name

    column = f"count_{name}"
    if column in count_df.columns:
        count = count_df[column].sum()
        return int(count)

    return None
