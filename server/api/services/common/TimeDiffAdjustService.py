from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def convert_est_to_jst(est_datetime: datetime) -> datetime:
    return est_datetime.astimezone(ZoneInfo("Asia/Tokyo"))


def convert_jst_to_est(jst_datetime: datetime) -> datetime:
    return jst_datetime.astimezone(ZoneInfo("America/New_York"))


def combine_date_and_time(date_str: str, time_str: str) -> datetime:
    """
    Combine date and time strings into a timezone-aware datetime (America/New_York).
    Assumes `time_str` ends with ' ET' or 'ET'.
    """
    # 1. "2025-05-14T00:00:00" -> "2025-05-14"
    date_clean = date_str[:10]

    # 2. "8:30 pm ET" -> "8:30 pm"
    time_clean = time_str.strip().replace(" ET", "").replace("ET", "")

    try:
        date_part = datetime.strptime(date_clean, "%Y-%m-%d")
        time_part = datetime.strptime(time_clean, "%I:%M %p")
        dt_naive = date_part.replace(hour=time_part.hour, minute=time_part.minute)

        # America/New_York でタイムゾーン指定（夏時間含む）
        return dt_naive.replace(tzinfo=ZoneInfo("America/New_York"))

    except Exception as e:
        print(f"[ERROR] combine_date_and_time failed: {date_str=}, {time_str=}, {e=}")
        # Fallback
        return datetime.strptime(date_clean, "%Y-%m-%d").replace(tzinfo=ZoneInfo("America/New_York"))
