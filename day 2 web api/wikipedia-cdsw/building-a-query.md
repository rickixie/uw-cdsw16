Querying Wikipedia APIs from Python
===================================

Ben Lewis


This is an introduction to the [MediaWiki API][mw-api]; MediaWiki is the
software that runs Wikipedia and associated projects (and the CDSW wiki!), and
it exposes an API that lets users write queries and get information back about
practically any part of Wikipedia. The site I linked to describes the API and
all its various features, in more depth than we'll cover here.

[mw-api]: https://www.mediawiki.org/wiki/API:Main_page "API documentation."

# Making a call and parsing the pieces

    import requests
    ENDPOINT = 'https://en.wikipedia.org/w/api.php'
    wp_call = requests.get(ENDPOINT + '?'
        + 'action=query&'
        + 'prop=links&'
        + 'titles=User:Zen-ben&'
        + 'continue=&'
        + 'format=json')

What we have above is a call to the _Wikipedia API_. I've broken this apart into
separate, concatenated stanzas to make each section stand alone, but it would
work as one string too. This makes explaining each part easier, and provides a
clean segue into the next way we'll call this code.

## The endpoint

The string `https://en.wikipedia.org/w/api.php` is the _endpoint_ for this call;
this is the URL for the API itself. The part of the URL after the question mark
is called the _query_, and it defines the work you want the API to perform.

In order to avoid writing the same string over and over again, as well as avoid
errors, I've declared a variable called `ENDPOINT` for this specific string.
(It's all-caps to remind me to never write anything to it, only to read from
it.) We'll be using this string every time we make a request.

## The query

A query is a list of parameters you pass to a server as a part of a URL; not
every URL has them (in fact, most sites you browse to don't have them. They're
only really common when interacting with APIs.) The query in our request above
is everything that comes after the question mark; it separates the query from
the _path_, which in this case is `/w/api.php`. The query is composed of
parameter/value pairs, which have the form `parameter=value` and are separated
with ampersands (`&`).

### Action
By setting `action=query`, we're requesting information from the Wikipedia
servers. Note that this _query_ is unrelated to the _query string_; if we wanted
to edit Wikipedia via the API (which is possible, the syntax is different and
outside the scope of this session), we would write `action=edit` instead. The
`action` parameter is required in a MediaWiki API call.

#### Action parameter: Property
Using `prop=links` tells the API we want information about links on a page (or
pages) that we haven't specified yet. (That's in another parameter.)

#### Action parameter: Titles
The field `titles=User:Zen-ben` specifies that this query should return results
about the page about the "User:Zen-ben" page; this is my user page on
Wikipedia. If you go to https://en.wikipedia.org/wiki/User:Zen-ben, you'll see
that the format of the address to actually view my user page is the same as the
requested format here. This is not a coincidence; if you want to try another
page, look it up on Wikipedia and switch that name in here instead. (I recommend
experimenting!)

#### Action parameter: Continue
By supplying `continue=` with our query, we can get additional data in further
responses if there's more to our query than the response provides. (We'll use
this later.) Note that this paramter is supplied without a value. This is
acceptable.

#### Format
The data we get back from the Wikipedia API needs to have some structure; when
we provide the `format=json` string, we are requesting that our response be
formatted in JSON, which we have easy ways to handle (in particular, requests
has good support for it already.)

# Handling the results of our query
After calling the Wikipedia API, we have a response stored in the `wp_call`
variable. If we want to do anything with it, though, we need it in a form we
know how to deal with.

    response = wp_call.json()

This aptly-named function turns the JSON response we got from Wikipedia into a
dictionary we can access. From here, we can start looking for interesting
pieces. To start, we'll just iterate through the responses we have. You can go
ahead and just see the structure of `response` by typing it at your console;
you'll see that it's a dictionary with dictionaries inside of it.

When you first get a response from a web API, it can be hard to tell what's
actually in the response. Printing the JSON will tell you something, but it's
hard to read and very dense. After expanding the JSON into a dictionary with the
`json()` function, you can explore the contents of the dictionary:

    >>> response.keys()
    dict_keys(['continue', 'query'])

This tells us we have two keys in the response dictionary, `'continue'` and
`'query'`. We'll leave the `'continue'` key alone for now, and focus on
`'query'` for the time being. The `'query'` key is actually the response to the
query we just made, somewhat confusingly, but we can now explore what it is. The
fastest way to check is to use the `type()` function to see what type the value
is:

    >>> type(response['query'])
    <class 'dict'>

This tells us that `response['query']` is a dictionary, so we can call `.keys()`
on it:

    >>> response['query'].keys()
    dict_keys(['pages'])

So there's only one key in the `response['query']` dictionary; I'm going to pull
the value of that key out of the response, now, and put it in its own variable
so I don't have to keep rewriting all of these strings:

    >>> pages = response['query']['pages']
    >>> type(pages)
    <class 'dict'>
    >>> pages.keys()
    dict_keys(['44376332'])
    >>> type(pages['44376332'])
    <class 'dict'>
    >>> pages['44376332'].keys()
    dict_keys(['title', 'pageid', 'links', 'ns'])

So, here, I've dug down a few more layers. That long number there is actually
the `'pageid'` of my userpage; it's the identifier that Wikipedia uses
internally to find my page. `'ns'` is short for namespace; my page is in the
`User` namespace, which is namespace number 2 (but that's not important to our
current discussion.) Instead, let's look at the `'links'` key, which has the
details I'm interested in:

    >>> user_page = pages['44376332']
    >>> type(user_page['links'])
    <class 'list'>

Okay, so this is a list. Now instead of indexing by key, I need to index by
... well, index. So we can see what the type of the first element in the list
is:

    >>> type(user_page['links'][0])
    <class 'dict'>

Now, I happen to know that there are the keys `'title'` and `'ns'` (there's that
namespace again) inside this dictionary; we only really care about the `'title'`
key right now, however.

To recap: we're looking at a dictionary that contains a dictionary that contains
a dictionary that contains a list of dictionaries. Wow, that's a lot to keep
track of. Oh, and we want to do the same thing for each item in that list. We
know how to do that, though, because we have loops!

Instead of just using my handy `user_page` variable here, I'm going to make my
loop a bit more generic than just working with my single user page, so that we
can reuse it (or something similar) in the future. At first, I just want to see
the title of the pages (or single page) in the response:

    for page in response['query']['pages']:
        print(response['query']['pages'][page]['title'])

Okay, so that printed out the title of the page. But we can do more with this!
Now if we create _another_ loop inside of that loop, we can iterate over the
links in the list of links, and print _their_ titles:

    for page in response["query"]["pages"]:
        for link in response['query']['pages'][page]['links']:
            print(link['title'])

Now we've explored the structure of our query's response, and even built _nested
loops_ to see the contents of a list inside a dictionary.

# Building a better API call
That last call got us the information we needed, but it was a very long string
to write. Instead, the requests library has a better way to build an API call,
using a dictionary!

## Parameters dictionary
In requests, we can supply a dictionary of parameters with a GET request. So,
let's create our dictionary:

    parameters = {'action' : 'query',
                  'prop' : 'links',
                  'titles' : 'User:Zen-ben',
                  'format' : 'json',
                  'continue' : ''}

As you read each line, look back at the query we used before; note how instead
of each field being `"field=value&"`, now they're keys and values. We can run
our query again, this time without building that big huge string:

    wp_call = requests.get(ENDPOINT, params=parameters)

Now the reason for creating a variable to store the endpoint URL makes more
sense; suddenly, instead of having to rewrite that long string, you just have to
type out the variable name (a quick call to
`len("'https://en.wikipedia.org/w/api.php'")` tells me that typing out the
string, with delimiters, is 36 characters. `ENDPOINT`, on the other hand, is 8.)

We're going to use a slightly different call structure this time, and take
advantage of a field I mentioned but didn't do much with last time: the continue
field.

    while True:
        wp_call = requests.get('https://en.wikipedia.org/w/api.php', params=parameters)
        response = wp_call.json()

        for page in response["query"]["pages"]:
            for link in response['query']['pages'][page]['links']:
                print(link['title'])

        if 'continue' in response:
            parameters['continue'] = response['continue']['continue']
            parameters['plcontinue'] = response['continue']['plcontinue']
        else:
            break

Now, this block uses the "while true" idiom; basically, the loop will run until
you use the `break` keyword to force Python to exit the loop. We do this here to
take advantage of the continue field, because now you can call back to the API
and get more results (as you can see, there's more to the results printed this
time as opposed to before.) Basically, the continue field is a token that the
server uses to identify when a request isn't quite done, and you want to get
more results. By returning the exact string that the server sent, you're
requesting specifically the rest of the results for your query.

## Expanding the query

We can add to this query and get link information for more than one page; let's
also look at Mako's user page:

    parameters['titles'] += '|User:Benjamin Mako Hill'

The `+=` in the line above means "add to the existing variable", so in this case
it appends that string to the end of the string already stored at
`'titles'`. (In the file, the string has already been appended.) We're also
going to switch from printing out the contents of the response to storing the
links in lists instead, in a dictionary where the keys are the names of our
pages:

    page_links = {}

Now we're going to build a slightly different loop than we had before, because
we need to make sure each list is present before we change it:

    while True:
        wp_call = requests.get(ENDPOINT, params=parameters)
        response = wp_call.json()

        for page in response['query']['pages']:
            page_title = response['query']['pages'][page]['title']
            if page_title not in page_links:
                page_links[page_title] = []
            if 'links' in response['query']['pages'][page]:
                page_links[page_title].extend(response['query']['pages'][page]['links'])

        if 'continue' in response:
            parameters['continue'] = response['continue']['continue']
            parameters['plcontinue'] = response['continue']['plcontinue']
        else:
            break

Now we're building our dictionary of lists; because we'll sometimes not get
links for one page or another (it'll first give us links from Mako's user page,
and then it'll give links from mine) we need to test for the presence of the
`'links'` entry in the response dictionary. This is a good example of what's
called _sanitizing input_, or verifying that the data we're getting is in a
usable form. There's a lot of examples of unsanitized data causing unexpected
problems in software, some more benign than others. In this case, a missing
`'links'` key is completely expected, so we're fine with that value not being
present. In others, it would be an error that would require exiting before
something bad happened. (Figuring out when missing data is safe isn't easy, but
it's not impossible either. Ask me about it!)

Now that we have our data, we could run some rough statistics on it, like how
many entries there are, how many are shared between the two pages, if each shows
up in the other ... there's a lot of information to be had just from this
set. Those are questions I'll leave up to you, however, because I'd like to show
some other types of queries we can run.

# Getting revisions to an article
We've now learned how to build a query, how to look for different pieces, and
how to modify our basic query. Instead of continuing to look at links for the
moment, let's look into what we can do with another type of data the Wikipedia
API offers: revisions to articles.

Each _revision_ is a separate change to a Wikipedia article. The revision
datatype in the Wikipedia API captures all sorts of metadata about the change
made, in addition to the actual content of the change; it captures the username
(or another identifier, we'll talk about that in a moment), the time the change
was made, the comment the user making the change left in the comment field, and
a hash of the change (a unique number generated from the content of the change
to represent it.) We'll be looking at usernames and a flag that gets set for
some of them. (A flag is a boolean value, `true` or `false`, which is normally
`false` unless some specific condition is met.)

As before, there's much more to this API than what we're covering here. I highly
recommend visiting the API documentation and reading more there.

## Looking for anonymous editors
One of Wikipedia's greatest strengths (or weaknesses) is that it allows
anonymous editors; people who haven't logged into the site can edit its
contents. This both allows people who don't want to (or don't care to) create
accounts to contribute, but also makes tracking contributions a bit harder.

Now, let's take some time to look at who's contributing to the article on
Python! (Since my user page is rather boring, really.) There's far more
revisions to work with, for one thing.

### While loops: looping on an indeterminate condition
So we have for loops. They're great, they let us iterate through items in a list
or keys in a dictionary. But what if we don't know how long something will take?
Then we need some other sort of loop. Enter the `while` loop; this loop checks
its condition before running, then runs the loop and re-checks the condition. As
long as its condition is true, it will continue running.

    iter = 0
    while iter < 10:
        iter = iter + 1
        print(iter)

Go ahead and run the block of code above in your interpreter. Note how it prints
the numbers 1 through 10 and then stops; this is a basic while loop. Now let's
write it a different way:

    iter = 0
    while True:
        iter = 1
        print(iter)
        if iter > 9:
            break

If you ran the block of code above, you'll note that your interpreter is still
churning away, printing 1s. Press Control-C to interrupt the loop and break
it. There's a bug in the logic there, and yes, it was intentional. Try fixing
it, then look at the following fixed version if you can't see it:

    iter = 0
    while True:
        iter = iter + 1
        print(iter)
        if iter > 9:
            break

That's better. Being able to break out of an infinite loop is a useful skill to
have, and being able to recognize when your code is stuck in a loop is also
useful.

Additionally, you might notice I have the keyword `break` in my code; that's a
keyword that tells Python to exit the loop it's currently in. It's a fast way to
exit a loop when you've found the item you're looking for, or end a loop if
you've finished handling some task (like we're about to do.)

### Checking for anonymous users
Now we have the tools we need to look at the complete history of the Python
article; we have the 'continue' tag, we have a set to store our anonymous users
in, and we can start writing some code:

    parameters = { 'action' : 'query',
                   'prop' : 'revisions',
                   'titles' : 'Python (programming language)',
                   'rvlimit' : 100,
                   'rvprop' : 'timestamp|user',
                   'format' : 'json',
                   'continue' : '' }

    anon_editors = set()
    while True:
        wp_call = requests.get(ENDPOINT, params=parameters)
        response = wp_call.json()
        for page_id in response['query']['pages']:
            revisions = response['query']['pages'][page_id]['revisions']
            for rev in revisions:
            if 'anon' in rev:
                    anon_editors.add(rev['user'])

        if 'continue' in response:
            parameters['continue'] = response['continue']['continue']
            parameters['plcontinue'] = response['continue']['plcontinue']
        else:
            break

Now that we have the number of edits made by anonymous versus logged-in editors,
we can sum the number of edits by each, and see the different counts:

    anon_edit_count = 0
    logged_in_edit_count = 0
    for editor in anon_editors:
        anon_edit_count += anon_editors[editor]
    for editor in logged_in_editors:
        logged_in_edit_count += logged_in_editors[editor]

    print_params = { 'anon_edits' : anon_edit_count,
                     'logged_in_edits' : logged_in_edit_count,
                     'total_edits' : anon_edit_count + logged_in_edit_count }
    print("Anonymous editors made %anon_edits edits to the Python page, while "
                     "logged-in editors made %logged_in_edits edits, for a total "
                     "of %total_edits edits." % print_params)

# Resources and references
