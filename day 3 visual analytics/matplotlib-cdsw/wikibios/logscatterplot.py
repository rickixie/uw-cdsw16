"""Make a scatterplot of male and female articles with logarithmic birth year axis scaling."""
import wikibios
from matplotlib import pyplot

figure = pyplot.figure()
axes = figure.gca()

firstedits_male = wikibios.columns_male['firstedit']
years_ago_male = [2015 - y for y in wikibios.columns_male['birth_year']]
firstedits_female = wikibios.columns_female['firstedit']
years_ago_female = [2015 - y for y in wikibios.columns_female['birth_year']]

axes.scatter(firstedits_male, years_ago_male, alpha=0.1, c='green', edgecolors='None', label='Male')
axes.scatter(firstedits_female, years_ago_female, alpha=0.1, c='orange', edgecolors='None', label='Female')
axes.set_xlabel('Article Date')
axes.set_ylabel('Years Ago')
axes.set_yscale('log')
axes.legend()
figure.savefig('logscatter.png')
