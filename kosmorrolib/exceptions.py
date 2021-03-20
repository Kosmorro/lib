#!/usr/bin/env python3

from datetime import date


class UnavailableFeatureError(RuntimeError):
    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg


class OutOfRangeDateError(RuntimeError):
    def __init__(self, min_date: date, max_date: date):
        super().__init__()
        self.min_date = min_date
        self.max_date = max_date
        self.msg = "The date must be between %s and %s" % (
            min_date.strftime("%Y-%m-%d"),
            max_date.strftime("%Y-%m-%d"),
        )


class CompileError(RuntimeError):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg
