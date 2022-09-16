from handle_directory import filtrate_directory
from handle_videos import get_metadata
from upload_video import upload_file
from s3_configs import VIDEOS_EXTENSION, THUMBS_EXTENSION, BUCKET_NAME, FOLDER_NAME
import pandas as pd
import random


def upload_and_gen_dataframe(folder):
    print("main function STARTING")

    # filtrate and return video files in current directory
    videos_list = filtrate_directory(VIDEOS_EXTENSION, THUMBS_EXTENSION, folder)
    print("videos_list: ", videos_list)

    # empty dataframe with column names
    dfToInsert = pd.DataFrame(columns=["datetime", "flag_id", "url_s3", "camera_id", "duration", "video_id"])

    # opens a file, iterate through the videos_list, uploads all video files to aws s3 bucket and generates a dataframe to insert in database
    
    with open('urls_s3.txt', 'w') as f:
        for video in videos_list:
            status, video_url = upload_file(video, BUCKET_NAME, FOLDER_NAME)

            flag_id = random.randint(1, 2) # table in only filled till 2 flag types
            camera_id = random.randint(0, 65535) # from the SQL "capture" table column "camera_id" type
            video_id = str(random.randint(0, 65535)) # from the SQL "capture" table column "video_id" type

            location, datetime, duration = get_metadata(video)

            if (status):
                #print("video.index: ", videos_list.index(video))
                print("values to insert SQL: ", [datetime, flag_id, video_url, camera_id, duration, video_id])
                print("datetime: ", type(datetime))
                print("flag_id: ", type(flag_id))
                print("video_url: ", type(video_url))
                print("camera_id: ", type(camera_id))
                print("duration: ", type(duration))
                print("video_id: ", type(video_id))
                # inserts a new row in the empty dataframe (video index in videos_list is equal to dataframe row index)
                dfToInsert.loc[videos_list.index(video)] = [datetime, flag_id, video_url, camera_id, duration, video_id]

    return dfToInsert

if __name__ == "__name__":

    pass