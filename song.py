import numpy as np

class Song:

	def __init__(self, name, ext="", path ="", id_genre = -1):
		self.id_genre = id_genre
		self.name = name
		self.ext = ext
		self.path = path
		#self.y = []
		self.sr = -1
		self.mfcc = None
		self.cov_mfcc = None
		#self.centroid = None
		self.NN_mfcc = None
		self.NN_cov_mfcc = None

	def __repr__(self):
		return "id_genre: " + str(self.id_genre)  + " path: " + self.path +self.name + self.ext +"\n"