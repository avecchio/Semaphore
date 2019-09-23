import sys, argparse
from Bio import SeqIO

def read_fasta_file(fastaFilepath):
	try:
		return SeqIO.parse(open(fastaFilepath),'fasta')
	except:
		print('There was an issue with importing the file: ' + filepath)

def fasta_sequence_todict(sequences):
	sequence_dict = {}
	for fasta in sequences:
		name, sequence = fasta.id, str(fasta.seq)
		sequence_dict[name] = sequence
	return sequence_dict

def compare_fasta_files(alpha_filename, beta_filename):
	alpha_sequences = read_fasta_file(alpha_filename)
	beta_sequences = read_fasta_file(beta_filename)
	# compare the dictionaries
	if (alpha_sequences is not None and beta_sequences is not None):
		alpha_sequence_dict = fasta_sequence_todict(alpha_sequences)
		beta_sequence_dict = fasta_sequence_todict(beta_sequences)
		
		alpha_sequence_names = alpha_sequence_dict.keys()
		beta_sequence_names = beta_sequence_dict.keys()

                # Get exclusive sequences and a list of all sequences
                alpha_exclusive_sequences = [name for name in alpha_sequence_names if name not in beta_sequence_names]
		beta_exclusive_sequences = [name for name in beta_sequence_names if name not in alpha_sequence_names]
		all_sequences = list(set(alpha_sequence_names) | set(beta_sequence_names))

                # Format text and print results to the screen
		for sequence in all_sequences:
			if (sequence in alpha_exclusive_sequences):
				print('{}: Missing from {}'.format(sequence, alpha_filename))
			elif (sequence in beta_exclusive_sequences):
				print('{}: Missing from {}'.format(sequence, beta_filename))
			else:
				if (alpha_sequence_dict[sequence] == beta_sequence_dict[sequence]):
					print('{}: Same'.format(sequence))
				else:
					print('{}: Different'.format(sequence))


if __name__ == "__main__":

	# define argument parser
	parser = argparse.ArgumentParser(description='')

	# define arguments
	fileOneDesc = 'The first fasta file to be compared'
	fileTwoDesc = 'The second fasta file to be compared'
	parser.add_argument('-fst1','--fastafile1', help=fileOneDesc, required=True)
	parser.add_argument('-fst2','--fastafile2', help=fileTwoDesc, required=True)

	# get arguments
	args = vars(parser.parse_args())
	
	# read both fasta files
	alpha_filename = args['fastafile1']
	beta_filename = args['fastafile2']
	
	compare_fasta_files(alpha_filename, beta_filename)
