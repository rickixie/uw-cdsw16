import ssadata

for name in ssadata.boys.keys():
    if 'king' in name:
        print(name + " " + str(ssadata.boys[name]))

for name in ssadata.girls.keys():
    if 'queen' in name:
        print(name + " " + str(ssadata.girls[name]))
