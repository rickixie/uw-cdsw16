"""
Module for loading data from wikipedia_bios.csv.
"""

import csv
from datetime import datetime

f = open('wikipedia_bios.csv', 'r')
reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
columns = {}
columns_female = {}
columns_male = {}
for fieldname in reader.fieldnames:
	columns[fieldname] = []
	columns_female[fieldname] = []
	columns_male[fieldname] = []

rows = []
rows_female = []
rows_male = []

for row in reader:
	# Convert firstedit from a string to a date.
	row['firstedit'] = datetime.strptime(row['firstedit'], '%Y-%m-%d %H:%M:%S')
	rows.append(row)
	if row['gender'] == 'female':
		rows_female.append(row)
	else:
		rows_male.append(row)
	for fieldname, value in row.items():
		columns[fieldname].append(value)
		if row['gender'] == 'female':
			columns_female[fieldname].append(value)
		else:
			columns_male[fieldname].append(value)

