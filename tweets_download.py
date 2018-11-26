"""path (str): The path to your key file.  The file should
  be in JSON format and look like this (but filled in):
    {
        "consumer_key": "<your Consumer Key here>",
        "consumer_secret":  "<your Consumer Secret here>",
        "access_token": "<your Access Token here>",
        "access_token_secret": "<your Access Token Secret here>"
    }
"""
key_file="" 

trump_tweets = get_tweets_with_cache("realdonaldtrump", key_file)

def load_keys(path):
    import json
    with open(path) as f:
        keys = json.load(f)
    return keys

def download_recent_tweets_by_user(user_account_name, keys):
    import tweepy
    tweets = [t._json for t in tweepy.Cursor(api.user_timeline, id=user_account_name, 
                                             tweet_mode='extended').items()]
    return tweets

def save_tweets(tweets, path):
    import json
    from pathlib import PurePath
    
    # Only accept .json file path
    if PurePath(path).suffix!=".json":
        raise ValueError("Tweets data has to be saved as json file.")
    
    with open(path, "w") as f:        
        json.dump(tweets, f)

def load_tweets(path):
    import json
    from pathlib import PurePath
    
    # Only accept .json file path
    if PurePath(path).suffix!=".json":
        raise ValueError("Tweets data has to be read from a json file.")
        
    with open(path, "r") as f:
        tweets = json.load(f)
    
    return tweets

def get_tweets_with_cache(user_account_name, keys_path):
    from pathlib import Path
    
    # read keys as a dictionary
    keys=load_keys(keys_path)

    file_path="{}_recent_tweets.json".format(user_account_name)
    
    # check if file exists
    if not Path(file_path).is_file():
        # get tweets as a list of dictionaries
        tweets=download_recent_tweets_by_user(user_account_name, keys)
        save_tweets(tweets, file_path)
    
    return load_tweets(file_path)