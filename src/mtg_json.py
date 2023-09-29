import pandas as pd
import numpy as np
import seaborn as sns
from typing import Optional
import tensorflow as tf
from collections import Counter
import json
import pickle

from src.constants import to_feature_name, COLOR_DICT, COLS_INCLUDE_ALL, ALL_KEYWORDS, COMMON_TYPES

def load_atomic(filename: str) -> pd.DataFrame:
    """Load from the Atomic standard files into a dataframe resembling the old data standard."""
    with open("../data/mtg/"+filename+".json") as f:
        json_data = json.load(f)  # Load from file
    json_data = json_data["data"]
    cards = [x[0] for x in json_data.values() if len(x) == 1] # Pull only cards with 1 face (no transform, fuse, split, flip cards, sorry Delver)
    df = pd.json_normalize(cards)
    return df

def prep_df(df: pd.DataFrame, monocolor: bool, creatures: bool, legal_format: Optional[str] = None) -> pd.DataFrame:
    """
    Preprocesses card DF
    @param df: Input DataFrame
    @param monocolor: If true, return only cards with 1 or less color
    @param creatures: If true, return only creatures
    @param legal_format: Filter for only cards legal in the given format, if provided.
    """
    df["num_colors"] = df["colorIdentity"].map(len)
    if creatures:
        df = df.loc[df['type'].str.contains('Creature')]
    if monocolor:
        df = df.loc[df['num_colors'] <= 1]
    if legal_format:
        df = df.loc[df["legalities."+legal_format.lower()] == "Legal"]
    df = df[COLS_INCLUDE_ALL]
    df["f_is_artifact"] = df["supertypes"].apply(lambda x: 1 if "Artifact" in x else 0)
    df["f_is_enchantment"] = df["supertypes"].apply(lambda x: 1 if "Enchantment" in x else 0)
    df["f_cmc"] = (df["manaValue"] / 7.5) - 1  # [0,15] -> [-1, 1]
    df['f_pow'] = df['power'].replace({"1+*": 1, "*": "0", "*+1": 1}) # Assume all *'s are 0 (as per the rules)
    df['f_pow'] = ((df['f_pow'].astype(int) + 1) / 9) - 1 # [-1,16] -> [-1, 1]
    df['f_tough'] = df['toughness'].replace({"1+*": 1, "*": "0", "*+1": 1}) # Assume all *'s are 0 (as per the rules)
    df['f_tough'] = ((df['f_tough'].astype(int) + 1) / 9) - 1 # [-1,16] -> [-1, 1]

    df["label_identity"] = df["colorIdentity"].apply(lambda x: COLOR_DICT[tuple(x)]) # Could use 'colors' instead, but Kenrith should be classified as a 5C card, and Tasigur as Sultai.
    df["label_white"] = df["colorIdentity"].apply(lambda x: 1 if "W" in x else 0)
    df["label_blue"] = df["colorIdentity"].apply(lambda x: 1 if "U" in x else 0)
    df["label_black"] = df["colorIdentity"].apply(lambda x: 1 if "B" in x else 0)
    df["label_red"] = df["colorIdentity"].apply(lambda x: 1 if "R" in x else 0)
    df["label_green"] = df["colorIdentity"].apply(lambda x: 1 if "G" in x else 0)
    df["label_colorless"] = df["colorIdentity"].apply(lambda x: 1 if len(x) == 0 else 0)

    # Binary columns for types and keywords
    for kw in ALL_KEYWORDS:
        feature = to_feature_name(kw)
        df[feature] = df["text"].str.contains(kw, case=False, na=0).astype(int)  # This works, but Death's Shadow counts as a creature with Shadow. Could look into using reminder text?
    for typ in COMMON_TYPES:
        feature = to_feature_name(typ, True)
        df[feature] = df["subtypes"].apply(lambda x: 1 if typ in x else 0)
    df = df.set_index("name")
    return df

