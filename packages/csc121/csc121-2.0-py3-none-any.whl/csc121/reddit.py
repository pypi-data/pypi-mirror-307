"""
This module contains various utility functions for interfacing with the Reddit API.

Author: Raghuram Ramanujan
"""

import praw, prawcore
import json
from ratelimit import limits, sleep_and_retry
from pkg_resources import resource_filename


@sleep_and_retry
@limits(calls=5, period=60)
def get_reddit_comments(subreddit_name):
    """ Returns the 20 most recent comments from a given Subreddit

    Args:
        subreddit_name - the Subreddit page to query

    Returns:
        A JSON object (i.e., a nested structure composed of lists and
        dictionaries) containing the response from Reddit
    """
    # Reddit app credentials
    client_id = "ZK5nGAvO_iZ-OYBMLheBaw"
    client_secret = "4A1ChQTeNOJUifF7cIpmDQ3Lsex8ZQ"
    user_agent = "HW7"
    comment_limit = 20

    # Set up API connection
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    subreddit = reddit.subreddit(subreddit_name)

    # setting up a more elaborate JSON structure to make students work to extract
    # the actual data
    comments = [{"search_metadata": {
        "completed_in": 0.097,
        "count": f"{comment_limit}",
        "max_id": 580546531234869250,
        "max_id_str": "580546531234869250",
        "since_id": 0,
        "since_id_str": "0",
        "subreddit": str(subreddit),
    }}, {"results": []}]

    try:
        for comment in subreddit.comments(limit=comment_limit):
            # cook up a more complicated JSON structure so students have
            # to do some work to unpack the data
            comment_entry = {
                        "comment_data": {
                            "id": comment.id,
                            "attributes": {
                                "body": comment.body,
                                "author": str(comment.author),
                                "created_utc": comment.created_utc,
                            },
                            "links": {
                                "permalink": comment.permalink
                            }
                        }
                    }
            comments[1]['results'].append(comment_entry)
    except prawcore.exceptions.Redirect:  # return empty list if given bogus subreddit
        pass
    
    return comments


def get_cached_comments():
    """
    Returns a cached set of Reddit comments in JSON format for testing purposes
    """
    cached_comments_filepath = resource_filename(__name__, 'cached_comments.txt')
    with open(cached_comments_filepath, "r") as in_file:
        return eval(in_file.read())



def pretty_print(data):
    """ Pretty prints a JSON object

    Args:
        data - the JSON object to print

    Returns:
        None
    """
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))