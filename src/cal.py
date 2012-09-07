import calendar
import itertools
from pprint import pprint as p

class Cal:
	
	def __init__(self):
		pass

	# Returns a calendar for year 'y' and month 'm'
	def get_cal(self, m, y):
		calendar.setfirstweekday(calendar.SUNDAY)
		cal = calendar.monthcalendar(y, m)
		days = list()
		header = "sun mon tue wed thur fri sat".split(" ")
		cal.insert(0,header)
		return cal

	
