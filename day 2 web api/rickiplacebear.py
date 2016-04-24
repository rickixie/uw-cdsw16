#this program downloads bear of a particular size from the placebear api

#step 1: ask user about the height and width
height = input("What height bear do you want?\n")
# print(height)
width = input("what width bear do you want?\n")
# print(width)

#step 2: download bear
import requests
#url1 = "https://placebear.com/%(widthI)s/%(heightI)s"%{"heightI":height, "widthI":width}
url = "https://placebear.com/{}/{}".format(width, height)

bear = requests.get(url)

#step 3: save to file
#file_name1 = "bear-%(widthI)sx%(heightI)s.jpg"%{"heightI":height, "widthI":width}
file_name = "bear-{}x{}".format(width, height)
#bear_file1 = open(file_name, 'wb')
bear_file = open("{}.jpg".format(file_name), "wb")
bear_file.write(bear.content)
bear_file.close()

print(("You have save a bear named {}!").format(file_name))

