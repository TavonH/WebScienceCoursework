import json
import os
import re
import pandas as pd
import preprocessor as p
import emoji
import string
from nltk.corpus import stopwords
from textblob import TextBlob
import spacy
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from emotion_lexicon import emotion_lexicon_tuple as le

nlp = spacy.load('en_core_web_md', disable=['ner'])
nlp.remove_pipe('tagger')
nlp.remove_pipe('parser')

#Extract emoji from tweet. This function returns a list
def extract_emojis(str):
    emojis = ''.join(c for c in str if c in emoji.UNICODE_EMOJI)
    emojis_list = list(emojis.strip())
    return emojis_list

#Clean tweets text to make sentiment analysis more precise
def clean_tweets(tweet):
    #Remove URLs, mentions, emojis
    p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.EMOJI)
    clean_tweet = p.clean(tweet)
    clean_tweet = re.sub(r':', '', clean_tweet)
    return clean_tweet

# Natue Language Processing from https://colab.research.google.com/drive/1Dc6rlxrsvYd0l8Bph66ydwNV05hBS-CX
#@Tokenize
def spacy_tokenize(string):
    tokens = list()
    doc = nlp(string)
    for token in doc:
        tokens.append(token)
    return tokens

#@Normalize
def normalize(tokens):
  normalized_tokens = list()
  for token in tokens:
    normalized = token.text.lower().strip()
    if ((token.is_alpha or token.is_digit)):
      normalized_tokens.append(normalized)
  return normalized_tokens

#@Lemmatizer from https://www.cnblogs.com/jclian91/p/9898511.html
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def Nature_Language_Processing(tweet):
    tokens = normalize(spacy_tokenize(tweet))
    tagged_sent = pos_tag(tokens)
    wnl = WordNetLemmatizer()
    lemmas_sent = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemmas_sent.append(wnl.lemmatize(tag[0], pos=wordnet_pos))
    return lemmas_sent

#Filter tweets text to make it easier to train the machine learning models
def filter_tweets(tweet):
    #Remove stopwords and punctuations
    stop_words = set(stopwords.words('english'))
    word_tokens = Nature_Language_Processing(tweet)
    filtered_tweet = []
    for w in word_tokens:
        # check tokens against stop words and punctuations
        if w not in stop_words and w not in string.punctuation:
            filtered_tweet.append(w)
    return filtered_tweet

#Get the system path
path = os.getcwd()
path = path + '/tweets_sample.json'
print(path)

#Load json file to a tweets list
tweets = []
for line in open(path, 'r'):
    tweets.append(json.loads(line))

#Construct a dataframe.
tweets_dict = {'tweet_id': [],
               'created_at': [],
               'text': [],                          #String
               'display_text_range': [],
               'clean_text': [],                    #list
               'filtered_text': [],                 #list
               'hashtags': [],
               'emoji': [],                         #list
               'sentiment': [],                     # polarity: [-1.0,1.0], negative < 0, positive > 0; subjectivity: [0.0,1.0], More subjective, more reliable
               'scores': [],
               'label': [],
               'keep': []}

# Clean Tweets and Text progressing
for tweet in tweets:
    if ('text' in tweet.keys()) & ('truncated' in tweet.keys()):
        #Drop Retweets
        if tweet['text'][:2] != 'RT':
            #Get id of this tweet
            tweets_dict['tweet_id'].append(tweet['id_str'])
            #Get created_at of this tweet
            tweets_dict['created_at'].append(tweet['created_at'])
            # Initial scores
            score = {'excitement': 0,
                     'happy': 0,
                     'pleasant': 0,
                     'surprise': 0,
                     'fear': 0,
                     'angry': 0}
            tweets_dict['scores'].append(score)
            # Initial 'keep'
            tweets_dict['keep'].append(0)
            # Initial labels
            tweets_dict['label'].append('')
            if tweet['truncated'] == False:
                # Get text of this tweet
                tweets_dict['text'].append(tweet['text'])
                # Get displayed text range of this tweet
                tweets_dict['display_text_range'].append([0, len(tweet['text'])])
                # Extract emojis from this tweet
                tweets_dict['emoji'].append(extract_emojis(tweet['text']))
                # sentiment analysis this tweet
                cleaned_text = clean_tweets(tweet['text'])
                tweets_dict['clean_text'].append(cleaned_text)
                blob = TextBlob(cleaned_text)
                sentiment = {'polarity': blob.sentiment.polarity,
                             'subjectivity': blob.sentiment.subjectivity}
                tweets_dict['sentiment'].append(sentiment)
                # Filter text
                filtered_text = filter_tweets(cleaned_text)
                tweets_dict['filtered_text'].append(filtered_text)
                # Get hashtags and its indices of this tweet
                tags = []
                for tag in tweet['entities']['hashtags']:
                    tags.append(tag)
                tweets_dict['hashtags'].append(tags)
            else:
                #Get text of this tweet
                tweets_dict['text'].append(tweet['extended_tweet']['full_text'])
                # Get displayed text range of this tweet
                tweets_dict['display_text_range'].append([0, len(tweet['extended_tweet']['full_text'])])
                # Extract emojis from this tweet
                tweets_dict['emoji'].append(extract_emojis(tweet['extended_tweet']['full_text']))
                # sentiment analysis this tweet
                cleaned_text = clean_tweets(tweet['extended_tweet']['full_text'])
                tweets_dict['clean_text'].append(cleaned_text)
                blob = TextBlob(cleaned_text)
                sentiment = {'polarity': blob.sentiment.polarity,
                             'subjectivity': blob.sentiment.subjectivity}
                tweets_dict['sentiment'].append(sentiment)
                # Filter text
                filtered_text = filter_tweets(cleaned_text)
                tweets_dict['filtered_text'].append(filtered_text)
                # Get hashtags and its indices of this tweet
                tags = []
                for tag in tweet['extended_tweet']['entities']['hashtags']:
                    tags.append(tag)
                tweets_dict['hashtags'].append(tags)
tweets_df = pd.DataFrame(tweets_dict)

# Drop the duplicates
tweets_df.drop_duplicates('clean_text', 'first', inplace=True)
print('DataFrame Constructed.')

# Labelling
# label = hashtags_score + emojis_score + sentiment_score
# sentiment_score = |polarity * subjectivity| (p or n is according to wheather the score is bigger than 0)

for row in tweets_df.iterrows():
    tweet = row[1]
    # Calculate sentiment score for this tweet
    # positive words ('excitement','happy', 'pleasant')
    # negative words ('surprise', 'fear', 'angry')
    sentiment_score = tweet['sentiment']['polarity'] * tweet['sentiment']['subjectivity']
    if sentiment_score > 0:
        tweet['scores']['excitement'] += sentiment_score
        tweet['scores']['happy'] += sentiment_score
        tweet['scores']['pleasant'] += sentiment_score
    elif sentiment_score < 0:
        tweet['scores']['surprise'] += -(sentiment_score)
        tweet['scores']['fear'] += -(sentiment_score)
        tweet['scores']['angry'] += -(sentiment_score)
    
    # Calculate hashtags score
    hashtags = []
    last_index = tweet['display_text_range'][1]
    for tag in tweet['hashtags'][::-1]:
        if tag['indices'][1] == last_index:
            normalized_hastag = normalize(spacy_tokenize(tag['text']))
            if len(normalized_hastag):
                hashtags.append(normalize(spacy_tokenize(tag['text']))[0])
                last_index = tag['indices'][0] - 1
        else:
            break
    for tag in le.total:
        score = len(set(hashtags) & set(tag))
        tweet['scores'][tag[0]] += score

    # Calculate emoji score
    i = 0
    emos = ['excitement', 'happy', 'pleasant', 'surprise', 'fear', 'angry']
    for emoji in le.total_emoji:
        score = (len(set(tweet['emoji']) & set(emoji))) * 0.5
        tweet['scores'][emos[i]] += score
        i += 1

    # Label this tweet
    score_dict = tweet['scores']
    max_score = max(score_dict.values())
    max_list = [k for k, v in score_dict.items() if v == max_score]
    flag = 0
    if len(max_list) == 1:
        tweets_df.loc[row[0], 'label'] = max_list[0]
        tweets_df.loc[row[0], 'keep'] = '1'
        flag = 1
    print('----------------')
    print(score_dict)
    print('label ' + tweets_df.loc[row[0], 'label'])
    print('keep: ' + str(tweets_df.loc[row[0], 'keep']))
    print('----------------')

tweets_df.to_csv('tweets.csv')
print('Label successful.')

excitement_list = []
happy_list = []
pleasant_list = []
surprise_list = []
fear_list = []
angry_list = []
c_name = tweets_df.keys()

for row in tweets_df.iterrows():
    tweet = row[1]
    if tweet['keep'] == '1':
        if tweet['label'] == 'excitement':
            excitement_list.append(tweet.values)
        elif tweet['label'] == 'happy':
            happy_list.append(tweet.values)
        elif tweet['label'] == 'pleasant':
            pleasant_list.append(tweet.values)
        elif tweet['label'] == 'surprise':
            surprise_list.append(tweet.values)
        elif tweet['label'] == 'fear':
            fear_list.append(tweet.values)
        elif tweet['label'] == 'angry':
            angry_list.append(tweet.values)

pd.DataFrame(columns=c_name, data=excitement_list).to_csv('excitement.csv')
pd.DataFrame(columns=c_name, data=happy_list).to_csv('happy.csv')
pd.DataFrame(columns=c_name, data=pleasant_list).to_csv('pleasant.csv')
pd.DataFrame(columns=c_name, data=surprise_list).to_csv('surprise.csv')
pd.DataFrame(columns=c_name, data=fear_list).to_csv('fear.csv')
pd.DataFrame(columns=c_name, data=angry_list).to_csv('angry.csv')




