############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

from typing import Tuple
from datetime import timezone as tzone, tzinfo
from datetime import datetime
from dateutil import tz


def DATE():
    try:
        now = datetime.now()
        return now.isoformat()
    except BaseException as e:
        print(f"[ERROR] lib_time.py<DATE>: {e}\n")
        raise e    

def TIME():
    return get_DATE("%H:%M:%S")

def get_UTC():
    try:
        now = datetime.now()
        return now.timestamp()
    except BaseException as e:
        print(f"[ERROR] lib_time.py<get_UTC>: {e}\n")
        raise e

def get_DATE(date_format: str="%Y-%m-%d %H:%M:%S"):
    try:
        now = datetime.now()
        return now.strftime(date_format)
    except BaseException as e:
        print(f"[ERROR] lib_time.py<get_DATE>: {e}\n")
        raise e

def get_ZONE() -> str:
    try:
        now = datetime.now().astimezone()
        zone_name = now.tzinfo.tzname(now)
        return zone_name
    except BaseException as e:
        print(f"[ERROR] lib_time.py<get_ZONE>: {e}\n")
        raise e
    
def get_UTC_time( local_date: str, timezone: str, date_format: str="%Y-%m-%d %H:%M:%S" ):
    try:
        return datetime.strptime(local_date + " " + timezone, date_format + " " + timezone)
        # return naive.replace(tzinfo=tzone.utc)
    except BaseException as e:
        print(f"[ERROR] lib_time.py<get_UTC_time>: {e}\n")
        raise e

def get_UTC_timestamp( local_date: str, timezone: str, date_format: str="%Y-%m-%d %H:%M:%S" ) -> float:
    try:
        utc = get_UTC_time( local_date, timezone, date_format )
        return utc.timestamp()
    except BaseException as e:
        print(f"[ERROR] lib_time.py<get_UTC_timestamp>: {e}\n")
        raise e

def cvt_utc( utc: float, date_format: str="%Y-%m-%d %H:%M:%S" ):
    try:
        d = datetime.fromtimestamp( utc, tz=None )
        return d.strftime( date_format )
    except BaseException as e:
        print(f"[ERROR] lib_time.py<cvt_utc>: {e}\n")
        raise e

def cvt_utc_DATE( utc: float, timezone: tzinfo=None, zone_utc: bool=False ) -> Tuple[str, str]:
    try:
        timezone = None
        if zone_utc is True:
            timezone = tzone.utc
            
        d = datetime.fromtimestamp( utc, tz=timezone )
        return f"{d.year:04}-{d.month:02}-{d.day:02}", f"{d.hour:02}:{d.minute:02}:{d.second:02}"
    except OSError as e:
        print(f"[ERROR] lib_time.py<cvt_utc_DATE>: {e}\n")
    except BaseException as e:
        print(f"[ERROR] lib_time.py<cvt_utc_DATE>: {e}\n")
        raise e

def cvt_DATE( from_date: str, from_tz: str, to_tz: str, utc_gap: float=0.0) -> Tuple[str, str]:
    try:
        to_tz = tz.gettz(to_tz)
        from_utc = get_UTC_timestamp(from_date, from_tz)
        date, time = cvt_utc_DATE( from_utc + utc_gap, to_tz )
        return date + " " + time
    except BaseException as e:
        print(f"[ERROR] lib_time.py<cvt_DATE>: {e}\n")
        raise e

def get_GAP( from_date: str, from_tz: str, to_date: str, to_tz: str ) -> float:
    try:
        utc_from = get_UTC_timestamp(from_date, from_tz)
        utc_to = get_UTC_timestamp(to_date, to_tz)
        return utc_to - utc_from
    except BaseException as e:
        print(f"[ERROR] lib_time.py<get_GAP>: {e}\n")
        raise e
    
