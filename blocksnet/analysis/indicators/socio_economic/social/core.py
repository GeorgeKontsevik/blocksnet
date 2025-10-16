import pandas as pd
from .indicator import SocialIndicator, SocialCountIndicator, SocialProvisionIndicator
from loguru import logger
from tqdm import tqdm
from .provision import calculate_provision
from .count import calculate_count
from ..utils import get_unique_parents
from ..const import TOTAL_COLUMN
from blocksnet.config import log_config
from blocksnet.analysis.services import services_count
from blocksnet.analysis.provision import provision_strong_total


def _calculate_social_indicators(
    counts_df: pd.DataFrame,
    prov_df: pd.DataFrame | None,
    indicator: SocialIndicator,
    blocks_ids: list[int] | None = None,
) -> tuple[float | None, float | None]:
    if blocks_ids is not None:
        counts_df = counts_df.loc[blocks_ids]
        if prov_df is not None:
            prov_df = prov_df.loc[blocks_ids]

    count = calculate_count(counts_df, indicator)
    if prov_df is not None:
        prov = provision_strong_total(prov_df)
    else:
        prov = None

    return count, prov


def _cast_social_indicator(indicator: SocialIndicator) -> tuple:

    from typing import cast

    name = indicator.name
    return SocialCountIndicator[name], SocialProvisionIndicator[name]


def calculate_social_indicators(blocks_df: pd.DataFrame, acc_mx: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    parents = get_unique_parents(blocks_df)

    counts_df = services_count(blocks_df)

    count_indicators = {p: {} for p in [*parents, TOTAL_COLUMN]}
    provision_indicators = {p: {} for p in [*parents, TOTAL_COLUMN]}

    for indicator in tqdm(list(SocialIndicator), disable=log_config.disable_tqdm):
        prov_df = calculate_provision(blocks_df, acc_mx, indicator)

        count_indicator, provision_indicator = _cast_social_indicator(indicator)

        for parent in parents:
            blocks_ids = blocks_df[blocks_df.parent == parent].index.to_list()
            count, prov = _calculate_social_indicators(counts_df, prov_df, indicator, blocks_ids)

            count_indicators[parent][count_indicator] = count
            provision_indicators[parent][provision_indicator] = prov

        count, prov = _calculate_social_indicators(counts_df, prov_df, indicator)
        count_indicators[TOTAL_COLUMN][count_indicator] = count
        provision_indicators[TOTAL_COLUMN][provision_indicator] = prov

    return (pd.DataFrame.from_dict(count_indicators), pd.DataFrame.from_dict(provision_indicators))
