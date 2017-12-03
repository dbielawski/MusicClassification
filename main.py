# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time
from os import listdir
from os import path
from os.path import isfile, join

import colors
import classifier
import csv_tools
from song import Song

import numpy as np


# Creer un tableau des noms des fichiers contenu dans un repertoire
def getFilesIn(directory_name):
	all_files_in_directory = [f for f in listdir(directory_name) if isfile(join(directory_name, f))]
	return all_files_in_directory

# Test le nombre d'arguments passé en paramètre, si incorrecte message d'erreur et renvoi false
def test_args():
	if len(sys.argv) - 1 != 6: # les 5 args
		print colors.bcolors.FAIL +  'usage: python main.py <genre.csv> <train.csv> <data_train_rep> <test.csv> <to_test_rep> <out_name.csv>' + colors.bcolors.ENDC
		return False
	else:
		return True

def createSongs(train_songs, train_path, dic_genre):
	songs = []
	for s in train_songs:
		split = path.splitext(s);
		name = split[0]
		ext = split[1]
		genre_id = -1
		if dic_genre[name] != "":
			genre_id = dic_genre[name]
		songs.append(Song(name, ext, train_path, genre_id))

	return songs

# Simple verification pour s'assurer que le nom du dossier se fini par un '/'
def checkPath(path):
	p = path
	if p[len(p) - 1] != '/':
		p += '/'

	return p

# Fonction principale
def main():
	print colors.bcolors.OKGREEN + "Start processing ..." + colors.bcolors.ENDC

	# dicGenre contient les lavbels pour chaque genre musical
	dic_genre = csv_tools.CSVtoDictionary(sys.argv[1])
	dic_train = csv_tools.CSVtoDictionary(sys.argv[2])
	train_songs_files = getFilesIn(sys.argv[3])
	songs_to_test = csv_tools.CSVtoDictionary(sys.argv[4])
	to_test_song_files = getFilesIn(sys.argv[5])	

	path_to_train_songs = checkPath(sys.argv[3])
	path_to_classify_songs = checkPath(sys.argv[5])

	# Tableau de sons que l'on connait
	train_songs = createSongs(train_songs_files, path_to_train_songs, dic_train)
	to_classify_songs = createSongs(to_test_song_files, path_to_classify_songs, songs_to_test)

	NUMBER_OF_SONGS_TO_TRAIN = 5
	# NUMBER_OF_SONGS_TO_TRAIN = len(train_songs)
	NUMBER_OF_SONGS_TO_CLASSIFY = 5
	# NUMBER_OF_SONGS_TO_CLASSIFY = len(to_classify_songs)

	print colors.bcolors.OKBLUE + 'Loading songs and extracting features ...' + colors.bcolors.ENDC
	# Dans un premier temps on calcul la MFCC des musiques 'connues' (train)
	# Ainsi que ...
	time_elapsed = time.time();
	train_songs = classifier.computeMFCCThreaded(train_songs[0:NUMBER_OF_SONGS_TO_TRAIN])
	to_classify_songs = classifier.computeMFCCThreaded(to_classify_songs[0:NUMBER_OF_SONGS_TO_CLASSIFY])	
	print colors.bcolors.OKGREEN + 'Songs loaded in ' + str(time.time() - time_elapsed) + colors.bcolors.ENDC

	print colors.bcolors.OKBLUE + 'Classifying songs ...' + colors.bcolors.ENDC
	time_elapsed = time.time();
	classifier.classifyNearestNeighbors(train_songs, to_classify_songs)
	print colors.bcolors.OKBLUE + 'Classification done in ' + str(time.time() - time_elapsed) + colors.bcolors.ENDC

	classifier.defineGenre(train_songs, to_classify_songs)
	csv_tools.songsToCSV(to_classify_songs, "track_id,genre_id\n", sys.argv[6])

	print colors.bcolors.OKGREEN + "Done processing" + colors.bcolors.ENDC

if __name__ == '__main__':
	if test_args():
		time_elapsed = time.time();
		main()
		print "Time time elapsed: " + str(time.time() - time_elapsed)