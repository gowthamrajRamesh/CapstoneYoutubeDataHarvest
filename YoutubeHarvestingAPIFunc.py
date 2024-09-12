# for Google API
from googleapiclient.discovery import build
import pandas as pd
import  streamlit as st 
import re
import sys

# for DB 
import mysql.connector
from mysql.connector import Error

#----------------------------------Starting line of code---------------------------------------------------------------------
# channels details mining

#channel_id = ['UCcZo9VRa3TFIJaf1aJOLDgw']#,'UCY6KjrDBN_tIRFT_QNqQbRQ']#,'UC5cY198GU1MQMIPJgMkCJ_Q','UC5EQWvy59VeHPJz8mDALPxg']  # example channel_ID
 
def get_channel_details(channel_id):
    #initialization
    api_key = 'AIzaSyBtgFVn0wVVI760A2njO77xJHyfsGHpfgo'
    youtube = build("youtube", "v3", developerKey=api_key)
    channels_list=[]
    nextPageToken = None
    # Channel Data collecting
    while 1:
        #API Request
        request = youtube.channels().list(
            
            id=channel_id,
            part='snippet,statistics,contentDetails',
            maxResults=50,
            pageToken=nextPageToken
        )
        channel_response = request.execute()
        # collecting required API Data
        for items in channel_response['items']:
            channels= {'channel_id':items['id'],
                                'channel_name':items['snippet']['title'],
                                'channel_description':items['snippet']['description'],
                                #'playlist_id':items['contentDetails']['relatedPlaylists']['uploads'],
                                'view_count':int(items['statistics']['viewCount']),
                                'subscriber_count':int(items['statistics']['subscriberCount']),
                                'Total_videos':int(items['statistics']['videoCount'])
                               }
            
            channels_list.append(channels)
        nextPageToken  = channel_response.get('nextPageToken')
        
        if nextPageToken is None:
            break
            
    return pd.DataFrame(channels_list)

#for channels in channel_id:
 #   channel_info=(get_channel_details(channels))
#channel_info

#playlist details
def get_playlist(channel_id):
    #initialization
    playlists =[]
    nextPageToken = None
    api_key = 'AIzaSyBtgFVn0wVVI760A2njO77xJHyfsGHpfgo'
    youtube = build("youtube", "v3", developerKey=api_key)

    while 1:
    #API request
        request = youtube.playlists().list(
                part="snippet,contentDetails",
                channelId=channel_id,
                maxResults=50,
                pageToken=nextPageToken
            )
        playlist_response = request.execute()

    #playlist mining stage 1
        for items in playlist_response['items']:
            playlists_data ={'Channel_id':items['snippet']['channelId'],
                             'playlist_id':items['id'],
                             'playlist_name': items['snippet']['title'],
                             'playlist_videos_cnt': int(items['contentDetails']['itemCount'])
                             }    
            playlists.append(playlists_data)
        
        nextPageToken = playlist_response.get('nextPageToken')

        if nextPageToken is None:
            break
         
    return pd.DataFrame(playlists)

#playlist Items
def get_playListItems(playlistId):
    #initialization
    playlistItems =[]
    api_key = 'AIzaSyBtgFVn0wVVI760A2njO77xJHyfsGHpfgo'
    youtube = build("youtube", "v3", developerKey=api_key)
    nextPageTocken = None

    while 1:
    #API request for playlistItems
        request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                maxResults=50,
                playlistId=playlistId,
                pageToken=nextPageTocken
            )
        playListResponse= request.execute()
    
        #playListItem Mining
        for items in playListResponse['items']:
            playlistItems_data ={ 'channel_id':items['snippet']['channelId'],
                                  'playlist_id':items['snippet']['playlistId'],
                                  'video_id': items['snippet']['resourceId']['videoId'],
                                  'video_title':items['snippet']['title']
                                }
            playlistItems.append(playlistItems_data)
        nextPageTocken = playListResponse.get('nextPageToken')

        if not nextPageTocken:
            break
    
    return pd.DataFrame(playlistItems)

def convert_duration(duration):
            regex = r'PT(\d+H)?(\d+M)?(\d+S)?'
            match = re.match(regex, duration)
            if not match:
                return '00:00:00'
            hours, minutes, seconds = match.groups()
            hours = int(hours[:-1]) if hours else 0
            minutes = int(minutes[:-1]) if minutes else 0
            seconds = int(seconds[:-1]) if seconds else 0
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return '{:02d}:{:02d}:{:02d}'.format(int(total_seconds / 3600), int((total_seconds % 3600) / 60), int(total_seconds % 60))


# videos function
def get_videos_details(video_id):
    #initialization
    videos =[]
    api_key = 'AIzaSyBtgFVn0wVVI760A2njO77xJHyfsGHpfgo'
    youtube = build("youtube", "v3", developerKey=api_key)
    nextPageToken = None

    while 1:
    #API request for viedo
        try:
            request = youtube.videos().list(
                        part="snippet,contentDetails,statistics",
                        maxResults=50,
                        id=video_id,
                        pageToken=nextPageToken
                    )
            videoListResponse= request.execute()
        except:
            st.write('your quota limit exhausted, please try again tomorrow')
            #videos Mining
        for items in videoListResponse['items']:
            videos_data ={'video_id': items['id'],
                            'channel_id':items['snippet']['channelId'],
                            'video_name':items['snippet']['title'],
                            'video_published_at':items['snippet']['publishedAt'],
                            #'video_description':items['snippet']['description'],
                            'duration':convert_duration(items['contentDetails']['duration']),
                            #'contentRating': items['contentDetails']['contentRating'],
                            'viewcount': int(items['statistics']['viewCount']) if 'viewCount' in items['statistics'] else 0,
                            'likecount':int(items['statistics']['likeCount']) if 'likeCount' in items['statistics'] else 0,
                            'favoriteCount':int(items['statistics']['favoriteCount']) if 'favoriteCount' in items['statistics'] else 0,
                            'commentCount':int(items['statistics']['commentCount']) if 'commentCount' in items['statistics'] else 0
                                }
            videos.append(videos_data)
                
        nextPageToken = videoListResponse.get('nextPageToken')

        if nextPageToken is None:
            break
        
    
    return pd.DataFrame(videos)
