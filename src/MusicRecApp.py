import time

import User
import MusicRecDB
import MusicRecFile

class MusicRec():

	def __init__(self, filename, storage, lines):

		self.filename = filename

		self.storage = storage

		self.NUM_LINES = lines

		if storage == 'db':
			self.database = MusicRecDB.MusicRecDB(self.filename, self.NUM_LINES)
		elif storage == 'file':
			self.database = MusicRecFile.MusicRecFile(self.filename, self.NUM_LINES)
		else:
			raise(ValueError, "Storage type not valid -- use either 'db' or 'file'.")

		# counts of artists from neighbor users
		# 	format: {artist1: [num_users, plays], artist2: [num_users, plays], ... }
		self.counts = {}

	def getRecommendation(self, artist):

		self.counts.clear()

		numPlaysOfArtist = self.database.getSimilarUsers(artist)

		for topArtist in numPlaysOfArtist:
			name = topArtist['Artist_Name']
			plays = topArtist['Plays']

			numUsers = self.counts.get(name, [0,0])[0]
			playSum = self.counts.get(name, [0,0])[1]
			
			self.counts[name] = [numUsers + 1, playSum + plays]


		# sort in descending order by # of plays -- TODO: look into k nearest neighbors for rec technique
		# sorting is O(n lg n) -- TODO: can use a quick select to reduce the complexity to O(n) on average
		sortedCounts = sorted(self.counts.items(), key=lambda count: count[1][1], reverse=True)

		# print the top ten recommendations based on artist
		print sortedCounts[:10]	

if __name__ == '__main__':

	m = MusicRec("../usersha1-artmbid-artname-plays.tsv", "file", 100)

	print "Enter an artist or \"q\" to quit: "
	artist = raw_input()

	while artist != "q":
		
		start = time.time()
		m.getRecommendation(artist)
		end = time.time()
		print "Time elapsed: " + str(end-start)

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