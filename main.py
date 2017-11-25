# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import classifier
import colors
import csv_tools

# Prend 3 parametre:
# 1 => CSV genre labels
# 2 => chemin du dossier contenant les musiques à classer
# 3 => le fichier CSV contenant le resultat de la classification

def main():
	if len(sys.argv) - 1 != 3: # les 3 args + le nom du fichier
		print colors.bcolors.FAIL +  'usage: python main.py <CSV file (verite de terrain)> <rep with all songs> <CSV output result>' + colors.bcolors.ENDC
	else:
		print colors.bcolors.OKGREEN + "Start processing ....." + colors.bcolors.ENDC

		# dicGenre contient les lavbels pour chaque genre musical
		dicGenre = csv_tools.CSVtoDictionary(sys.argv[1])
		csv_tools.dictionaryToCSV(dicGenre, "test_1_2_1_2.csv", "genre_id,genre\n")

		# classifier.classify(sys.argv[1], sys.argv[2], sys.argv[3])

		print colors.bcolors.OKGREEN + "Done" + colors.bcolors.ENDC

if __name__ == '__main__':
	main()