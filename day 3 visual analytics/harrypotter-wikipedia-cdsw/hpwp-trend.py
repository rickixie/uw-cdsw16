import encoding_fix

from csv import DictReader

# read in the input file and count by day
input_file = open("hp_wiki.tsv", 'r', encoding="utf-8")

edits_by_day = {}
for row in DictReader(input_file, delimiter="\t"):
    day_string = row['timestamp'][0:10]

    if day_string in edits_by_day:
        edits_by_day[day_string] = edits_by_day[day_string] + 1
    else:
        edits_by_day[day_string] = 1

input_file.close()

# output the counts by day
output_file = open("hp_edits_by_day.tsv", "w", encoding='utf-8')

# write a header
output_file.write("date\tedits\n")

# iterate through every day and print out data into the file
for day_string in edits_by_day.keys():
    output_file.write("\t".join([day_string, str(edits_by_day[day_string])]) + "\n")

output_file.close()
