from math import ceil
import datetime

def get_utc_offset():
    utc_now = datetime.datetime.utcnow()
    now = datetime.datetime.now()

    delta = now - utc_now

    hours, remainder = divmod(abs(delta.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)

    sign = '+' if delta >= datetime.timedelta(0) else '-'

    return f'{sign}{int(hours):02}:{int(minutes):02}'

def calculate_date_with_offset(date: str):
    if date.endswith('Z'):
        date = datetime.datetime.fromisoformat(date)
        offset = get_utc_offset()

        sign = 1 if offset[0] == '+' else -1
        hours = int(offset[1:3])
        minutes = int(offset[4:6])

        return (date + datetime.timedelta(hours=sign*hours, minutes=sign*minutes)).strftime('%Y-%m-%dT%H:%M:00') + offset
    
    return date


def total_pages(total_rows: int, rows_per_page: int) -> int:
    return ceil(total_rows / rows_per_page)