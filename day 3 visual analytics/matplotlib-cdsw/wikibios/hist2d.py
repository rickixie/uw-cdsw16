"""Make a 2D histogram ("heat map") of the male and female articles by birth year and first edit date"""
import wikibios
from datetime import datetime
from matplotlib import pyplot, dates

figure = pyplot.figure()

min_firstedit = min(dates.date2num(wikibios.columns['firstedit']))
max_firstedit = max(dates.date2num(wikibios.columns['firstedit']))

firstedits_male = dates.date2num(wikibios.columns_male['firstedit'])
birth_years_male = wikibios.columns_male['birth_year']

axes1 = figure.add_subplot(1,2,1)
h1 = axes1.hist2d(firstedits_male, birth_years_male, range=[[min_firstedit, max_firstedit], [1750, 2014]], bins=50)
figure.colorbar(h1[3])
axes1.xaxis.set_major_formatter(dates.AutoDateFormatter(dates.AutoDateLocator()))
axes1.set_title('Male')

firstedits_female = dates.date2num(wikibios.columns_female['firstedit'])
birth_years_female = wikibios.columns_female['birth_year']

axes2 = figure.add_subplot(1,2,2)
h2 = axes2.hist2d(firstedits_female, birth_years_female, range=[[min_firstedit, max_firstedit], [1750, 2014]], bins=50)
figure.colorbar(h2[3])
axes2.xaxis.set_major_formatter(dates.AutoDateFormatter(dates.AutoDateLocator()))
axes2.set_title('Female')

figure.savefig('hist2d.png')
