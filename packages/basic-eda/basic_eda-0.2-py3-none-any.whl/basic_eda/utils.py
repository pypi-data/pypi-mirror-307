import os
import sys
import typing as tp
import warnings
from pathlib import Path

import matplotlib.backends.backend_pdf
import pandas as pd
from joblib import Parallel
from tqdm import tqdm


def get_numeric_columns(df: pd.DataFrame) -> tp.List[str]:
    return df.select_dtypes(include=["number"]).columns.to_list()


def get_categorical_columns(df: pd.DataFrame) -> tp.List[str]:
    """Categorical columns are which are not numerical."""
    return list(set(df.columns.to_list()) - set(get_numeric_columns(df)))


def exclude_columns(columns: tp.List[str], excludes: tp.List[str]) -> tp.List[str]:
    return [col for col in columns if col not in excludes]


def get_grid_size(n: int, n_cols: int) -> tp.Tuple[int, int]:
    """
    Returns grid size for plotting multiple graphs. n is number of all figures.
    """
    n_cols = min(n_cols, n)
    n_rows = n // n_cols if n % n_cols == 0 else n // n_cols + 1
    return n_cols, n_rows


def text_truncator(text: str, n: int) -> str:
    """
    Truncates given text. It is useful for visualizing long texts.
    """
    return text[:n] + "..." if len(text) > n else text


def series_truncator(series: pd.Series, n_top: int) -> pd.Series:
    """
    Leaves only n_top frequent categorical values in given pd.Series;
    """

    # Check if series is numeric.
    # The meaning of "biufc": b bool, i int (signed), u unsigned int, f float, c complex.
    if series.dtype.kind in "biufc":
        return series

    values = set(series.value_counts()[:n_top].keys())
    truncated_series = series.apply(lambda x: x if x in values else "others")
    truncated_series = truncated_series.apply(lambda x: text_truncator(x, 12))

    return truncated_series


def save_as_pdf(figs, pdf_path: Path, orientation: str = "portrait") -> None:
    """Save list figures as PDF file."""
    pdf = matplotlib.backends.backend_pdf.PdfPages(pdf_path)
    for fig in figs:
        if fig is not None:
            pdf.savefig(fig, orientation=orientation)
    pdf.close()


def ignore_python_warnings():
    if not sys.warnoptions:
        warnings.simplefilter("ignore")
        os.environ["PYTHONWARNINGS"] = "ignore"  # Also affect subprocesses


def should_skip_pair(df: pd.DataFrame, col1: str, col2: str, target: tp.Optional[str] = None):
    mask = df[col1].notna() & df[col2].notna()
    if target is not None:
        mask &= df[target].notna()
    return mask.sum() == 0


class ProgressParallel(Parallel):
    """
    Util class for track progress of Parallel job.
    Example:
        from joblib import Parallel, delayed
        arr = list(range(100))
        parallel = ProgressParallel(n_jobs=-1, total=len(arr))
        func = lambda x: x ** 2
        with parallel:
            results = parallel(delayed(func)(x) for x in arr)
    """

    def __init__(self, use_tqdm=True, total=None, *args, **kwargs):
        self._use_tqdm = use_tqdm
        self._total = total
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        with tqdm(disable=not self._use_tqdm, total=self._total) as self._pbar:
            return Parallel.__call__(self, *args, **kwargs)

    def print_progress(self):
        if self._total is None:
            self._pbar.total = self.n_dispatched_tasks
        self._pbar.n = self.n_completed_tasks
        self._pbar.refresh()
