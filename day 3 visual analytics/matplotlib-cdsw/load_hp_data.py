""" load_hp_data.py 

A module for loading data from the Harry Potter wikipedia data set

""" 
import csv
from datetime import datetime

f = open('hp_wiki.tsv', 'r', encoding='utf-8')
reader = csv.DictReader(f, delimiter='\t')

columns = {}
for fieldname in reader.fieldnames:
	columns[fieldname] = []


rows = []
for row in reader:
    # Convert timestamp from a string to a date:
    row['timestamp'] = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
    # Convert size from a string to an integer:
    row['size'] = int(row['size'])
    rows.append(row)

# Sort these things, so that they give you nice ordered time-series
sort_rows = sorted(rows, key=lambda row: row['timestamp'], reverse=False)

rows = sort_rows
for row in sort_rows:
    for fieldname, value in row.items():
        columns[fieldname].append(value)
