import requests

answer = requests.get("https://mako.cc/cdsw.json")
parsed_json = answer.json()

fish = parsed_json["fish"]

for betta_name in fish:
	print(betta_name["name"])
for betta_age in fish:
	print(betta_age["age"])
