import re


# ######################################### #
# Helper functions for main.py and test.py
# ######################################### #
def _time_slice(period: str) -> slice:
    vals = period.split(":")
    if len(vals) != 3:
        raise ValueError(
            "'period' must have exacly three values separated with colons"
        )
    return slice(*vals)


def _handle_period_arg(unknowns):
    _PERIOD_PATTERN = re.compile(r"^-.+:.+:.+$")
    for un in unknowns:
        if _PERIOD_PATTERN.match(un):
            return _time_slice(un)
    raise ValueError("Period must be provided as argument (e.g. -10d:-2d:10m)")
