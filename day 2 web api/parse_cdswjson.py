import requests

requests_call = requests.get("http://mako.cc/cdsw.json")
parsed_json = requests_call.json()

print("parsed_json's type is:")
print(type(parsed_json))

# Looking inside the dict to print fish names
print("The fishes' names are:")
for fish in parsed_json["fish"]:
    print(fish["name"])
