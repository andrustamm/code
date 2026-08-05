# utils/formatters.py
import pandas as pd


def format_period_string(val) -> str:
    """Parses PERIOOD values into YYYY-MM format."""
    if pd.isna(val):
        return "Teadmata"
    val_str = str(val).strip()

    parsed = pd.to_datetime(val_str, dayfirst=True, errors="coerce")
    if pd.notna(parsed):
        return parsed.strftime("%Y-%m")

    if len(val_str) >= 7:
        return val_str[:7]
    return val_str


def parse_duration_to_minutes(val) -> float:
    """Parses duration string in hh:mm:ss format to total float minutes."""
    if pd.isna(val):
        return 0.0
    val_str = str(val).strip()
    try:
        td = pd.to_timedelta(val_str)
        return td.total_seconds() / 60.0
    except Exception:
        return 0.0


def format_minutes_to_hm(minutes: float) -> str:
    """Formats float minutes into 'xxH yyM' string representation."""
    if pd.isna(minutes) or minutes <= 0:
        return "0t 00m"
    total_minutes = int(round(minutes))
    hours = total_minutes // 60
    mins = total_minutes % 60
    return f"{hours}t {mins:02d}m"


def format_bytes(gb_val: float) -> str:
    """Formats values (stored in GB) into readable GB/MB string format."""
    if pd.isna(gb_val) or gb_val <= 0:
        return "0 MB"
    if gb_val >= 1.0:
        return f"{gb_val:.2f} GB"
    mb_val = gb_val * 1024
    return f"{mb_val:.1f} MB"