import tweepy
from tweepy import OAuthHandler
import preprocess
import csv
import json
import time
from textblob import TextBlob
import credentials
class analyse(object):
	def __init__(self):
		'''		
		Constructor to initialise Twitter app credentials
		'''			
		# keys and tokens from the Twitter Dev Console
		consumer_key =credentials.consumer_key
		consumer_secret=credentials.consumer_secret
		access_token=credentials.access_token
		access_token_secret=credentials.access_token_secret
	 
		# attempt authentication
		try:
		    # create OAuthHandler object
		    self.auth = OAuthHandler(consumer_key, consumer_secret)
		    # set access token and secret
		    self.auth.set_access_token(access_token, access_token_secret)
		    # create tweepy API object to fetch tweets
		    self.api = tweepy.API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
		except:
		    print( "Error: Authentication Failed")
		print( "Authenticated\nI am collecting Twitter Data, please wait...\n")
 
	def get_data(self, query, count):
		'''
		Main function to fetch tweets and parse them.
		''' 
		searched_tweets=[]
		max_id = -1
		while len(searched_tweets)<count:
			remaining_tweets = count - len(searched_tweets)
			try:
				# call twitter api to fetch tweets
				if (max_id <= 0):
					new_tweets = self.api.search(q = query, count = remaining_tweets,tweet_mode = 'extended')
				else:
					new_tweets = self.api.search(q = query, count = remaining_tweets,tweet_mode = 'extended',max_id=str(max_id - 1))
				# if no new tweets found
				if not new_tweets:
					break
				searched_tweets.extend(new_tweets)
			    # parsing tweets one by one
				with open("tweet_corpus.json",'a+') as file:
					for tweet in new_tweets:
						if tweet.lang=='en':
							simple=preprocess.simplify(self,tweet.full_text)
							analysis = TextBlob(simple)
							if analysis.sentiment.polarity>0:
								senti=1
							elif analysis.sentiment.polarity<0:
								senti=-1
							else:
								senti=0
							if(senti!=0):
								json.dump([simple,senti], file)
								file.write('\n')
				max_id = new_tweets[-1].id
			except tweepy.TweepError as e:
				# print( error (if any)
				print( "Exception : " + str(e))
				time.sleep(15*60)
		print( "Labelled Dataset of Tweets Created")
  	
def main():
	# creating object of analyse Class
    	api = analyse()
    	api.get_data(query = "#GSTbill -filter:retweets", count = 10000)
	
if __name__ == "__main__":
	# calling main function
	main()
