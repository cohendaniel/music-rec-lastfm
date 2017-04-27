import csv

class MusicRecFile():

	def __init__(self, datafile, numlines):

		self.NUM_LINES = numlines

		self.data = self._readFile(datafile)

	# Given an artist, find users who listen to artist and track their other top artists
	def getSimilarUsers(self, artist):

		topArtists = []

		for index, userData in enumerate(self.data):
			
			# if user's top artist is same as artist from input
			if userData[1] == artist:
				
				self._countArtists(userData[0], index, topArtists)

		return topArtists


	# The data is organized such that a user's top artists and # of plays are sequential:
	# 	userA   coldplay	230
	# 	userA   eminem	204
	#   ...
	#   userB   britney spears	1454

	# Given the index of a user's top artist, count the user's other top artists
	def _countArtists(self, user, index, topArtists):

		# count artists before the artist index for given user
		i = index - 1

		while self.data[i][0] == user:
			topArtists.append({'Artist_Name': self.data[i][1], 'Plays': int(self.data[i][2])})
			i -= 1

		# count artists after the artist index for given user
		i = index + 1

		while self.data[i][0] == user:
			topArtists.append({'Artist_Name': self.data[i][1], 'Plays': int(self.data[i][2])})
			i += 1


	def _readFile(self, fp):

		with open(fp, 'r') as file:

			rows = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)

			data = []

			# Read only up to NUM_LINES of data into memory
			for i, row in enumerate(rows):
				
				print row
				if i > self.NUM_LINES:
					break

				# row[0] = user id, row[2] = artist, row[3] = plays
				data.append([row[0], row[2], row[3]])

			return data
