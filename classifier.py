# -*- coding: utf-8 -*-
#!/usr/bin/python

import librosa
import numpy as np
import multiprocessing as mp
import math
from sklearn.neighbors import NearestNeighbors


class Classifier:

	MAX_COLS = 5000
	n_neighbors = 5

	def __init__(self, train_dataset, classify_dataset):
		self.train_dataset = train_dataset
		self.classify_dataset = classify_dataset

		self.neigh_mfcc = None
		self.neigh_cov_mfcc = None

	# Prepare les mfcc des données train
	# def prepareTrainMFCC(self, n_neighbors=5):
	# 	mfccs = []

	# 	for s in self.train_dataset:
	# 		if s.mfcc is not None:
	# 			new_mfcc = np.reshape(s.mfcc, (1, s.mfcc.shape[0] * s.mfcc.shape[1]))
	# 			new_mfcc = checkMFCCsize(new_mfcc, self.MAX_COLS)
	# 			mfccs.append(new_mfcc)

	# 	mfccs = np.asarray(mfccs);

	# 	nsamples, nx, ny = mfccs.shape
	# 	mfccs = mfccs.reshape((nsamples, nx * ny))

	# 	self.mfccs = mfccs


	# Trouve les plus proches voisins de 'song', passe en parametre
	def findNN(self, song):
		if song is None:
			return
		if song.mfcc is None:
			return
		if song.cov_mfcc is None:
			return
		if song.mfcc.shape[1]!=20*12:
			return

		# song_mffc_as_vector = np.reshape(song.mfcc, (1, song.mfcc.shape[0] * song.mfcc.shape[1]))
		# song_mffc_as_vector = checkMFCCsize(song_mffc_as_vector, self.MAX_COLS)
		# NN = classif.neigh.kneighbors(song_mffc_as_vector)
		NN_mfcc = self.neigh_mfcc.kneighbors(song.mfcc)
		NN_cov_mfcc = self.neigh_cov_mfcc.kneighbors(song.cov_mfcc)

		song.NN_mfcc = NN_mfcc
		song.NN_cov_mfcc = NN_cov_mfcc

		return song

	def findAllNN(self):
		self.neigh_mfcc = NearestNeighbors(n_neighbors=Classifier.n_neighbors)	
		self.neigh_cov_mfcc = NearestNeighbors(n_neighbors=Classifier.n_neighbors)

		mfccs = []
		cov_mfccs = []
		for song in self.train_dataset:
			if song is not None:
				if song.mfcc is not None:
					mfccs.append(song.mfcc[0])
				if song.cov_mfcc is not None:
					cov_mfccs.append(song.cov_mfcc[0])

		self.neigh_mfcc.fit(mfccs)
		self.neigh_cov_mfcc.fit(cov_mfccs)

		for song in self.classify_dataset:
				self.findNN(song)

	# Parcours toutes les données à classer pour assigner un genre musical
	def defineGenre(self):
		for song in self.classify_dataset:
			if song.NN_mfcc is not None and song.NN_cov_mfcc is not None:
				# on recupere les indices des N voisins
				indicesTrainNNmfcc = song.NN_mfcc[1][0]
				indicesTrainNNcov_mfcc = song.NN_cov_mfcc[1][0]
				id_genres = []

				# on parcourt tout les voisins pour recuperer
				# les id_genre de ces voisins
				for i in indicesTrainNNmfcc:
					id_genres.append(self.train_dataset[i].id_genre)

				for i in indicesTrainNNcov_mfcc:
					id_genres.append(self.train_dataset[i].id_genre)

				song.id_genre = greatestOccurrence(id_genres)
			else:
				song.id_genre = 0
	

# Charge tous les sons passe en parametre
# Fait de maniere parallele
def computeMFCCThreaded(list_of_songs):
	# cpu_cores = 1
	# print "Nombre de cores " + str(cpu_cores)

	# Recupere le nombre de coeurs de la machine
	cpu_cores = mp.cpu_count() + 1
	pool = mp.Pool(cpu_cores)
	songs = pool.map(loadSong, list_of_songs)
	pool.close()
	pool.join()

	return songs

# Cherche les N voisins de tous les sons a classer
# Fait de maniere parallele
# def findNNThreaded(classif):
# 	classif.neigh = NearestNeighbors(n_neighbors=Classifier.n_neighbors)	

# 	classif.neigh.fit(classif.mfccs)

# 	cpu_cores = mp.cpu_count() + 1
# 	pool = mp.Pool(cpu_cores)
# 	r = pool.apply_async(classif.findNN, args=(classif.classify_dataset,))
# 	pool.close()
# 	pool.join()
# 	pool.terminate()

# 	return r

# 	jobs = []
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i,))
#         jobs.append(p)
#         p.start()


# Charge un son depuis l'objet passe en parametre
# Extrait la MFCC
def loadSong(song):
	full_path = song.path + song.name + song.ext;
	try:
		y, sr = librosa.load(full_path)
	except:
		y = None
		print "Error while loading song, corrupted ?? : " + song.path + song.name + song.ext

	# corrompu ?
	if y is None or len(y) == 0:
		song.id_genre = 0
	else:
		M = librosa.feature.mfcc(y=y, sr=sr)
		#centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

		# new_MFCC = np.array([], shape=(M.shape[0], M.shape[1] / 100))
		new_MFCC = np.array([])
		# print "efezf", new_MFCC.shape
		x = 100
		size = M.shape
		list = np.arange(1200,size[1])
		for i in range(0,size[0]):
			M = np.delete(M, list, axis=1)

		size = M.shape
		for i in range(0, size[0]):
			new_MFCC_row = np.array([])
			for j in range(0, size[1], x):
				TMP = M[i][j:j + 100]
				TMP = np.reshape(TMP, (1, TMP.shape[0]))
				new_MFCC_row = np.append(new_MFCC_row, np.mean(TMP))

			new_MFCC_row = np.reshape(new_MFCC_row, (1, new_MFCC_row.shape[0]))
			new_MFCC = np.append(new_MFCC, new_MFCC_row)


		new_MFCC_for_cov = np.reshape(new_MFCC, (M.shape[0], int(math.ceil(float(M.shape[1]) / x))))

		cov_mfcc = np.cov(new_MFCC_for_cov)
		cov_mfcc = np.reshape(cov_mfcc, (1, (cov_mfcc.shape[0] * cov_mfcc.shape[1])))
		new_MFCC = np.reshape(new_MFCC, (1, new_MFCC.shape[0]))

		song.sr = sr
		# song.mfcc = np.copy(M)
		song.mfcc = np.copy(new_MFCC)
		song.cov_mfcc = np.copy(cov_mfcc)
		#song.centroid = np.copy(centroid)

	return song


def greatestOccurrence(array):
	counts = np.bincount(array)
	value_of_greatest_occurrence = np.argmax(counts)

	values = []

	# parcourt counts pour trouver quelles valeurs sont le plus redondantes
	for x in range(0, len(counts)):
		if counts[x] == counts[value_of_greatest_occurrence]:
			values.append(str(x))

	r = -1
	found = False

	for x in array:
		for v in values:
			if x == v and not found:
				r = x
				found = True

	return r


# Passe une MFCC en parametre et verifie s'il est de la bonne taille.
# Si ce n'est pas le cas, soit il fait du padding
# soit il le tronque
# def checkMFCCsize(mfcc, size, padding_value=0):
# 	n = np.array([])

# 	if mfcc.shape[1] != size:
# 		if mfcc.shape[1] > size:
# 			n = np.copy(mfcc[0][0:size])
# 			n = np.reshape(n, (1, n.shape[0]))
# 		else:
# 			mfcc_tmp = np.copy(mfcc)
# 			for i in range(mfcc.shape[1], size):
# 				mfcc_tmp = np.append(mfcc_tmp, padding_value)

# 			mfcc_tmp = np.reshape(mfcc_tmp, (1, mfcc_tmp.shape[0]))
# 			n = np.copy(mfcc_tmp)

# 	n = np.reshape(n, (1, n.shape[1]))
# 	return n