
"""
This module contains various utility functions for interfacing with the
Twitter API.

Author: Raghuram Ramanujan
"""
import json
import requests
from pkg_resources import resource_filename


def get_tweets(query_term):
    """Returns search results from Twitter for the supplied query

    Args:
        query_term - the search term to send to Twitter's API (a string)

    Returns:
        A JSON object (i.e., a nested structure composed of lists and
        dictionaries) containing the response from Twitter
    """
    # authentication token for talking to Twitter
    BEARER_TOKEN = ("AAAAAAAAAAAAAAAAAAAAAHgJUAAAAAAAaVEOLsaEBot1M5rTmH4tcOn"
                    "65Xs%3D1FFj0BgMfc153PjusP4R0V0Z9ECdW3S6bkqtAJqAwE")

    # The Twitter search URL
    BASE_URL = "https://api.twitter.com/1.1/search/tweets.json"

    # search parameters
    params = {"q": query_term, "include_entities": "false", "count": 100}

    # HTTP headers for authentication
    headers = {"User-Agent": "HW7",
               "Authorization": "Bearer {}".format(BEARER_TOKEN)}

    # make the request and return the results
    return requests.get(BASE_URL, params=params, headers=headers).json()


def get_cached_tweets():
    """
    Returns a cached set of tweets in JSON format for testing purposes
    """
    # File below contains twenty tweets mentioning Steph Curry that were
    # retrieved on 03/24/2015.
    cached_tweets_filepath = resource_filename(__name__, 'cached_tweets.txt')
    with open(cached_tweets_filepath, "r") as in_file:
        return eval(in_file.read())


def pretty_print(data):
    """
    Pretty prints a JSON object
    """
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
