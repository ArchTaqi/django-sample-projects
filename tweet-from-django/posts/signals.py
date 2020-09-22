import tweepy as tweepy
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post


@receiver(post_save, sender=Post)
def tweet_post(sender, instance, **kwargs):
    twitter_auth_keys = {
        "consumer_key": "API KEY HERE",
        "consumer_secret": "API SECRET KEY",
        "access_token": "ACCESS TOKEN HERE",
        "access_token_secret": "ACCESS TOKEN SECRET KEY HERE"
    }

    auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
    )
    auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
    )
    api = tweepy.API(auth)

    tweet = instance.title + '\n' + Post.get_absolute_url(instance) 
    
    try:
        api.update_status(tweet)
    except tweepy.TweepError as error:
        if error.api_code == 187:
            print('duplicate message')