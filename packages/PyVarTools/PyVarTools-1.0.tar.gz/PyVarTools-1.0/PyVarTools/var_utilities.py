from re import search
from datetime import datetime, timedelta
#
#
#
#
def date_range(start_date: datetime, end_date: datetime, step: timedelta):
	while start_date < end_date:
		yield start_date
		start_date += step
#
#
#
#
def check_string_is_IPv4(string: str):
	return bool(
			search(
					r"\A\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d{1,5})?\Z",
					string
			)
	)
