from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

class TimeAdjustService:

    # TODO convert from "8:30 pm ET"
    def convert_type_str_to_date(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, "%Y%m%d")

    def convert_tz_to_jst(self, datetime: datetime) -> datetime:
        return datetime.astimezone(ZoneInfo("Asia/Tokyo"))

    def convert_tz_to_est(self, datetime: datetime) -> datetime:
        return datetime.astimezone(ZoneInfo("America/New_York"))


    def combine_date_and_time(self, date_str: str, time_str: str) -> datetime:
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
