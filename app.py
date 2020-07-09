from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse
import tweepy
from textblob import TextBlob
import re

app=Flask(__name__)
api=Api(app)

consumer_key = '5eq6TRJgT8yGDAf4ZTn3mpnq4'
consumer_secret= 'gl4ZmDVdPKNryE53EI5j5iZkyBOeyfZ0SpTBJD2FyJHylADRDS'

access_token= '1168836138225885184-mqWMfHrnsH4wHwoUk3TYlEHMtoEbFq'
access_token_secret = 'Iw4YAFO7gEPXtwxDWjrMQqbp7HA1t8boOlXVeZXwXN2y5'

auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api2=tweepy.API(auth)

class sentiment(Resource):
   
    
    def get(self,topic):
        
        positivey="positive%:"
        polarity=getPolarity(topic)
        result={ "polarity": polarity }

        return result ,200



def getPolarity(topic):
    public_tweet=api2.search(q=topic,count=50)
    max=len(public_tweet)
    
    sum=0
    polarity="Positive"

    for tweet in public_tweet:
        text=tweet.text
        textWords=text.split()
        #print (textWords)
        Tweet=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", text).split())
        #print(Tweet)
        analysis=TextBlob(Tweet)
        sum=sum+analysis.polarity

    avg_polarity=sum/max

    if (avg_polarity<0):
        polarity="Negative"
        
    elif(0<=avg_polarity<=0.15):
        polarity="Neutral"
        
    else:
        polarity="Positive"
        
    
    return polarity
    

    #return jsonify( {"positive(%):"  },
           ##         {"neutral(%):"  },
             #       {"negative(%):"  } )


api.add_resource(sentiment,"/<string:topic>")

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True) 