from datetime import datetime
from pandas import DateOffset

ALLOWED_TIMESTAMP_IN_YEARS = 1

ALLOWED_FORMAT = '%Y-%m-%d'

def datetime_input_allowed(date: datetime) -> bool:
   now = datetime.now()
   limit = now + DateOffset(years=ALLOWED_TIMESTAMP_IN_YEARS, days=1)
   return (now < date) and (date < limit)

def parse_and_check_datetime(date: str) -> tuple[datetime | None, str]:
  # Try parsing date
  try:
    parsed_datetime = datetime.strptime(date, '%Y-%m-%d')

    # Check if date in allowed range
    if not datetime_input_allowed(parsed_datetime):
       return None, 'Not allowed to pick this date'
    
    return parsed_datetime, ''

  # Invalid format
  except ValueError:
     return None, 'Invalid format'