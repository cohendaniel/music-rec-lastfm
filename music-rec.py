import csv
import operator

class MusicRec(object):

	def __init__(self, arg):

		self.NUM_LINES = 1000000

		# raw data from file
		# format: [[user_id, artist], [user_id, artist]...]
			# e.g. [[1, "coldplay"], [1, "u2"] ... [100, "eminem"] ... ]
		self.data = self._readFile(arg)

		# counts of artists from neighbor users
		# format: {artist1: count1, artist2: count2, ... }
		#	e.g. {"coldplay": 352, "u2": 233, ... }
		self.counts = {}

	def getRecommendation(self, artist):

		self.counts.clear()

		self._getCounts(artist)

		if len(self.counts) == 0:
			print "Artist not found"
			return

		# sort the counts in descending order
		# sorting is O(n lg n) -- TODO: can use a quick select to reduce the complexity to O(n) on average
		sortedCounts = sorted(self.counts.items(), key=operator.itemgetter(1), reverse=True)

		# print the top ten recommendations based on artist
		print sortedCounts[:10]		


	# Given an artist, find users who listen to artist and track their other top artists
	def _getCounts(self, artist):

		for index, userData in enumerate(self.data):
			
			# if user's top artist is same as artist from input
			if userData[1] == artist:
				
				self._countArtists(userData[0], index)


	# The data is organized such that a user's top artists are sequential:
	# 	userA   coldplay
	# 	userA   eminem
	#   ...
	#   userB   britney spears

	# Given the index of a user's top artist, count the user's other top artists
	def _countArtists(self, user, index):

		topArtists = []

		# count artists before the artist index for given user
		i = index - 1

		while self.data[i][0] == user:
			topArtists.append(self.data[i][1])
			i -= 1

		# count artists after the artist index for given user
		i = index + 1

		while self.data[i][0] == user:
			topArtists.append(self.data[i][1])
			i += 1

		# update counts for recommendation system
		for artist in topArtists:
			self.counts[artist] = self.counts.get(artist, 0) + 1
	
	def _readFile(self, fp):

		with open(fp, 'r') as file:

			rows = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)

			data = []

			# Read only up to NUM_LINES of data into memory
			for i, row in enumerate(rows):
				
				if i > self.NUM_LINES:
					break

				# row[0] = user id
				# row[2] = artist
				data.append([row[0], row[2]])

			return data

m = MusicRec("usersha1-artmbid-artname-plays.tsv")

print "Enter an artist or \"q\" to quit: "
artist = raw_input()

while artist != "q":
	m.getRecommendation(artist)
	print "\nEnter an artist or \"q\" to quit: "
	artist = raw_input()


# This is a slow version of counting user's top artists. For each of the  
# listeners of the input artist, loop through the entire data set and count
# user's other top artists. This runs in O(kn) time, where k is the number of
# users and n is the number of lines of data (k * num top artists per user)

# def _countArtistsSlow(self, listeners):

# 	counts = {}

# 	for u in listeners:

# 		for v in self.data:

# 			if u == v[0]:
# 				counts[v[1]] = counts.get(v[1], 0) + 1

# 	return counts