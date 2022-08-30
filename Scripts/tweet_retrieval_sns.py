import pandas as pd
import tweepy as tw
import snscrape.modules.twitter as sntwitter
import datetime


for i in range(1):

    print("Iteration No.: " + str(i) + "\n")
    tweets_df = pd.DataFrame(columns=['user_name','user_location','text','likes', 'date'])

    try:
        tweets_df = pd.read_csv('tweets_sns.csv')
    except:
        pass

    regions_df = pd.read_csv('regions_sns.csv')
    
    my_api_key = "Mo8qVCy7ItfRJgVBNtyCWAMb2"
    my_api_secret = "vL4KWpZGfQ0eUi4XbEAHInVLRXSE66M8hnqpxDehyAVe87P4fe"

    auth = tw.OAuthHandler(my_api_key, my_api_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    search_query = "Vodafone OR Orange OR Etisalat OR WE OR فودافون OR موبينيل OR اتصالات"

    if 'date' not in regions_df.columns:
        regions_df['date'] = str(datetime.datetime.now())[:10]

    max_tweets = 100
    max_date  = "2022-01-01"

    latitude_ind = regions_df.columns.get_loc("latitude")
    longitude_ind = regions_df.columns.get_loc("longitude")
    radius_ind = regions_df.columns.get_loc("radius")
    date_ind = regions_df.columns.get_loc("date")

    for ind, region in enumerate(regions_df['name'].unique()):
        
        print(region + ":")

        if regions_df.iloc[ind, date_ind] < max_date:
            print("limit reached for this region")
            continue

        latitude = regions_df.iloc[ind, latitude_ind]
        longitude = regions_df.iloc[ind, longitude_ind]
        radius = regions_df.iloc[ind, radius_ind]
        last_date = regions_df.iloc[ind, date_ind]

        geocode = str(latitude)+","+str(longitude)+","+str(radius)+"km"

        tweet_count = 0

        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(\
            'q:{} until:{} geocode:{} lang:ar -filter:links -filter:replies -filter:retweets'.\
            format(search_query, last_date, geocode)).get_items()):

            if i >= max_tweets :
                break

            full_text = tweet.content
            try:
                status = api.get_status(tweet.id, tweet_mode = "extended")
                full_text = status.full_text
            except:
                print("failed to retrieve full text of tweet id: " + tweet.id)
                pass

            row = {
                'user_name': tweet.user.username, 
                'user_location': region,
                'text': full_text,
                'likes': tweet.likeCount,
                'date': str(tweet.date)[0:10]
            }

            row2df = pd.DataFrame.from_records([row])
            tweets_df = pd.concat([tweets_df, row2df], ignore_index=True, axis=0)

            tweet_count+=1
        
        if tweet_count==0:
            print("No more tweets to retrieve in this region")
            continue

        tweets_df.to_csv('tweets_sns.csv', index=False)
        regions_df.to_csv('regions_sns.csv', index=False)
        print(str(tweet_count)+" tweets from " + region + " have been retrieved successfully\n")