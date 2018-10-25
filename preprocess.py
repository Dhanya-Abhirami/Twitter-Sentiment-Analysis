import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
def simplify(self,tweet):
		'''
		Preprocess the tweet 
		'''    
    	#Convert to lower case
		tweet = tweet.lower()
		#Convert www.* or https?://* to URL
		tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
		#Convert @username to AT_USER
		tweet = re.sub('@[^\s]+','AT_USER',tweet)
		#Remove additional white spaces
		tweet = re.sub('[\s]+', ' ', tweet)
		#Replace #word with word
		tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
		# Remove RT (retweet)
		tweet = re.sub(r'rt', '', tweet)
		# Replace 2+ dots with space
		tweet = re.sub(r'\.{2,}', ' ', tweet) 	
		# Remove punctuation
		tweet = tweet.strip('\'"?!,.():;')
		# Convert more than 2 letter repetitions to 2 letter funnnnny --> funny
		tweet = re.sub(r'(.)\1+', r'\1\1', tweet)
		# Remove - & '
		tweet = re.sub(r'(-|\')', '', tweet)
		# Smile -- :), : ), :-), (:, ( :, (-:, :')
		tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
		# Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
		tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
		# Love -- <3, :*
		tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
		# Wink -- ;-), ;), ;-D, ;D, (;,  (-;
		tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
		# Sad -- :-(, : (, :(, ):, )-:
		tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
		# Cry -- :,(, :'(, :"(
		tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
		word_tokens = word_tokenize(tweet)
		stop_words = set(stopwords.words('english'))
		filtered_tweet = [w for w in word_tokens if w not in stop_words]
		ps = PorterStemmer()
		word_stem = []
		for w in filtered_tweet:
			word_stem.append(ps.stem(w))
		return " ".join(filtered_tweet) 