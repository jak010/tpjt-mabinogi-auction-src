from datetime import datetime, timedelta, timezone

TZ_KST = timezone(timedelta(hours=9))
current_kst = datetime.now(TZ_KST)
tomorrow = current_kst + timedelta(days=1, hours=6)


def today_midnigit():
    return current_kst.replace(hour=23, minute=59, second=59)


def get_day_after_two_days():
    return current_kst + timedelta(days=2)
