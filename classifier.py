# -*- coding: utf-8 -*-
#!/usr/bin/python

import librosa
import numpy as np
import multiprocessing as mp

from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors


def computeMFCCThreaded(list_of_songs):
	# cpu_cores = 1
	# print "Nombre de cores " + str(cpu_cores)

	# Recupere le nombre de coeurs de la machine
	cpu_cores = mp.cpu_count()
	pool = mp.Pool(cpu_cores)
	songs = pool.map(loadSong, list_of_songs)

	return songs


def loadSong(song):
	full_path = song.path + song.name + song.ext;
	y, sr = librosa.load(full_path)

	# corrompu ?
	if len(y) == 0:
		song.id_genre = -1
		print "Corrompu " + song.path + song.name + song.ext
		
	else:
		M = librosa.feature.mfcc(y=y, sr=sr)
		#centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

		#song.y = np.copy(y)
		song.sr = sr
		song.mfcc = np.copy(M)
		#song.centroid = np.copy(centroid)

	return song


def findNN(train_dataset, song, MAX_COLS, n_neighbors=5):
	if song is None:
		return
	if song.mfcc is None:
		return

	neigh = NearestNeighbors(n_neighbors=n_neighbors)	

	neigh.fit(train_dataset)

	song_mffc_as_vector = np.reshape(song.mfcc, (1, song.mfcc.shape[0] * song.mfcc.shape[1]))
	song_mffc_as_vector = checkMFCCsize(song_mffc_as_vector, MAX_COLS)

	NN = neigh.kneighbors(song_mffc_as_vector)
	song.NN = NN


def classifyNearestNeighbors(train_dataset, classify_dataset, n_neighbors=5):
	mfccs = []
	MAX_COLS = 25000

	for s in train_dataset:
		if s.mfcc is not None:
			new_mfcc = np.reshape(s.mfcc, (1, s.mfcc.shape[0] * s.mfcc.shape[1]))
			new_mfcc = checkMFCCsize(new_mfcc, MAX_COLS)
			mfccs.append(new_mfcc)

	mfccs = np.asarray(mfccs);

	nsamples, nx, ny = mfccs.shape
	train_dataset = mfccs.reshape((nsamples, nx * ny))

	for c_song in classify_dataset:
		findNN(train_dataset, c_song, MAX_COLS, n_neighbors)


def defineGenre(train_dataset, classify_dataset):
	for song in classify_dataset:
		if song.NN is not None:
			# on recupere les indices des N voisins
			indicesTrainNN = song.NN[1][0]
			id_genres = []
			# on parcourt tout les voisins pour recuperer
			# les id_genre de ces voisins
			for i in indicesTrainNN:
				id_genres.append(train_dataset[i].id_genre)

			song.id_genre = greatestOccurrence(id_genres)
		else:
			song.id_genre = -1


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

# Passe une MFCC en parametre et determine s'il a la bonne
# verifie s'il est de la bonne taille.
# Si ce n'est pas le cas, soit il fait du padding
# soit il le tronque
def checkMFCCsize(mfcc, size, padding_value=0):
	n = np.array([])

	if mfcc.shape[1] != size:
		if mfcc.shape[1] > size:
			n = np.copy(mfcc[0][0:size])
			n = np.reshape(n, (1, n.shape[0]))
		else:
			mfcc_tmp = np.copy(mfcc)
			for i in range(mfcc.shape[1], size):
				mfcc_tmp = np.append(mfcc_tmp, padding_value)
			mfcc_tmp = np.reshape(mfcc_tmp, (1, n.shape[0]))
			n = np.copy(mfcc_tmp)

	n = np.reshape(n, (1, n.shape[1]))
	return n










def findKNN(list_of_songs, mfcc):
	knn = KNeighborsClassifier()
	mfccs = []
	for s in list_of_songs:
		mfccs = mfccs.append(s.mfcc)

	knn.fit(mfccs)
	same_mfcc = knn.neighbors(mfcc)


def m_std_v_ofMFCC(y):

	return np.mean(y), np.std(y), np.var(y)