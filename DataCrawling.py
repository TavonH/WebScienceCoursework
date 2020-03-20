# Adopted by YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import authentication
from emotion_lexicon import emotion_lexicon as le


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        pass

    def stream_tweets(self, filename, hashtag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API

        #Creating a StreamListener
        listener = StdOutListener(filename)

        #Creating a Stream
        auth = OAuthHandler(authentication.API_KEY, authentication.API_SECRET_KEY)
        auth.set_access_token(authentication.ACCESS_TOKEN, authentication.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        #Start Streaming
        stream.filter(track=hashtag_list, languages=['en'])


# # # # STANDARD STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, filename):
        self.fetched_tweets_filename = filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status_code):
        #Print the error according to the status code
        print(status_code)
        if status_code == 420:
            print("App is being rate limited for making too many requests")
            return False


if __name__ == '__main__':
    # Authenticate using config.py and connect to Twitter Streaming API.
    hashtag_list = le.total
    filename = "tweets_sample.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(filename, hashtag_list)