# Copyright (C) 2016 Ben Lewis, and Morten Wang
# Licensed under the MIT license, see ../LICENSE

# What was the most edits per day in the first two weeks?

import requests

ENDPOINT = 'https://en.wikipedia.org/w/api.php'

parameters = { 'action' : 'query',
               'prop' : 'revisions',
               'titles' : 'Panama_Papers',
               'format' : 'json',
               'rvdir' : 'newer',
               'rvstart': '2016-04-03T17:59:05Z',
               'rvend' : '2016-04-23T17:59:05Z',
               'rvlimit' : 500,
               'continue' : '' }

num_revisions = 0

done = False
hour_edits = {}
while not done:
    wp_call = requests.get(ENDPOINT, params=parameters)
    response = wp_call.json()

    pages = response['query']['pages']
    
    for page_id in pages:
        page = pages[page_id]
        revisions = page['revisions']
        for revision in revisions:
            revday = revision['timestamp'][0:10]
            revhour = revision['timestamp'][0:13]
            num_revisions = num_revisions + 1
            
            if revhour in hour_edits:
                hour_edits[revhour] = hour_edits[revhour] + 1
            else:
                hour_edits[revhour] = 1

    print('Done one query, num revisions is now ' + str(num_revisions))

    if 'continue' in response:
        parameters['continue'] = response['continue']['continue']
        parameters['rvcontinue'] = response['continue']['rvcontinue']
    else:
        done = True

top_hours = []
max_edits = 0
for revhour in hour_edits:
    num_edits = hour_edits[revhour]
    if num_edits > max_edits:
        max_edits = num_edits
        top_hour = [revhour]
    elif num_edits == max_edits:
        top_hours.append(revhour)
    else:
        pass

print(str(top_hour) + 'Is the hour with the most edits. ')
print('There were ' + str(max_edits) + ' edits during that hour.')
