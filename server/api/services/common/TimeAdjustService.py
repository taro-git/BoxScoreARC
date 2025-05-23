from datetime import datetime
from zoneinfo import ZoneInfo
import re

class TimeAdjustService:

    def convert_date_str_to_datetime(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, "%Y%m%d")
    
    def convert_time_str_to_datetime(self, time_str: str) -> datetime:
        time_str = time_str.strip()
        formatted_time_str = re.match(r"(\d{1,2}:\d{2}\s*(am|pm))\s*ET", time_str, re.IGNORECASE)
        if not formatted_time_str:
            raise ValueError(f"Invalid time format: {time_str}")
        
        naive_datetime = datetime.strptime(
            f"{datetime.now().date()} {formatted_time_str.group(1).lower()}",
            "%Y-%m-%d %I:%M %p"
        ).replace(tzinfo=ZoneInfo("America/New_York"))
        
        return naive_datetime

    def convert_tz_to_jst(self, datetime: datetime) -> datetime:
        return datetime.astimezone(ZoneInfo("Asia/Tokyo"))

    def convert_tz_to_est(self, datetime: datetime) -> datetime:
        return datetime.astimezone(ZoneInfo("America/New_York"))
    
    def today_jst(self) -> datetime.date:
        return datetime.now(ZoneInfo("Asia/Tokyo")).date()

