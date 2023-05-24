from typing import Dict

import numpy as np
import pandas as pd

from test_utils.data import FRAMES
from tradeengine.dto.dataflow import Asset, TargetWeightOrder


def sample_strategy(signal_only=True) -> Dict[Asset, pd.Series | pd.DataFrame]:
    result = {}
    for a, f in FRAMES.items():
        df = f[["Close"]]
        df["ma20"] = df["Close"].rolling(20).mean()
        df["ma90"] = df["Close"].rolling(90).mean()
        df["signal"] = df["ma20"] - df["ma90"]
        df["signal"] = df["signal"].rolling(2).apply(lambda x: (np.sign(x[0]) != np.sign(x[1])) * np.sign(x[1]))

        df["order"] = df["signal"].apply(lambda x: {TargetWeightOrder: dict(size=0.49 if x > 0 else -0.49)} if x != 0 else None)

        result[a] = df["order"] if signal_only else df

    return result


def one_over_n() -> Dict[Asset, pd.DataFrame]:
    pass
