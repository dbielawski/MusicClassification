
import csv

def CSVtoArray(CSV_path):
	with open(CSV_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
		dictionary = { }
		arrayName = []
		arrayQuality = []
		arrayAge = []
		all_rows = []
		for row in spamreader:
			# r = '\t'.join(row)
			# print r.split(';')
			for element in row:
				print element

	return all_rows


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

def dictionaryToCSV(dictionary, out_file_name, header):
	with open(out_file_name,'w') as f1:
		# header = "genre_id,genre" + "\n"
		f1.write(header)
		for key, value in dictionary.iteritems():
			line = key + "," + value + "\n"
			f1.write(line)