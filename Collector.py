import pandas as pd
import os

from CollectorException import NoFileException




class Extractor:



	"""
	# Extract Data From the Given File
	"""

	def get_csv_data (self, csv_file):
		print ('reading csv file ...')
		return pd.read_csv (csv_file)



class Collector:

	"""
	# Collect Extracted Data
	"""


	def __init__ (self, src):
		try:
			if os.path.isfile (src):
				self._src = src
			else:
				raise NoFileException (f"{src} is not file!")

		except NoFileException as nfe:
			print (nfe.message)


	def collect (self):
		print ('Collecting data ...')
		extractor = Extractor()
		data = extractor.get_csv_data (self._src)
		return data


	def export_csv (self, data, dest):
		data.to_csv (dest)




if __name__ == '__main__':

	path = '/Users/kyawthit/Desktop/Scripts/WatchDog/Data/dataset.csv'

	collector = Collector (path)

	df = collector.collect()

	print (df.head())
