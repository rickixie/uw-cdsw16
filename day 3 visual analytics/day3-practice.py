counter = 0
print(counter)

while True:
	counter = counter + 1
	
	if counter == 2:
		continue

	print(counter)

	if counter >=10:
		break


names = ['mako','mika','bettamax']

#join all items in the lists joined together as a single string
",".join(names) 
#return "mako,mika,bettamx"
#"\t".join(names)
#return "mako	mika	bettamax"




fav_colors = {'mako':'pink','bettamax':'acquamarine','mika':'blue'}
fav_colors2 = {'mako':'red', 'mika':'red', 'nothing':'null'}
#update will update dict item that can be found in the original dictionary and add new item to it
fav_colors.update(fav_colors2)

print(fav_colors)


#create your own function
def my_function():
	print ("hi there")

def greet(name):
	greeting_string = "hi there {}".format(name)
	return(greeting_string)

greet("mako")


for current_name in names:
	print(greet(current_name))
