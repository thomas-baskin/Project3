# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Getting data
# This notebook walks us through the following methods of obtaining data:
# * Using Pandas to read delimited files
# * Getting raw HTML from a website
# * Parsing HTML
# * Using an API to get web data (we'll demonstrate with the Twitter API)

# %%
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# %% [markdown]
# ## Using Pandas to read delimited files

# %%
# Comma-separated values
iris = pd.read_csv('iris.csv')
display(iris.head())

# Comma-separated values with no headers
iris = pd.read_csv('iris-no-headers.csv', names=['sepal_length','sepal_width','petal_length','petal_width','species'])
display(iris.head())

# Tab-delimited files
iris = pd.read_csv('iris.txt', delimiter='\t')
display(iris.head())

# %% [markdown]
# ## Get content from a website
# 
# ### Legal implications
# (See [here](https://benbernardblog.com/web-scraping-and-crawling-are-perfectly-legal-right/) for a layperson's guide to the legal implications of scraping and crawling.)
# 
# We are bound to websites' terms of service in scraping data from the web. For example, the RottenTomatoes Terms of Use states:
# >...you agree that you will not use the Services, or duplicate, download, publish, modify or otherwise distribute or use any material in the Services for any purpose, except for your personal, non-commercial use...You may not download (other than page caching) or modify the Services or any portion of them unless we have provided you with express written consent. ([Fandango Terms of Use](https://www.fandango.com/policies/terms-of-use))
# 
# Why are website administrators concerned about this? A number of reasons:
# * Websites can be copyrighted. If they have public data, the data isn't copyrighted, but the presentation of the data is.
# * Sometimes people that scrape websites aren't responsible and can overload the website with requests.
# * Businesses sometimes use scraping for competitive advantage.
# 
# Some websites, like [Wikipedia](https://meta.wikimedia.org/wiki/Terms_of_use), are fairly free with their terms of service. But in most cases, you should use an API if one is available.
# 
# Some websites have a _robots.txt_ file (see, for example, [reddit.com/robots.txt](https://www.reddit.com/robots.txt)) that guides web crawlers on any content they shouldn't request. Sometimes the file includes a `crawl-delay` or `Request-rate`, both of which set a limit at which web crawlers should request pages. Most or all popular websites also has software that checks for crawlers and robots that either are not respecting their terms of use or are hitting the site with overly many requests. To be safe, you should limit your page requests to one per 10-15 seconds. (Yeah, lame, I know.)
# 
# ### Scraping
# Uses the [requests library](http://docs.python-requests.org/en/latest) (at the commandline: `pip install requests`)
# 
# Looks at the homepages of various news websites and counts the number of mentions of 'Repulican', 'Democrat', and 'Trump'. We chose these websites to get news across the political spectrum. See [this website](https://www.allsides.com/media-bias/media-bias-chart). (Daily Kos is not listed on that chart, but it is generally accepted to be liberal.)
# 
# **Warning**: The following code may not conform to the Terms of Service of the six news websites.

# %%
import requests

urls = {
    'Daily Kos':'https://www.dailykos.com',
    'Politico':'http://politico.com',
    'Reuters':'http://reuters.com',
    'AP':'https://apnews.com',
    'Fox news':'http://foxnews.com',
    'The Blaze':'https://www.theblaze.com'
}

sites = [requests.get(url) for url in urls.values()]
list(sites[0])[0]


# %%
import re

rep_matches = [len([m for m in re.finditer('(R|r)epublican', html.text)]) for html in sites]
dem_matches = [len([m for m in re.finditer('(D|d)emocrat', html.text)]) for html in sites]
trump_matches = [len([m for m in re.finditer('Trump', html.text)]) for html in sites]

df = pd.DataFrame({'Site':list(urls.keys()), 'Republican':rep_matches, 'Democrat':dem_matches, 'Trump':trump_matches})
df


# %%
N = len(sites)

fig, ax = plt.subplots()

ind = np.arange(N)    # the x locations for the groups
width = 0.28         # the width of the bars
p1 = ax.bar(ind, df.Republican, width, color='r')
p2 = ax.bar(ind+width, df.Democrat, width, color='b')
p3 = ax.bar(ind+2*width, df.Trump, width, color='g')

ax.set_title('News website homepage mentions by group')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(df.Site)

ax.legend((p1[0], p2[0], p3[0]), ('Republican', 'Democrat', 'Trump'))
ax.autoscale_view()

# %% [markdown]
# ## Parse HTML
# 
# Uses the following libraries:
# * [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup) (at the commandline: `pip install beautifulsoup4`) - builds a tree out of a webpage
# * html5lib (at the commandline: `pip install html5lib`) - HTML parser that's better than the default Python HTML parser
# 
# We're going to look at the list of action/adventure movies listed [here](https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies).
# 
# **Warning**: the following code does not conform to RottenTomatoes's terms of use.
# %% [markdown]
# ### Request the html and build a tree

# %%
from bs4 import BeautifulSoup
import requests

# Request the raw html from the webpage
html = requests.get('https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/')

# Build a tree, or nested data structure, from the webpage
soup = BeautifulSoup(html.text, 'html5lib')

# %% [markdown]
# ### Get the table listing the movies and extract the links from each entry

# %%
import re

# Try to get links of top movies
# soup('a', {'class':'unstyled articleLink'})
# Hmm, got a lot more than that

# Get all the tables in the html document
tables = soup('table', {'class':'table'})
table = tables[0]
links = table('a', {'class':'unstyled articleLink'})

# %% [markdown]
# ### Get the text from each link which has the title of the movie

# %%
titles = [link.text for link in links]
titles

# %% [markdown]
# ### Use regular expressions to extract the title
# `\s` is whitespace, `\S` is non-whitespace, `\d` is a digit

# %%
matches = [re.search('\\n\s*(\S.*) \((\d*)', text) for text in titles]
# movies = [(m[1], int(m[2])) for m in matches]
# movies = [type('movie', (object,), {'title':m[1],'year':int(m[2])}) for m in matches]

class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year
    def __str__(self):
        return '{} ({})'.format(self.title, self.year)
        
movies = [Movie(m[1], int(m[2])) for m in matches]

print('\n'.join([str(m) for m in movies]))


# %%
fig, ax = plt.subplots()
years = [movie.year for movie in movies]
plt.hist(years, bins=30)
_ = ax.set_title('Top action/adventure movies - RottenTomatoes')

before1940 = [movie.title for movie in movies if movie.year < 1940]
print('Top movies made before 1940: ', before1940)

sixties = [movie.title for movie in movies if movie.year < 1960 and movie.year > 1954]
print('Top movies made between 1954 and 1960: ', sixties)

# %% [markdown]
# # Using an API
# An API is the best way to go to get data from the internet.
# 
# According to [this website](https://ahrefs.com/blog/most-visited-websites/) the top 10 websites from search engine traffic are:
# 1. youtube.com
# * en.wikipedia.org
# * facebook.com
# * twitter.com
# * amazon.com
# * imdb.com
# * reddit.com
# * pinterest.com
# * ebay.com
# * tripadvisor.com
# 
# All of these websites have APIs. Facebook's API is used mostly for development. There is a search API but there are very strict controls and you need to get permissions from Facebook. TripAdvisor's API is for customer-facing websites only -- not for a project like what we're doing.
# %% [markdown]
# ## Twitter API
# 
# We'll use the [Tywthon library](https://twython.readthedocs.io/en/latest/) (`pip install twython`). Go [here](https://twython.readthedocs.io/en/latest/usage/starting_out.html#beginning) to get everything set up.
# * You may need to create an account and then go again to this link
# * You will need a developer account - getting a developer account can take some time as they have a human review every request, so if you want to use Twitter get started early!
# 
# We'll be using OAuth 2.

# %%
from twython import Twython
import json


# %%
# Get keys from TWITTER_CREDS_FN or https://developer.twitter.com/en/apps/16087482
# NOTE: do not run this cell unless you get the API keys from twitter.com.
CONSUMER_KEY = ''
CONSUMER_SECRET_KEY = ''
ACCESS_TOKEN_SECRET = ''
TWITTER_CREDS_FN = '/Users/edwajohn/.twitter-credentials.json'

if (CONSUMER_KEY != ''):
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET_KEY, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()

    # Save creds to json file
    creds = {'CONSUMER_KEY':CONSUMER_KEY, 'CONSUMER_SECRET_KEY':CONSUMER_SECRET_KEY,
             'ACCESS_TOKEN':ACCESS_TOKEN, 'ACCESS_TOKEN_SECRET':ACCESS_TOKEN_SECRET}
    with open(TWITTER_CREDS_FN, 'w') as outfile:  
        json.dump(creds, outfile)


# %%
try:
    with open(TWITTER_CREDS_FN) as data_file:
        data = json.load(data_file)
        CONSUMER_KEY = data['CONSUMER_KEY']
        CONSUMER_SECRET_KEY = data['CONSUMER_SECRET_KEY']
        ACCESS_TOKEN = data['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = data['ACCESS_TOKEN_SECRET']
#         print('CONSUMER_KEY={}\nCONSUMER_SECRET_KEY={}\nACCESS_TOKEN={}\nACCESS_TOKEN_SECRET={}'.format(
#             CONSUMER_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET))
except IOError:
    print("Could not read file: ~/.twitter-credentials.json. Please Instantiate object with your username and password")


# %%
# ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(CONSUMER_KEY, access_token=ACCESS_TOKEN)
# twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET_KEY, oauth_version=2)
# search = twitter.search(q='impeach', tweet_mode='extended')
# search['statuses'][0]
# search['statuses'][0]['user']['screen_name']
# search['statuses'][0]['full_text']
# search['statuses'][0]['created_at']


# %%
statuses = twitter.search(q='impeach', tweet_mode='extended', count=5000)['statuses']
for status in statuses:
#     print(status['user']['screen_name'])
#     print(status['created_at'])
    if 'retweeted_status' in status:
#         print(status["retweeted_status"]['full_text'])
        status['full_text'] = status["retweeted_status"]['full_text']
#     else:
#         print(status['full_text'])
#     print()
    
texts = [status['full_text'] for status in statuses]

# Create a dataframe with three columns: trump, pelosi, and mcconnell
trump = [text.lower().count('trump') for text in texts]
schiff = [text.lower().count('schiff') for text in texts]
bolton = [text.lower().count('bolton') for text in texts]
mcconnell = [text.lower().count('mcconnell') for text in texts]
romney = [text.lower().count('romney') for text in texts]
d = {'trump':trump, 'schiff':schiff, 'bolton':bolton, 'mcconnell':mcconnell, 'romney':romney}
df = pd.DataFrame(data=d)

df.head()


# %%
x_values = df.mean()*100
xticks = range(1, len(df.columns)+1)
plt.bar(xticks, x_values)
plt.ylabel('Percent mentions')
plt.xticks(xticks, df.columns)
plt.title("Who's the biggest player in the impeachment?")

plt.show()

# %% [markdown]
# # Twitter Streaming API

# %%
from twython import TwythonStreamer
from collections import Counter

tweets = []

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        tweets.append(data)
        print('received tweet #{}'.format(len(tweets)))
        if len(tweets) >= 100:
            self.disconnect()
#         if data['lang'] == 'en':
#             tweets.append(data)
#             print('received tweet #{}'.format(len(tweets)))
            
#             if len(tweets) >= 1000:
#                 self.disconnect()
                
    def on_error(self, status_code, data):
        print('Error. status_code={}, data={}'.format(status_code, data))
        self.disconnect
        
ACCESS_TOKEN = '1088546875932692480-SPPBZkQ5uw80TIPeloFf5MdhYJyeKI'
ACCESS_TOKEN_SECRET = 'gU5LfWDrNAgTuxYwS5Ym6SDHTZy9yVhvZQN4zY07uhTvx'

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Starts consuming public statuses that contain the keyword 'trump'
stream.statuses.filter(track='trump')

# consume a sample of *all* public statuses
# stream.statuses.sample()


# %%
display(tweets[0])

# top_hashtags = Counter(hashtag['text'].lower()
#                       for tweet in tweets
# #                       for hashtag in tweet['entities']['hashtags']
#                       if 'entities' in tweet)

t = [tweet['text'] for tweet in tweets if 'text' in tweet]
t


# %%


# %% [markdown]
# # Wikipedia API
# To install the Wikipedia API: `pip3 install wikipedia-api`
# 
# See [here](https://pypi.org/project/Wikipedia-API/) for further documentation.

# %%
import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)
wiki_html = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.HTML
)


# %%
py_wiki = wiki_wiki.page('Python_(programming_language)')
print('title: {}'.format(py_wiki.title))
print()
print('summary: {}'.format(py_wiki.summary))
print()
print('full text: {}'.format(py_wiki.text))


# %%
py_html = wiki_html.page('Python_(programming_language)')
print('title: {}'.format(py_html.title))
print()
print('summary: {}'.format(py_html.summary))
print()
print('full text: {}'.format(py_html.text))


# %%
sections = py_wiki.sections
top_level_titles = [section.title for section in sections]
top_level_titles


# %%
def print_section_titles(section, prefix):
    print(prefix+section.title)
    for subsection in section.sections:
        print_section_titles(subsection, prefix+'  ')

for section in sections:
    print_section_titles(section, '')


