import gobject
import pango
import pygtk
pygtk.require('2.0')
import gtk
from gtk import gdk
import cairo
from cal import Cal
from datetime import datetime


class Gui:
   

	def __init__(self, cally):
		self.cally = cally
		
		# -- Widgets
		self.window = gtk.Window()
		self.window.set_border_width(10)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.move(self.cally.config['margin left'], self.cally.config['margin top'])
		self.window.stick()
		self.window.set_decorated(False)
		self.window.set_app_paintable(True)
		self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DESKTOP)
		self.main_box = gtk.VBox()
		self.window.add(self.main_box)
		
		# -- Event handlers
		self.window.connect('expose-event', self.expose)
		self.window.connect("destroy", lambda w: gtk.main_quit())
		
		

		self.screen_changed(self.window)
	
		# -- Call start up methods
		# We start off by showing a calendar of this month
		date = datetime.now()
		self.create_calendar(date.month, date.year )
		
		
		self.window.show_all()


	# Generates the calendar
	def create_calendar(self, m, y):
		cal = Cal().get_cal(m, y)
		#event_bg_color = gtk.gdk.color_parse(self.cally.config['background event'])
		event_txt_color = gtk.gdk.color_parse(self.cally.config['text event'])
		normal_txt_color = gtk.gdk.color_parse(self.cally.config['text normal'])
		# create a table of 6 rows, 7 columns (dimension of calendar)
		table = gtk.Table(6, 7)
		for i, row in enumerate(cal):
			for j, d in enumerate(row):
				# Create label with event box
				if d == 0: d = ' '
				day = gtk.Label(d)
				day.set_markup("<span foreground='%s'>%s</span>" % (normal_txt_color, d))
				e = gtk.EventBox()
				e.add(day)
				e.set_border_width(5)
				e.set_size_request(40, 30)
				
				
				# each day is an ID. the id format is 'month day year'
				# see if we have this ID in our events dictionary. if so,
				# we color this eventbox to let the user know there's an 
				# event on this day
				id = "%s %s %s" % (m, d, y)
				if self.cally.events.has_key(id):
					# This day has an event. Apply colors, etc
					e.set_visible_window(True)
					e.set_app_paintable(True)
					e.connect("expose-event", self.expose_eventbox)
					day.set_markup("<span foreground='%s'>%d</span>" % (event_txt_color, d))
				else:
					e.set_visible_window(False)
					
				# Since there is only 1 widget inside the eventbox clicked, that widget
				# is our label. So w.get_children()[0].get_label() should give us our day.
				d = e.get_children()[0].get_text()
				e.connect('button-press-event', self.create_popup, m, d, y)
								
				
				# Attach eventbox to table
				table.attach(e, j, j+1, i, i+1)

		self.main_box.add(table)
		table.show_all()
		

	# OK was clicked on dialog box
	def add_event(self, w, e, month, day, year, buf):
		# If buffer has any text, we save/update this event.
		# If not, then we delete it
		start, end = buf.get_bounds()
		notes = buf.get_text(start, end)
		eventid = "%s %s %s" % (month, day,  year)
		
		if len(notes) == 0:
			try:
				del self.cally.events[eventid]
			except: return
		else:
			self.cally.events[eventid] = notes
			self.cally.save_events_dict()
		
		# "reload" calendar so new event is shown
		self.window.unrealize()
		self.__init__(self.cally)
		

	# User double clicked a day. Show our popup window.
	# FIXME this should be in its own class
	def create_popup(self, w, e, month, day, year):
		
		# We want doubleclick only.
		if not e.type == gtk.gdk._2BUTTON_PRESS: return
			
		window = gtk.Window()		
		window.set_size_request(280,200)
		window.set_decorated(False)
		window.set_border_width(10)
		window.set_position(gtk.WIN_POS_MOUSE)
		
		# Create boxes
		vbox = gtk.VBox()
		hbox = gtk.HBox()
		
		# Create widgets
		sw = gtk.ScrolledWindow()
		textview = gtk.TextView()
		ok = gtk.Button('save')
		close = gtk.Button('close')
		
		# Put widgets in boxes
		sw.add(textview)
		vbox.pack_start(sw, 1, 1, 0)
		vbox.pack_start(gtk.HSeparator(), 0, 0, 0)
		hbox.pack_start(ok)
		hbox.pack_start(close)
		
		# Put boxes inside boxes. Boxin' all day everyday
		vbox.pack_start(hbox, 0, 0 ,0)
		window.add(vbox)	
		
		# Bind events
		ok.connect("button-press-event", self.add_event, month, day, year, textview.get_buffer())
		close.connect("button-press-event", lambda x, y: window.destroy())

		# Before showing the textview, let's see if there's an event this date.
		# If so, show the notes inside the textview
		buf = textview.get_buffer()
		id = "%s %s %s" % (month, day, year)
		if self.cally.events.has_key(id):
			text = self.cally.events[id]
		else:
			text = None
		if text : buf.set_text(text)
		
		# Show the popup window
		window.show_all()	

	
	# For eventbox transparency
	def expose_eventbox(self, w, e):
		cr = w.window.cairo_create()
		cr.set_operator(cairo.OPERATOR_SOURCE)
		cr.set_source_rgba(30/255, 30/255, 30/255, 0.5)
		cr.rectangle(0, 0, 40, 40)
		cr.fill()
		return False
		
		
	# For window transparency	
	def expose(self, widget, e):
		cr = widget.window.cairo_create()
		cr.set_operator(cairo.OPERATOR_SOURCE)
		(width, height) = widget.get_size()
		cr.set_source_rgba(1.0, 0.2, 0.2, 0.0)
		cr.rectangle(0, 0, width, height)
		cr.fill()
		cr.stroke()
		return False
	
	
	# For window transparency
	def screen_changed(self, widget, old_screen = None):
		screen = widget.get_screen()
		colormap = screen.get_rgba_colormap()
		widget.set_colormap(colormap)
		return False
	
def main():
	gtk.main()
	return 0       

if __name__ == "__main__":

	main()
