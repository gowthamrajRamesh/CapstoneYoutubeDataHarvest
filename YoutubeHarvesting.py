from googleapiclient.discovery import build
import pandas as pd
import  streamlit as st 
import YoutubeHarvestingAPIFunc as YTAPI
import re
import sys



# for DB
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import sqlalchemy



st.title(':red[Youtube Data Harvesting] ')
channel_id= st.text_input('Enter a Youtube Channel ID below')

#channel_info= []
onclick = st.button ('Get Details and Store',key='channels_button')
if onclick or st.session_state.channels_button:
    channel_info=(YTAPI.get_channel_details(channel_id))
    #channel_name = channel_info['channel_name']
    st.write('Channel Name: ' ,channel_info['channel_name'][0])
    st.write('Total no of Views: ',channel_info['view_count'][0])
    st.write('Channel subscribers: ',channel_info['subscriber_count'][0])
    st.write('Total no of video: ',channel_info['Total_videos'][0])
    
    # creating MySQL DB engine
    def MySQLdbConnection(host_name,user_name, password):
        
        try:
            connection = mysql.connector.connect(
                        host=host_name,
                        user=user_name,
                        password=password   
                    )
            print('MysqlDB connection created Successfully')
            
        except Error as e:
            print(f'The error {e} occurred')
        return connection



    try:
        connection = MySQLdbConnection('localhost','root','12345678')
        cursor = connection.cursor()
        DB_query = 'create database if not exists capstone_youtube'
        cursor.execute(DB_query)
        print('DB capstone_youtube created')
        query = 'use capstone_youtube'
        cursor.execute(query)
        print('started using db capstone_youtube')
    except Error as e:
            print(f'The error {e} occured')


    # creating necessary tables in Mysql----------------------------------------------------------------
    # Creating channels Table
    channel_table_creation_query = '''create table if not exists channels (
                                        channel_id varchar(200) ,
                                        channel_name varchar(250),
                                        channel_description varchar(500),
                                        view_count int,
                                        subscriber_count int,
                                        Total_videos int,
                                        PRIMARY KEY (channel_id)
                                        )'''
    cursor.execute(channel_table_creation_query)

    # playlist table

    playlist_creation_query ='''create table if not exists playlists (
                                Channel_id varchar(200),
                                playlist_id varchar(250),
                                playlist_name varchar(200),
                                playlist_videos_cnt int,
                                PRIMARY KEY (playlist_id)
                                )'''

    cursor.execute(playlist_creation_query)

    # Playlist Items Table
    playlistItem_creation_query = '''create table if not exists playlist_items (
                                    channel_id varchar(200),
                                    playlist_id varchar(250),
                                    video_id varchar(200),
                                    video_title varchar(250),
                                    UNIQUE (video_id)
                                    )'''
    cursor.execute(playlistItem_creation_query)

    #  videos table
    videos_details_table_query = '''create table if not exists videos_details (
                                video_id varchar(200),
                                channel_id varchar(200),
                                video_name varchar(500),
                                video_published_At varchar(200),
                                duration varchar(100),
                                viewcount int,
                                likecount int,
                                favoriteCount int,
                                commentCount int,
                                PRIMARY KEY (video_id)
                                )'''
    cursor.execute(videos_details_table_query)

    # Comments table
    comments_table_query = '''create table if not exists comments (
                            commentsThreads_id varchar(200),
                            channel_id varchar(200),
                            video_id varchar(200),
                            likeCount int,
                            totalreplycount int,
                            PRIMARY KEY (commentsThreads_id)
                            )'''
    cursor.execute(comments_table_query)
    print('all requried tables created in MYSQL')


    

    #-------------------------------------------------------------------------------------------------
    # --------Storing data into Mysql
    #channels loop
    if len(channel_id)!=0:
    #for channels in channel_id:
        try:
            channel_info=(YTAPI.get_channel_details(channel_id))
        except Exception as e:
            st.write(e)
            sys.exit(1)
        #insert query on channels
        channel_insert_query = f"insert ignore into channels values(%s,%s,%s,%s,%s,%s)  " 
        data =[]
        for index in channel_info.index:
            row = channel_info.loc[index].values
            row =(str(row[0]),str(row[1]),str(row[2]),int(row[3]),int(row[4]),int(row[5]))
            data.append(row)
        cursor.executemany(channel_insert_query,data)
        connection.commit()
        
        # playlist 
        try:
            playlistinfo_df=YTAPI.get_playlist(channel_id)
        except Exception as e:
            st.write(e)
            sys.exit(1)
        playlist_insert_query = f"insert ignore into playlists values(%s,%s,%s,%s)  " 
        data =[]
        for index in playlistinfo_df.index:
            row = playlistinfo_df.loc[index].values
            row =(str(row[0]),str(row[1]),str(row[2]),int(row[3]))
            data.append(row)
        cursor.executemany(playlist_insert_query,data)
        connection.commit()
        
        # playlist items
        for playlist in playlistinfo_df['playlist_id']:
            try:
                playlistItems_df= YTAPI.get_playListItems(playlist)
            except Exception as e:
                st.write(e)
                break
            if playlistItems_df.empty:
                continue
            else:
                playlistitems_insert_query = f"insert ignore into playlist_items values(%s,%s,%s,%s)  " 
                data =[]
                for index in playlistItems_df.index:
                    row = playlistItems_df.loc[index].values
                    row =(str(row[0]),str(row[1]),str(row[2]),str(row[3]))
                    data.append(row)
                cursor.executemany(playlistitems_insert_query,data)
                connection.commit()
                
                #videos 
                for videos in playlistItems_df['video_id']:
                    try:
                        videoList_df=(YTAPI.get_videos_details(videos))
                    except Exception as e:
                        st.write(e)
                        break
                    if videoList_df.empty:
                        continue
                    else:
                        videoslist_insert_query = f"insert ignore into videos_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s)  " 
                        data =[]
                        for index in videoList_df.index:
                            row = videoList_df.loc[index].values
                            row =(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),int(row[5]),int(row[6]),int(row[7]),int(row[8]))
                            data.append(row)
                        cursor.executemany(videoslist_insert_query,data)
                        connection.commit()

    st.subheader(':green[Data insertion completed, start your analysis]')

st.header(':blue[Data Analysis]')
start_analysis=st.checkbox('Select the checkbox to start the analysis',key='analysis_checkbox')

if start_analysis:
    st.write('(Note: This Zone analyze the collection of data collected from the channels, each question gives data in table format)')
    questions = st.radio(':red[Analysis Questions]',
                         ['1.What are the names of all the videos and their corresponding channels?',
                           '2.Which channels have the most number of videos, and how many videos do they have?',
                           '3.What are the top 10 most viewed videos and their respective channels?',
                            '4.How many comments were made on each video, and what are their corresponding video names?',
                            '5.Which videos have the highest number of likes, and what are their corresponding channel names?',
                            '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                            '7.What is the total number of views for each channel, and what are their corresponding channel names?',
                            '8.What are the names of all the channels that have published videos in the year 2022?',
                            '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                            '10.Which videos have the highest number of comments, and what are their corresponding channel names?'    
                         ],index=None,
                         key='questions_list'
                         )
    #creating DB engine to run sql queries
    engine = create_engine('mysql+mysqlconnector://root:12345678@localhost/capstone_youtube')

    # showing results based on questions selected
    #Q1
    if questions=='1.What are the names of all the videos and their corresponding channels?':
        df = pd.read_sql('select pis.video_title as Videos,c.channel_name as channels  from playlist_items pis left join channels c on c.channel_id=pis.channel_id',engine)
        #df = pd.DataFrame(df,columns=['Video','Channel'])
        st.dataframe(df)
    #Q2
    elif questions=='2.Which channels have the most number of videos, and how many videos do they have?':
        df= pd.read_sql('select channel_name as channel,total_videos from channels order by total_videos desc',engine)
        #df = pd.DataFrame(df,columns=['channel','number of videos'])
        st.dataframe(df,column_config={'channel':'channel','total_videos': 'No of Videos'})
    #Q3
    elif questions=='3.What are the top 10 most viewed videos and their respective channels?':
        df= pd.read_sql('select  c.channel_name, vd.video_name from videos_details vd left join channels c on c.channel_id = vd.channel_id order by vd.viewcount desc limit 10'
                            ,engine)
        #df = pd.DataFrame(df,columns=['Channel','Top 10 Videos'])
        st.dataframe(df,column_config={'channel_name':'channels',
                                            'video_name':'Top 10 Videos'
                                            })
    
    #Q4
    elif questions=='4.How many comments were made on each video, and what are their corresponding video names?':
        df= pd.read_sql('''select video_name,commentCount from videos_details'''
                            ,engine)
        #df = pd.DataFrame(df,columns=['video','Comments Count'])
        st.dataframe(df,column_config={'video_name':'Video',
                                            'commentCount':'Comment Count'
                                            })
    
    #Q5
    elif questions=='5.Which videos have the highest number of likes, and what are their corresponding channel names?':
        df= pd.read_sql('''select  c.channel_name,vd.video_name,vd.likecount 
                            from videos_details vd left join channels c on c.channel_id=vd.channel_id 
                            order by vd.likecount desc'''
                            ,engine)
        #df = pd.DataFrame(df,columns=['Channels','Videos','Like Count'])
        st.dataframe(df,column_config={'channel_name':'Channels',
                                        'video_name':'Videos',
                                        'likecount':'Likes'
                                            })
    
    #Q6
    elif questions=='6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        df= pd.read_sql('''select video_name,likecount from videos_details'''
                            ,engine)
        #df = pd.DataFrame(df,columns=['Videos','Like Count'])
        st.dataframe(df,column_config={
                                        'video_name':'Videos',
                                        'likecount':'Likes'
                                            })
    
    #Q7
    elif questions=='7.What is the total number of views for each channel, and what are their corresponding channel names?':
        df= pd.read_sql('''select channel_name,view_count from channels'''
                            ,engine)
        #df = pd.DataFrame(df,columns=['Channels','No of Views'])
        st.dataframe(df,column_config={'channel_name': 'Channels',
                                        
                                        'view_count':'Views'
                                            })
    
    #Q8
    elif questions=='8.What are the names of all the channels that have published videos in the year 2022?':
        df= pd.read_sql("select distinct c.channel_name from videos_details vd join channels c on c.channel_id=vd.channel_id where extract(YEAR from vd.video_published_At)=2022"
                            ,engine)
        st.dataframe(df,column_config={'channel_name': 'Channels'
                                            })

    #Q9
    elif questions=='9.What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        df= pd.read_sql("select c.channel_name,vd.video_name, SEC_TO_TIME(AVG(TIME_TO_SEC(vd.duration))) as Avg_Duration from videos_details vd join channels c on c.channel_id=vd.channel_id group by c.channel_name,vd.video_name"
                            ,engine)
        
        st.dataframe(df,column_config={'channel_name': 'Channels',
                                        'video_name': 'Videos',
                                        'Avg_Duration':'Average Duration'
                                            })
    
    #Q10
    elif questions=='10.Which videos have the highest number of comments, and what are their corresponding channel names?':
        df= pd.read_sql('select c.channel_name,vd.video_name,vd.commentCount from videos_details vd join channels c on c.channel_id=vd.channel_id order by vd.commentCount desc'
                            ,engine)
        #df = pd.DataFrame(df,columns=['video Name','Channel','No of comments'])
        st.dataframe(df,column_config={'channel_name': 'Channels',
                                        'video_name': 'Videos',
                                        'commentCount':'No of comments'
                                            })