import os
import sys
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler

from Collector import Collector



class EventLogger:

	"""
	# Logging Output into Console
	"""

	def __init__ (self, ignored_event=None):
		self._ignored_event = ignored_event


	def write (self, event):
		if self._ignored_event is not None and event.event_type in self._ignored_event:
			return
		dt = datetime.strftime (datetime.now(), "%Y-%m-%d %H:%M:%S")
		filename = event.src_path.split('/')[ len(event.src_path.split('/')) - 1 ]
		print (f"{dt}\t{filename} has been {event.event_type}")



class Watcher:

	"""
	# To Observe Specific Events of files within the given Folder
	"""

	def __init__ (self, path='.', handler=FileSystemEventHandler()):
		self.path = path
		self.handler = handler
		self.observer = Observer()



	def run (self):
		print ("Starting the watcher ...")
		self.observer.schedule (
			self.handler,
			self.path, 
			recursive=True
		)
		self.observer.start ()
		print ("Watcher in progress")
		print (f"Target Path : {self.path}\n")
		try:
			while True:
				time.sleep (1)
		except KeyboardInterrupt:
			print ("\nKeyboardInterrupt Encountered. Exiting ....\n")
			self.observer.stop ()
		self.observer.join ()



class Handler (PatternMatchingEventHandler):

	"""
	# Event Hanlder Model for Watcher
	"""

	def __init__ (self, patterns=None, ignore_directories=None, case_sensitive=None, event_logger=EventLogger()):
		super().__init__(patterns, ignore_directories, case_sensitive)
		self._event_logger = event_logger



	def on_any_event (self, event):
		self._event_logger.write (event)


	def on_created (self, event):
		collector = Collector (event.src_path)
		data = collector.collect ()
		filename = event.src_path.split('/')[ len(event.src_path.split('/')) - 1 ]
		collector.export_csv (data, f"Exports/{filename}")



if __name__ == '__main__':
	path = '/Users/kyawthit/Desktop/Scripts/WatchDog/Data/'
	if not os.path.isdir (path):
		print (f"\n[Error]\t{path} not found!\n")
		sys.exit()

	handler = Handler (
		patterns=['*.txt', '*.csv', '*.json'], 
		case_sensitive=True, 
		event_logger=EventLogger(ignored_event=["moved", "closed"])
	)
	watcher = Watcher (path, handler)
	watcher.run ()









