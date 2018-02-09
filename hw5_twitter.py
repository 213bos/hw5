from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: Wednesday 9:00-10:30 AM
## Any names of people you worked with on this assignment:

# usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this
CACHE_FNAME = "twitter_cache.json"
try:
    cache_file = open(CACHE_FNAME,'r') #reading the data from the cache file
    cache_contents = cache_file.read() # get the data into a string
    CACHE_DICTION = json.loads(cache_contents) #load that stuff info a dictionary
    cache_file.close() # close that file when were done with it

except:
    CACHE_DICTION = {} # if there is nothing there, make sure that CACHE_DICTION is empty
# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)
def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

#Code for Part 1:Get Tweets
baseURL = "https://api.twitter.com/1.1/statuses/user_timeline.json"
response = requests.get(baseURL, params = {"screen_name": 'umsi', "count": 25}, auth=auth)
tweets = response.text
tweet_json = json.loads(tweets)
# print(tweet_json)

json_new = open('tweet.json', 'w')
json_new.write(json.dumps(tweet_json, indent=2))
json_new.close()



tokens = []
for tweet_dict in  tweet_json:
    tokens+= nltk.word_tokenize(tweet_dict['text'])
#Creates frequency distribution from list
#Notice how you can incorporate conditional statements here
freqDist = nltk.FreqDist(token for token in tokens if (token.isalpha() and ("RT" not in token) and ("http" not in token) and ("https" not in token)))
#Loop through and print the words and frequencies for the most common 5 words
for word, frequency in freqDist.most_common(5):
    print(word + " " + str(frequency))




if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
        #
