import re
from constants import *

AUCTION_DATE = 0
ISSUE = 1
AUCTION_ANNOUNCEMENT = 2

JBI = "Inflation-Indexed"

ISSUE_REGEX = re.compile(r"\(\d+\)")
REOPEN_REGEX = re.compile(r"(\w+ \d{4})")

AUCTION_DATE_FORMAT = "%b %d, %Y"

TD = "td"
TR = "tr"
ANNOUNCEMENT_TD_ATTRS = {"colspan": 2}
