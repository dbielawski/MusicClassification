import csv


# Charge un fichier CSV passe en parametre puis le met dans un tableau
# L'entete n'est pas mise dans le tableau
def CSVtoArray(CSV_path):
	with open(CSV_path, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter='\n', quotechar='|')

		reader.next()
		all_rows = []
		for row in reader:
			all_rows.append(row)

	return all_rows

# Charge un fichier CSV passe en parametre puis le met dans un dictionnaire
# L'entete n'est pas mise dans le tableau
def CSVtoDictionary(CSV_path):
	with open(CSV_path, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter='\n', quotechar='|')

		reader.next()
		result = {}
		for row in reader: 
			r = '\t'.join(row)
			r = r.replace(",", " ")
			r = r.split(" ")
			key = r[0]
			if key in result:
				pass
			result[key] = '\t'.join(r[1:])

	return result

# Ecrit un fichier dictionnaire passe en parametre dans un fichier CSV
# L'entete est le parametre header
# Le fichier est nomme selon out_file_name
def dictionaryToCSV(dictionary, out_file_name, header):
	with open(out_file_name,'w') as f1:
		# header = "genre_id,genre" + "\n"
		f1.write(header)
		for key, value in dictionary.iteritems():
			line = key + "," + value + "\n"
			f1.write(line)

def songsToCSV(list_of_songs, header, out_file_name):
	with open(out_file_name,'w') as f1:
		# header = "genre_id,genre" + "\n"
		f1.write(header)
		for song in list_of_songs:
			line = song.name + "," + str(song.id_genre) + "\n"
			f1.write(line)