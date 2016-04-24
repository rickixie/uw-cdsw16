#!/usr/bin/env python
# coding=utf-8

import encoding_fix
import requests

# get_article_revisions is a function that takes an article title in
# wikipedia and return a list of all the revisions and metadata for
# that article
def get_article_revisions(title):
    revisions = []

    # create a base url for the api and then a normal url which is initially
    # just a copy of it
    # The following line is what the requests call is doing, basically.
    # "http://en.wikipedia.org/w/api.php/?action=query&titles={0}&prop=revisions&rvprop=flags|timestamp|user|size|ids&rvlimit=500&format=json&continue=".format(title)
    wp_api_url = "http://en.wikipedia.org/w/api.php/"

    parameters = {'action' : 'query',
                  'titles' : title,
                  'prop' : 'revisions',
                  'rvprop' : 'flags|timestamp|user|size|ids',
                  'rvlimit' : 500,
                  'format' : 'json',
                  'continue' : '' }

    # we'll repeat this forever (i.e., we'll only stop when we find
    # the "break" command)
    while True:
        # the first line open the urls but also handles unicode urls
        call = requests.get(wp_api_url, params=parameters)
        api_answer = call.json()

        # get the list of pages from the json object
        pages = api_answer["query"]["pages"]

        # for every page, (there should always be only one) get its revisions:
        for page in pages.keys():
            query_revisions = pages[page]["revisions"]

            # for every revision, first we do some cleaning up
            for rev in query_revisions:
                #print(rev)
                # let's continue/skip this revision if the user is hidden
                if "userhidden" in rev:
                    continue
                
                # 1: add a title field for the article because we're going to mix them together
                rev["title"] = title

                # 2: let's "recode" anon so it's true or false instead of present/missing
                if "anon" in rev:
                    rev["anon"] = True
                else:
                    rev["anon"] = False

                # 3: let's recode "minor" in the same way
                if "minor" in rev:
                    rev["minor"] = True
                else:
                    rev["minor"] = False

                # we're going to change the timestamp to make it work a little better in excel/spreadsheets
                rev["timestamp"] = rev["timestamp"].replace("T", " ")
                rev["timestamp"] = rev["timestamp"].replace("Z", "")

                # finally, save the revisions we've seen to a varaible
                revisions.append(rev)

        # 'continue' tells us there's more revisions to add
        if 'continue' in api_answer:
            # replace the 'continue' parameter with the contents of the
            # api_answer dictionary.
            parameters.update(api_answer['continue'])
        else:
            break

    # return all the revisions for this page
    return(revisions)

category = "Harry Potter"

# we'll use another api called catscan2 to grab a list of pages in
# categories and subcategories. it works like all the other apis we've
# studied!
#
# The following requests call basically does the same thing as this string:
# "http://tools.wmflabs.org/catscan2/catscan2.php?depth=10&categories={0}&doit=1&format=json".format(category)
url_catscan = "http://tools.wmflabs.org/catscan3/catscan2.php"

parameters = {'depth' : 10,
              'categories' : category,
              'format' : 'json',
              'doit' : 1}

# r = requests.get("http://tools.wmflabs.org/catscan2/catscan2.php?depth=10&categories=Harry Potter&doit=1&format=json"

r = requests.get(url_catscan, params=parameters)
articles_json = r.json()
articles = articles_json["*"][0]["*"]

# open a file to write all the output
output = open("hp_wiki.tsv", "w", encoding="utf-8")
output.write("\t".join(["title", "user", "timestamp", "size", "anon", "minor", "revid"]) + "\n")

# for every article
for article in articles:

    # first grab the article's title
    title = article["a"]["title"]
    print(title)

    # get the list of revisions from our function and then iterate through it,
    # printing it to our output file
    revisions = get_article_revisions(title)
    for rev in revisions:
        output.write("\t".join(['"' + rev["title"] + '"', '"' + rev["user"] + '"',
                               rev["timestamp"], str(rev["size"]), str(rev["anon"]),
                               str(rev["minor"]), str(rev["revid"])]) + "\n")

# close the file, we're done here!
output.close()
    
    
