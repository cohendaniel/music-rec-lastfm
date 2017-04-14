import sqlite3
import csv

class MusicRecDB():

	def __init__(self, datafile, numlines, **kwargs):

		self.NUM_LINES = numlines

		self.filename = kwargs.get('filename', 'musicRec.db')
		self.table = kwargs.get('table', 'Users')

		self.db = sqlite3.connect(self.filename)
		self.db.row_factory = sqlite3.Row
		self.db.execute('''create table if not exists {} 
						   (Id TEXT, Artist_Name TEXT, 
						   Plays INTEGER)'''.format(self.table))

		count = self.db.execute('''select count(*) from {}'''
								.format(self.table)).fetchone()[0]

		if count == 0:
			print "importing data..."
			self._importData(datafile)


	# Given an artist, return a generator 

	def getSimilarUsers(self, artist):

		cursor = self.db.execute('''select Artist_Name, Plays from {} where Id in 
									(select Id from {} where Artist_Name = ?)'''
								 .format(self.table, self.table), (artist,))

		for row in cursor:
			yield dict(row)

	def close(self):

		self.db.close()
		del self.filename

	def _importData(self, fp):

		with open(fp, 'r') as file:

			rows = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)

			data = []

			# Read only up to NUM_LINES of data into memory
			for i, row in enumerate(rows):
				
				if i > self.NUM_LINES:
					break

				# row[0] = user id, row[2] = artist, row[3] = plays
				data.append((row[0], row[2].decode('utf-8'), row[3]))
				
			self.db.executemany('''insert into {} (Id, Artist_Name, Plays) 
							   values (?, ?, ?)'''.format(self.table), data)

			self.db.execute('''create index name_index on {} (Artist_Name)'''.format(self.table))
			self.db.execute('''create index id_index on {} (Artist_Name)'''.format(self.table))

			self.db.commit()

