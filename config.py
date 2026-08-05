from pathlib import Path
import json
import os

# =============================================================================
# Path & Data Directories
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RULES_FILE_PATH = os.path.join(DATA_DIR, "category_rules.json")


# =============================================================================
# Category Rules Management (JSON Storage)
# =============================================================================
def load_category_rules() -> dict:
    """Loads category mapping rules from the external JSON file.
    Creates a default file if it does not exist yet.
    """
    if not os.path.exists(RULES_FILE_PATH):
        os.makedirs(DATA_DIR, exist_ok=True)
        default_rules = {
            "Kõned": ["kõne", "call", "roaming call"],
            "Sõnumid": ["sms", "mms"],
            "Parkimine": ["park", "europark"],
            "Andmeside": ["internet", "data", "gb"],
        }
        save_category_rules(default_rules)
        return default_rules

    try:
        with open(RULES_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading category rules: {e}")
        return {}


def save_category_rules(rules: dict) -> bool:
    """Saves category mapping rules to the JSON file."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(RULES_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(rules, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving category rules: {e}")
        return False


# Export live CATEGORY_RULES dictionary
# CATEGORY_RULES = load_category_rules()

# Directory path
DATA_DIR = Path(__file__).resolve().parent / "data"

# Column Name Mappings
COL_SERVICE = "ARVEREA NIMETUS"
COL_RAW_SERVICE = "TEENUSED"
COL_PERIOD = "PERIOOD"
COL_COST = "SUMMA KM"
COL_CATEGORY = "KATEGOORIA"
COL_DATA = "MAHT"
COL_DURATION = "KESTUS"
COL_MINUTES = "KESTUS_MIN"
COL_NUMBER = "SIDEVAHEND"
COL_COUNT = "KOGUS"

# Table View Columns
DISPLAY_COLUMNS = [
    COL_SERVICE,
    COL_RAW_SERVICE,
    COL_CATEGORY,
    COL_COST,
    COL_PERIOD,
    COL_DATA,
    COL_DURATION,
    COL_NUMBER,
]

# Categorization Regex Rules
CATEGORY_RULES = [
    (r"kõne|paketitasu", "Kõned"),
    (r"sõnum", "Sõnumid"),
    (r"park", "Parkimine"),
    (r"värava", "IoT"),
    (r"koduinternet", "Kodune internet"),
    (r"internet|andmeside", "Mobiilne internet"),
    (r"standard|TeliaTV|digiboks", "TV standarpakett"),
    (r"videolaen", "TV videolaenutus"),
    (r"järel", "TV järelevaatamine"),            
]