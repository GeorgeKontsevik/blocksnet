import pandas as pd
from .indicator import SocialIndicator
from blocksnet.analysis.provision import competitive_provision
from blocksnet.config import log_config, service_types_config


def calculate_provision(
    blocks_df: pd.DataFrame, acc_mx: pd.DataFrame, indicator: SocialIndicator
) -> pd.DataFrame | None:

    name = indicator.meta.name

    if not name in service_types_config:
        return None

    column = f"capacity_{indicator.meta.name}"
    if not column in blocks_df.columns:
        return None

    disable_tqdm = log_config.disable_tqdm
    logger_level = log_config.logger_level
    log_config.set_disable_tqdm(True)
    log_config.set_logger_level("ERROR")

    _, demand, accessibility = service_types_config[name].values()
    df = blocks_df.rename(columns={column: "capacity"})
    prov_df, _ = competitive_provision(df, acc_mx, accessibility, demand)

    log_config.set_disable_tqdm(disable_tqdm)
    log_config.set_logger_level(logger_level)

    return prov_df
