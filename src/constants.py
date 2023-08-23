import pickle

COLOR_DICT = { # We want to make colorless its own color. This labelling system makes all color combos distinct, which will be more difficult for the classifier
    (): 0, # Colorless
    ("W",): 1, # White
    ("U",): 2, # Blue
    ("B",): 3, # Black
    ("R",): 4, # Red
    ("G",): 5, # Green
    ("G", "W"): 6, # Selesnya
    ("U", "W"): 7, # Azorius
    ("B", "U"): 8, # Dimir
    ("B", "R"): 9, # Rakdos
    ("G", "R"): 10, # Gruul
    ("B", "G"): 11, # Golgari
    ("B", "W"): 12, # Orzhov
    ("G", "U"): 13, # Simic
    ("R", "U"): 14, # Izzet
    ("R", "W"): 15, # Boros
    ("B", "G", "R"): 16,  # Jund
    ("B", "G", "U"): 17,  # Sultai
    ("B", "G", "W"): 18,  # Abzan
    ("B", "R", "U"): 19,  # Grixis
    ("B", "R", "W"): 20,  # Mardu
    ("B", "U", "W"): 21,  # Esper
    ("G", "R", "U"): 22,  # Temur
    ("G", "R", "W"): 23,  # Naya
    ("G", "U", "W"): 24,  # Bant
    ("R", "U", "W"): 25,  # Jeskai
    ("B", "G", "R", "U"): 26, # Whiteless (Yidris)
    ("B", "G", "R", "W"): 27, # Blueless (Saskia)
    ("B", "G", "U", "W"): 28, # Redless (Atraxa)
    ("B", "R", "U", "W"): 29, # Greenless (Breya)
    ("G", "R", "U", "W"): 30, # Blackless (Aragorn)
    ("B", "G", "R", "U", "W"): 31 # 5-Color
}

COLOR_DICT_SHORT = {
    "": 0, # Colorless
    "W": 1, # White
    "U": 2, # Blue
    "B": 3, # Black
    "R": 4, # Red
    "G": 5, # Green
}

COLS_INCLUDE_ALL = ['colorIdentity', 'colors', 'firstPrinting', 'keywords', 'manaCost', 'manaValue',
                     'subtypes', 'supertypes', 'text', 'type', 'types', 'power', 'toughness',  'colorIndicator',
                     'name', 'hasAlternativeDeckLimit']

COLS_INCLUDE_NONCREATURE = ['loyalty',]

COLS_EDHREC = ["edhrecRank", "edhrecSaltiness"]

COLS_LEGALITY = ['legalities.commander', 'legalities.duel', 'legalities.explorer',
       'legalities.historic', 'legalities.historicbrawl', 'legalities.legacy',
       'legalities.modern', 'legalities.oathbreaker', 'legalities.pauper',
       'legalities.paupercommander', 'legalities.penny', 'legalities.pioneer',
       'legalities.vintage', 'legalities.gladiator','legalities.alchemy',
       'legalities.brawl', 'legalities.future', 'legalities.standard', 'legalities.predh',
       'legalities.premodern', 'legalities.oldschool',]

COLS_LEADERSHIP = ['leadershipSkills.brawl',
       'leadershipSkills.commander', 'leadershipSkills.oathbreaker',]

def to_feature_name(s: str, typ: bool = False) -> str:
    if typ:
        return "f_ct_" + s.lower().replace(" ", "_")
    return "f_kw_" + s.lower().replace(" ", "_")

# Legacy Keyword Lists, sourced from wikis
evergreen_keywords = ["Activate", "Attach", "Cast", "Counter", "Create", "Destroy", "Discard", "Exchange", "Exile", "Fight",
                       "Mill", "Play", "Reveal", "Sacrifice", "Scry", "Search", "Shuffle", "Tap", "Untap"]
my_common_words = ["Enchantment", "Artifact", "+1/+1", "Token", "Draw" "Land", "Nonland", "Spell", "Creature",]
evergreen_abilities = ["Deathtouch", "Defender", "Double Strike", "Enchant", "Equip", "First Strike", "Flash", "Flying",
                        "Haste", "Hexproof", "Indestructible", "Lifelink", "Menace", "Protection", "Reach", "Trample",
                          "Vigilance", "Ward", "Regenerate", "Shroud", "Intimidate", "Prowess"]
all_keywords = evergreen_keywords + my_common_words + evergreen_abilities

def get_kw_list(filename: str):
    """Get list of keywords from file"""
    with open(filename+".json") as f:
        json_data = json.load(f)
    data = json_data["data"]
    ability_words = data["abilityWords"]
    kw_abilities = data["keywordAbilities"]
    kw_actions = data["keywordActions"]
    all_kws = ability_words + kw_abilities + kw_actions
    return all_kws, ability_words, kw_abilities, kw_actions

def make_types_list(df: pd.DataFrame, n: int) -> None:
    """From a complete dataset, write a list of the 200 most common creature types to a file called common_types.txt"""
    all_types = []
    df["subtypes"].apply(all_types.extend)
    all_types = Counter(all_types)
    common_types = [x for x,y in all_types.most_common(n)]
    with open("./common_types.txt", "wb") as f:
        pickle.dump(common_types, f)

# all_kws, _, _, _ = get_kw_list("../data/mtg/Keywords")
ALL_KEYWORDS, _, _, _ = get_kw_list("./short_keywords")


with open("./common_types.txt", "rb") as f:
       COMMON_TYPES = pickle.load(f)