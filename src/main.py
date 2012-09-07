from gui import Gui
import gtk
import os
from os.path import expanduser
		
class Cally:
	
	def __init__(self):
		
		self.cfg_dir  = expanduser("~/.config/cally")
		self.rc_file = self.cfg_dir + "/callyrc"
		self.events_file = self.cfg_dir + "/events"
		
		self.check_directory()		
		self.load_config()
		self.load_events()
		self.gui = Gui(self)
	
	
	# Load our configs
	def load_config(self):
		f = open(self.rc_file)
		conf = f.read()
		self.config = eval(conf)
		
		
	# Load our events, or if there are none, create empt dic
	def load_events(self):
		# Read our events file to see if we have anything
		f = open(self.events_file)
		d = f.read()
		if d:
			# There is a dict in the file. This dict should contain
			# information about events. So we need this for when
			# creating our calendar.
			self.events = eval(d)
		else:
			# File is blank. Create an empty dictionary. Each time an 
			# event is added, we append it to this dict, and save it
			# to the file
			self.events = {}
		f.closed
		
		
	# Store our current events dict into the file
	def save_events_dict(self):
		with open(self.events_file, 'w') as f:
			f.write(str(self.events))
		f.closed
		
		
	# See if our config directory exists in ~/.config
	def check_directory(self):
		
		
		if os.path.exists(self.cfg_dir) == False:
			os.mkdir(self.cfg_dir)
			
			# create empty events file
			f = open(self.events_file, "w")
			f.close()
			
			# Create our default rc file
			rc = """
# Our config file.
# Leave a value blank for default/transparency


# by default, the windows is placed on the top left of your screen, (0,0) coordinates.
# 'margin left' tells how many pixels from the left cally should load. Same thing for 'margin top'
# play around with these to position cally where you want it. Some window managers may ignore this.

{
'margin left' : 1620,			# distance from left side of screen
'margin top' : 30,				# distance from top of screen
'text normal':'#222222',		# default text color for everything
'text event' : '#6c9b87',		# text color on event day
'background calendar' : '',		# not yet implemented
'background weekday' : '',		# background of mon, tue, etc
'background event' : '#222222'	# background color of event day
}
"""
			f = open(self.rc_file, "w")
			f.write(rc)
			f.close()
			
cally = Cally()

if __name__ == "__main__":
	gtk.main()


