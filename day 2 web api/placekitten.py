# Retrieves square pictures of kittens from the placekitten.com API

import requests

# Gets the user's input to determine picture size
pic_size = input("How big a kitten? ")

# Creates custom URL for the API
url = "http://placekitten.com/%(size)s/%(size)s" % {"size": pic_size}

# Requests and gets the photo data
kitten = requests.get(url)

# Saves (writes) the file
file_name = "kittten-%(size)s.jpg" % {"size": pic_size}
kitten_file = open(file_name, "wb")
kitten_file.write(kitten.content)
kitten_file.close()
