import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import time
import numpy as np
# Tweepy login credentials for Twitter API
#consumer key, consumer secret, access token, access secret.
ckey="kI0kERGmUK4sxTmgcCntCCHmF"
csecret="ULPUE5BTlm68qH253Ul2MhFGpfe6VLyIGNAoX1DfFLp7hCXa8m"
atoken="725346482287685633-YmG7EsWnhYkJecqzSLNNI4cIm1hlh2m"
asecret="Kn6Bb7oBITgyhUHWUlVk48AiMxXPOVjwjQssuV7LvjmWw"
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
###################################################################################
# Plotly login credentials
tls.set_credentials_file(username="davidyanju",api_key="qpqckqaumc",stream_ids=["ns0r5d781h","3zw49r7kbf","6duefewb8y","rez5fuf8md","t0rvu7bmoz"])
stream_ids = tls.get_credentials_file()['stream_ids']
####################################################################################
# Function to analyse tweets and check if the tweets are positive or negative.
def tweetanalytics(twit):
    file_one=open("positive_keywords.txt","r")
    file_two=open("negative_keywords.txt","r")
    fh_o= file_one.readlines()# this reads the lines for the positive keywords
    fh_t= file_two.readlines()# this reads the lines for the negative keywords
    n = 0# initializes n
    p = 0# initializes p
    p_value =1# sets the p_value to 1
    n_value =-1# sets the n _value to -1
    # The for loop iterates each line in both the negative and the positve keywords text and check if these words are
    # found in a tweet.
    for i,j in zip(fh_o,fh_t):
        flow_one = " "+i.strip() # removes all characters except alphabets and assigns string to flow_one
        flow_two = " "+j.strip() # removes all characters except alphabets and assigns string to flow_two
        if flow_one in twit:
            p = p+1 # count how many times a positive keyword appears in a tweet.
        if flow_two in twit:
            n = n+1 # count how many times a positive keyword appears in a tweet.
        else:
            pass
    if p>0 and n== 0:
        return p_value # returns a positive value (1)
    if n>0 and p ==0:
        if n%2 == 0:
            return p_value # returns a positive value (1)
        if n%2!= 0:
            return n_value # returns a positive value (-1)
    if p >0 and n>0:
        if n%2 == 0:
            return p_value # returns a positive value (1)
        if n%2!= 0:
            return n_value # returns a positive value (-1)
    else:
        return 0 # returns a zero value
####################################################################################
# Class that listens to twitter for tweets that matches my search words.
class listener(StreamListener):
    def on_data(self, data):
        try:
            import datetime
            # tweet value is splits the details of a tweet and extracts the actual tweet.
            tweet = data.split(',"text":"')[1].split('","source')[0]
            tweet = str(tweet) # this makes the tweet a string
            print tweet
            y = int(tweetanalytics(tweet)) # this sends the tweet to be analyzed to detect if the tweet is positive
            # or negative. this is done by calling the tweetanalytics function
            print y
            x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') # the will check the date and time and  acts
            # as the time series.
            s_1.write(dict(x=x,y=y)) # this writes the data to the plotly API for the popularity stream
            # i count the number of tweets for each keyword by creeting a list by appending items to the list and
            # finding the number of items in the list plus one because the list counts ZERO
            if y == -1:
                n_count.append('i') # this is list to add i
            if y == 1:
                p_count.append('j') # this is list to count theh amount of positive streams
            else:
                z_count.append('k')
            #z_zcount = len(z_count)+1
            n_ncount = len(n_count)+1 # count
            p_pcount = len(p_count)+1
            z = (p_pcount*100)/(p_pcount+n_ncount) # I find the percentage of positive keyword pupolarity
            s_2.write(dict(x=x,y=z)) # this writes data to the plotly API for the percentage popularity stream
            #time.sleep(1) #  wait for one second ******************
            return
        except BaseException, e:
            time.sleep(5) # wait for five second
    def on_error(self, status):
        print status # prints the status of the error code
####################################################################################
# main class. this starts plotly and it also triggers the twitter stream
import datetime
print 'Welcome'
time.sleep(5)
search_key = str(raw_input('Search term = ')) # This asks for the search term
stream_id1 = stream_ids[0] # assigns a token
stream_id2 = stream_ids[1] # assigns a token
stream_1 = dict(token=stream_id1, maxpoints=1000) # assigns a token and a maximum plot to a data
stream_2 = dict(token=stream_id2, maxpoints=1000) # assigns a token and a maximum plot to a data
trace1 = go.Scatter(
    x=[],
    y=[],
    stream=stream_1,
    name='trace1'
) # Adds details to the first trace
trace2 = go.Scatter(
    x = [],
    y = [],
    stream= stream_2,
    yaxis='y2',
    name='trace2',
    marker=dict(color='rgb(148, 103,189)') # makes the makers the color purple
)# Adds details to the second trace
data = go.Data([trace1,trace2])
layout = go.Layout(
    autosize=False,
    height=782,
    showlegend=False,
    title=' DA-Popularity trend of '+search_key+' to time',
    width=660,
    xaxis=dict(
        autorange=True,
        title='Time Series',
        type='datetime'
    ),
    yaxis=dict(
        title='Popularity of '+ search_key,
    ), # details for the Y axis on the left hand side
    yaxis2=dict(
        title='Percentage Popularity of '+ search_key+'(%)',
        titlefont=dict(
            color='rgb(148, 103, 189)'  # makes the makers the color purple
        ),
        tickfont=dict(
            color='rgb(148, 103, 189)'  # makes the makers the color purple
        ),
        overlaying='y',
        side='right'
    ) # details for the y axis on the right hand side
)# Adds a layout to the way the graph would be presented.
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='DA-demo-python-streaming')
s_1 = py.Stream(stream_id1) # starts a stream for the first token
s_2 = py.Stream(stream_id2) # starts a stream  for the second token
s_1.open() # open the first stream
s_2.open() # open The Second stream
n_count = [] # universal list to store the negative keyword items
p_count = [] # universal list to store the positve keyword items
z_count = []# universal list to store the neutral keyword items
# Delay start of stream by 5 sec (time to switch tabs)
time.sleep(5)  # waits for five second
twitterStream = Stream(auth, listener())# function to stream tweets
twitterStream.filter(track=[search_key]) # function to stream tweets based on a search term.
s_1.close() # closes the first stream
s_2.close() # closes the second stream
