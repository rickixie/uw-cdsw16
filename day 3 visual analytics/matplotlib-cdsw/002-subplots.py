""" 

Make a slightly more elaborate plot with subplots

Save the figure in the end

""" 
import matplotlib.pyplot as plt
import math

# Make some data to plot
x = []
y1 = []
y2 = []

for i in range(100):
    x.append(i)
    y1.append(math.sin(i * (2 * math.pi / 100)))
    y2.append(math.cos(i * (2 * math.pi/ 100)))

# First, create an empty figure with 2 subplots --> in ax1, ax2
# - The function plt.subplots returns an object for the figure and for each axes
# - There are multiple ways to accomplish this same goal, but this is probably the
#   simplest - notice that each subplot is associated with one of the axes objects.
fig, (ax1, ax2, ax3) = plt.subplots(3)

# Next, put one line on the first axis and both lines on the second axis
# - On the second axes, add a legend to distinguish the two lines
ax1.plot(x, y1)

ax2.plot(x, y1, label='sin')  # The labels are what appear in the legend
ax2.plot(x, y2, label='cos')
ax2.legend() #tell the axes to add the legend

ax3.plot(x,y2)
# Finally, save the figure as a png file
fig.savefig('myfig.png')