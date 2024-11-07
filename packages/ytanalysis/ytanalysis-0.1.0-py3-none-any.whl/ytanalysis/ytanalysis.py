import re
import os
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class YTAnalysis:
    
    def __init__(self, channelURL, apikey):
        self.channel_id = channelURL.partition('channel/')[2]
        self.apiKey = apikey
        self.youtube = build('youtube', 'v3', developerKey=self.apiKey)
        self.channel = self.youtube.channels().list(part='snippet,contentDetails,statistics', id=self.channel_id).execute()
        self.channelName = self.channel['items'][0]['snippet']['title']

    def getChannelDetail(self):
        data_dict = {
            "Name": self.channel['items'][0]['snippet']['title'],
            "Subscribers": self.channel['items'][0]['statistics'].get('subscriberCount', "null"),
            "TotalViews": self.channel['items'][0]['statistics']['viewCount'],
            "TotalVideos": self.channel['items'][0]['statistics']['videoCount'],
            "PlaylistId": self.channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        }
        return data_dict

    def getVideoIds(self):
        playlistId = self.channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        video_ids = []
        next_page_token = None

        while True:
            playlist = self.youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlistId,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            video_ids += [item['contentDetails']['videoId'] for item in playlist['items']]
            next_page_token = playlist.get('nextPageToken')

            if next_page_token is None:
                break

        return video_ids

    def getVideoDetail(self):
        videoDetails = []
        videoIds = self.getVideoIds()

        for i in range(0, len(videoIds), 50):
            videoIdReq = self.youtube.videos().list(
                part='snippet,statistics',
                id=','.join(videoIds[i:i+50])
            ).execute()

            for vid in videoIdReq['items']:
                vid_stat = {
                    "Title": vid['snippet']['title'],
                    "Published_date": vid['snippet']['publishedAt'],
                    "Views": int(vid['statistics']['viewCount']),
                    "Likes": int(vid['statistics'].get('likeCount', 0)),
                    "Comments": int(vid['statistics'].get('commentCount', 0))
                }
                videoDetails.append(vid_stat)

        return videoDetails

    def export_csv(self):
        data = self.getVideoDetail()
        dataFrame = pd.DataFrame(data)
        dataFrame['Published_date'] = pd.to_datetime(dataFrame['Published_date']).dt.date
        dataFrame.to_csv(f'{self.channelName}_stats.csv', index=False)

    def plotViews(self, values=10, mostViewed=True, save=False):
        data = self.getVideoDetail()
        dataFrame = pd.DataFrame(data)
        dataFrame['Views'] = pd.to_numeric(dataFrame['Views'])

        order = False if mostViewed else True
        top_videos = dataFrame.sort_values(by='Views', ascending=order).head(values)

        plt.figure(figsize=(10, 8))
        bar = sns.barplot(data=top_videos, x='Views', y='Title')
        plt.title(f'Top {values} {"Most" if mostViewed else "Least"} Viewed Videos')

        if save:
            bar.get_figure().savefig(f'{self.channelName}_most_viewed.png')
        plt.show()

    def plotVideoCount(self, save=False):
        data = self.getVideoDetail()
        dataFrame = pd.DataFrame(data)
        dataFrame['Month'] = pd.to_datetime(dataFrame['Published_date']).dt.strftime('%b')
        
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        dataFrame['Month'] = pd.Categorical(dataFrame['Month'], categories=month_order, ordered=True)
        
        month_counts = dataFrame['Month'].value_counts().reindex(month_order, fillna=0)

        plt.figure(figsize=(10, 6))
        bar = sns.barplot(x=month_counts.index, y=month_counts.values)
        plt.title("Number of Videos Posted Per Month")
        plt.xlabel("Month")
        plt.ylabel("Frequency")

        if save:
            plt.savefig(f'{self.channelName}_videos_per_month.png')
        plt.show()
