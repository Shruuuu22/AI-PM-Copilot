import re
import pandas as pd
from pathlib import Path
from datetime import datetime

REQUIRED_COLS = ['feedback_id','date','customer_id','customer_segment','source','feedback_text','sentiment','account_value','plan','region']


def load_and_validate(path_or_buffer):
    if hasattr(path_or_buffer, 'read'):
        df = pd.read_csv(path_or_buffer)
    else:
        df = pd.read_csv(Path(path_or_buffer))
    report = {"Uploaded": len(df)}
    # basic validation
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    report['Missing Columns'] = missing
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    # drop blank rows
    before = len(df)
    df = df.dropna(subset=['feedback_text'])
    after = len(df)
    report['Valid'] = after
    report['Duplicates removed'] = before - after
    # parse dates
    def parse_date(d):
        try:
            return pd.to_datetime(d).date()
        except Exception:
            return pd.NaT
    df['date'] = df['date'].apply(parse_date)
    invalid_dates = df['date'].isna().sum()
    report['Invalid dates'] = int(invalid_dates)
    return df, report


def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return s
    s0 = s.strip()
    s0 = re.sub(r'\s+', ' ', s0)
    # basic PII redaction: emails, phones
    s0 = re.sub(r'[\w\.-]+@[\w\.-]+', '[REDACTED_EMAIL]', s0)
    s0 = re.sub(r'\+?\d[\d\-\s]{6,}\d', '[REDACTED_PHONE]', s0)
    return s0


def preprocess_feedback(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['clean_text'] = df['feedback_text'].astype(str).apply(clean_text)
    # simple duplicate detection on clean_text
    df['duplicate_of'] = df['clean_text'].duplicated(keep='first')
    # preserve original
    return df
