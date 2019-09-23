import sys, argparse
import yaml
import pymysql.cursors

def load_config(config_filepath):
	with open(config_filepath, 'r') as stream:
		try:
			return yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print('>>> Invalid yaml file! <<<')
			print(exc)

def db_connection(db_config):
	try:
		return pymysql.connect(host=db_config['host'], user=db_config['username'], password=db_config['password'], db=db_config['database'], charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	except:
		print('Unable to connect to host')
		print('Please verify database configuration options')

def query_db(db_configs, sql, value):
	connection = db_connection(db_configs)
	try:
		with connection.cursor() as cursor:
			# Read a single record
			cursor.execute(sql, (value,))
			return cursor.fetchall()
	finally:
		connection.close()	

def parse_exon_results(results):
	exon_coordinates = []
	chrome_name = ''
	for result in results:
                # Extract all data. Set bytes of coordinates in utf8 format and then split into array
		chrom_name = str(result['chrom'])
		exon_starts = str(result['exonStarts'], 'utf-8').split(',')
		exon_ends = str(result['exonEnds'], 'utf-8').split(',')

                # if both start and end sets are of equal length
                # convert both sets into integer arrays and merge the list into a single list of objects with start/end attributes
		if (len(exon_starts) == len(exon_ends)):
			exon_coordinates += merge_exon_arrays(to_int_array(exon_starts), to_int_array(exon_ends))

                exon_coordinates = sorted(exon_coordinates, key = lambda i: i['exonStart'])
	return exon_coordinates, chrom_name

def merge_exon_arrays(alpha_array, beta_array):
	merged_array = []
	if (len(alpha_array) == len(beta_array)):
		for index in range(0, len(alpha_array)):
			merged_array.append({'exonStart': alpha_array[index], 'exonEnd': beta_array[index]})
	return merged_array

def to_int_array(str_arr):
	int_arr = []
	for item in str_arr:
		try:
			int_arr.append(int(item))
		except:
			pass
	return int_arr

def format_to_bed(chrom_name, deduped_exon_coordinates):
        # construct headers
        body_template = 'browser position {}:{}-{}\nbrowser hide all\n'
	body = body_template.format(chrom_name, deduped_exon_coordinates[0]['exonStart'], deduped_exon_coordinates[-1]['exonEnd'])

        # for all deduped values, format into BED format
        for exon_index in range(0, len(deduped_exon_coordinates)):
		coordinate = deduped_exon_coordinates[exon_index]
		formatted_row = '{}\t{}\t{}\t{}.{}\n'.format(chrom_name, coordinate['exonStart'], coordinate['exonEnd'], chrom_name, exon_index + 1)
		body += formatted_row
	return body

def write_to_file(name, text):
	with open(name,'w') as f:
		f.write(text)
		f.close()

def dedup_exon_coordinates(exon_coordinates):
	deduped_coordinates = []
	deduped_coordinates.append(exon_coordinates[0])
	for coordinate_index in range(1, len(exon_coordinates)):
		coordinate = exon_coordinates[coordinate_index]
		deduped_coordinates = merge_deduped_exon_coordinates(coordinate, deduped_coordinates)
	return deduped_coordinates

def merge_deduped_exon_coordinates(coordinate, deduped_coordinates):
	merged = False
	for deduped_coordinate in deduped_coordinates:
                # if the start value for a new coordinate that has not been deduped
                # is between the start/end values of a deduped coordinate, set the deduped end value to the greater value
		if (coordinate['exonStart'] >= deduped_coordinate['exonStart'] and coordinate['exonStart'] <= deduped_coordinate['exonEnd']):
			if deduped_coordinate['exonEnd'] < coordinate['exonEnd']:
				deduped_coordinate['exonEnd'] = coordinate['exonEnd']
			merged = True
			break
		# if the end value for a new coordinate that has not been deduped
                # is between the start/end values of a deduped coordinate, set the deduped value to the smallest value
                elif (coordinate['exonEnd'] >= deduped_coordinate['exonStart'] and coordinate['exonEnd'] <= deduped_coordinate['exonEnd']):
			if deduped_coordinate['exonStart'] > coordinate['exonStart']:
				deduped_coordinate['exonStart'] = coordinate['exonStart']
			merged = True
			break
        # If nothing was merged, sp
        if not merged:
		deduped_coordinates.append(coordinate)
		sorted(deduped_coordinates, key = lambda i: i['exonStart'])
	return deduped_coordinates

def main(db_configs, gene_name):
	sql = "SELECT `chrom`, `exonStarts`, `exonEnds` FROM `ensGene` eg LEFT OUTER JOIN `ensemblToGeneName` etgn ON (eg.name=etgn.name) WHERE etgn.value=%s;"
	results = query_db(db_configs, sql, gene_name)
	if (len(results) == 0):
		print('No results found.')
	exon_coordinates, chrom_name = parse_exon_results(results)
	deduped_coordinates = dedup_exon_coordinates(exon_coordinates)
	bed_formatted_text = format_to_bed(chrom_name, deduped_coordinates)
	filename = chrom_name + '.bed'
	write_to_file(filename, bed_formatted_text)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-g','--geneName', help='The name of the gene to be analyzed.', required=True)
	parser.add_argument('-c','--dbConfig', help='The MYSQL Database configuration yaml file path', required=True)
	args = vars(parser.parse_args())
	gene_name = args['geneName']
	db_configs = load_config(args['dbConfig'])
	main(db_configs, gene_name)
