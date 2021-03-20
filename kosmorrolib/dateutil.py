#!/usr/bin/env python3

from datetime import datetime, timezone, timedelta


def translate_to_timezone(date: datetime, to_tz: int, from_tz: int = None):
    if from_tz is not None:
        source_tz = timezone(timedelta(hours=from_tz))
    else:
        source_tz = timezone.utc

    return date.replace(tzinfo=source_tz).astimezone(
        tz=timezone(timedelta(hours=to_tz))
    )
