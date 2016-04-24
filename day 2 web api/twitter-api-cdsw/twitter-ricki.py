#use this for all twitter app
import time
import encoding_fix
import tweepy
from twitter_authentication import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
#done



#exercise 0: Get your first tweet in your current timeline
#get the first tweet of your timeline
single_tweet = api.home_timeline(count=1)
#get the actual tweet object
actual_single_tweet = single_tweet[0]
#in tweepy, a tweet is a "status"

user = api.get_user('7ricki')
# count1 = 1
# #exercise 1: Who are my followers?
# print(user.screen_name + " has "+ str(user.followers_count) + " followers.")
# print ("They include these 5 people: ")
# #step 1: get your followers (recent 5)
# for followers in user.followers(count=5):
# 	print(str(count1) + " : "+followers.screen_name)
# 	# time.sleep(1)
# 	print("And they have these 5 followers.")
# 	for followers_followers in followers.followers(count=5):
# 		print(followers_followers.screen_name)
# 		# time.sleep(1)
# 	count1 = count1 +1
#step 2: For each of your followers, get *their* followers (investigate time.sleep to throttle your computation)

#step 3: Identify the follower you have that also follows the most of your followers.

#step 4: How many handles follow you but none of your followers?

#step 5: Repeat this for people you follow, rather than that follow you.


tweets = api.home_timeline(count=20)

for tweet in tweets:
	if hasattr(tweet, 'retweeted_status'):
		print("Retweet from: "+tweet.author.screen_name)
	else:
		print("Original content from: "+tweet.author.screen_name)
	print(tweet.text+"\n")



#get each tweet's url -- below getting the first one
tweet.entities['urls'][0]['display_url']





