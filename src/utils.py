import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
from typing import Any, Dict, List, Tuple, Union, Optional
import re

import matplotlib.pyplot as plt
import seaborn as sns

from lightgbm import LGBMClassifier, LGBMRegressor

from sklearn.metrics import (
    roc_auc_score,
    log_loss,
    brier_score_loss
)

nan_list = [None, [], {}, 'NaN', 'Null','NULL','None', 'none', 'nulo', 'NA','<NA>','NaT','?','-', '.','', ' ', '   ', 'unknown', 'Unknown','[unknown]']

def data_exploratory_analysis(data: pd.DataFrame) -> None:
    
    """
    Perform Data Brief inspection.
    """
    
    pd.set_option("display.max_columns", None)

    print("===== Data Inspection =====")

    print(f"\nShape:\n{data.shape}")

    print("\nData Types:")
    print(data.dtypes.to_string())
    
    print("Number of Null Rows:", data.isna().sum().sum())

    print("\nMissing Values:")
    print(data.isnull().sum().to_string())

    print("\nUnique Values:")
    print(data.nunique().to_string())

    repeated_rows = data[data.duplicated()]
    
    print(f"\nNumber of Repeated Rows: {len(repeated_rows)}")

    print("\n" + "="*40 + "\n")