""" 

hello_plot.py

A first plot with matplotlib

"""

import matplotlib.pyplot as plt 
figure, axis = plt.subplots(1)
#the above line equals to the next three lines
#fig_and_axis = plt.subplots(1)
#figure = fig_and_axis[0]
#axis = fig_and_axis[1]

#(1,2), (2,4), (3,8)
axis.plot([1,2,3], [2,4,8])

plt.show()

