import pandas as pd
import frictionless as fl
from pathlib import Path
from slugify import slugify
import re


def create_ids(df, pattern="{}"):
    def to_id(row):
        id = "_".join(row)
        return slugify(pattern.format(id))

    ids = df.apply(to_id, axis=1)
    dups = ids.groupby(ids).rank(method="first", ascending=False).apply(lambda x: "" if x == 1 else str(int(x)))
    return ids + dups


def segment_sounds(col, sounds):
    def splitter(series, split_pattern):
        series = series.str.split(pat=split_pattern, regex=True)
        return series.apply(lambda x: " ".join([char for char in x if char]))

    defs = col == "#DEF#"
    split_pattern = re.compile("(" + "|".join(sorted(sounds, key=len, reverse=True)) + ")")
    segmented = col.copy()
    segmented[~defs] = splitter(segmented[~defs], split_pattern)
    return segmented


def read_table(name, package, **kwargs):
    """
    Reads Paralex tables.

    Parameters:
        name(str): A table's name.
        package: A frictionless Package.
        **kwargs: keyword arguments passed to `pandas.read_csv`
    Returns:
        a `pandas.DataFrame` containing the required table.
    """
    table_data = package.get_resource(name)
    paths = [table_data.path]
    if table_data.scheme == "multipart":
        paths.extend(table_data.extrapaths)
    return read_table_from_paths(paths, package, **kwargs)


def read_table_from_paths(paths, package, **kwargs):
    paths = paths if isinstance(paths, list) else [paths]
    return pd.concat(
        [pd.read_csv(Path(package.basepath) / path, **kwargs) for path in paths]
        , axis=0)
