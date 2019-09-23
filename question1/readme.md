## Question 1 - Comparing FASTA sequences

#### Setup
To execute this program, please have python 3 and pip3 installed.
All required packages are within the requirements.txt document.
To install all dependencies for this program, please execute the following command:
`pip3 install -r requirements.txt`

The following libraries were used in the making of this project:
- http://biopython.org/DIST/biopython-1.73.tar.gz

#### Usage
This is a command line application.
To use this application, both FASTA files must be downloaded to your local hard drive and extracted.

The format to execute this program is as follows:
`python3 fasta_seq_diff.py -fst1 [fasta_file_1] -fst2 [fasta_file_2]

Where you must specify the `-fst1` parameter followed by the first fasta file to compare
and the `-fst2` parameter followed by the second fasta file to be compared against.

All output will be displayed on the terminal screen
