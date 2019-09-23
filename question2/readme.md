## Question 2 - Denormalizing Exon Coordinates

#### Setup
To execute this program, please have python 3 and pip3 installed.
All required packages are within the requirements.txt document.
To install all dependencies for this program, please execute the following command:
`pip3 install -r requirements.txt`

The following libraries were used in the making of this project:
- https://github.com/PyMySQL/PyMySQL
- http://pyyaml.org/download/pyyaml/PyYAML-5.1-cp37-cp37m-win32.whl

#### Usage
This is a command line application.
All database configuration parameters are contained within `db.yml`
The output of the program will be 

The format to execute this program is as follows:
`python3 exon_denormalizer.py -c [db_config_yaml] -g [gene_name]`

Where you must specify the `-c` parameter followed by a path to the database configuration yaml file along with the `-g` option
followed by the name of the gene for wich you would like to query the deduplicated exon coordinates.
