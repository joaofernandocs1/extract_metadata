import os 
import glob
from datetime import datetime
from upload_video import upload_file


def rename_videos_and_upload(root_path, video_to_rename, msc_block, msc_pos):

    # videos_to_rename[0] = ["absolute path"]
    print("videos to rename: ", video_to_rename)

    msc_pos -= 1

    #print("msc block: ", msc_block)
    #print("msc block shape: ", msc_block.shape)
    #print("mscpos: ", msc_pos)

    msc_block = msc_block.iloc[msc_pos] # recorta a linha de index msc_pos e transforma em uma coluna
    #print("msc block [0] (data): ", msc_block[0]) # primeira linha da coluna (data)
    #print("msc block [1] (duracao): ", msc_block[1]) # segunda linha da coluna (duracao)
    duracao_video = str(msc_block[1])
    duracao_video = duracao_video[0:2] + "_" + duracao_video[3:5]
    #print("duracao video: ", duracao_video)
    #print("msc block [2] (PDV): ", msc_block[2]) # terceira linha da coluna (nome do PDV)
    nome_pdv = str(msc_block[2])
    nome_pdv = nome_pdv.replace(" ", "_")
    #print("nome pdv: ", nome_pdv)
    #print("type msc block: ", type(msc_block))
    #print("msc block sliced shape: ", msc_block.shape)

    complete_datetime = datetime.fromisoformat(msc_block[0])
    full_path_videoname = video_to_rename[0]
    print("full path video to rename: ", full_path_videoname)
    #print("complete datetime: ", complete_datetime)

    new_video_name = str(complete_datetime.day) + str(complete_datetime.month) + str(complete_datetime.year) + "_" + str(complete_datetime.hour) + str(complete_datetime.minute) + str(complete_datetime.second) + "_" + str(complete_datetime.microsecond) + "_" + duracao_video + "_" + nome_pdv + ".mp4"
    # data completa + duracao + location_name + extensao (mp4)
    print("new video name: ", new_video_name)
    rename_command = "rename {0} {1}".format(full_path_videoname, new_video_name)
    print("rename command: ", rename_command)
    os.system(rename_command)
    # os.system("rename videos\{0} {1}".format(video, new_video_name)) # caso abspath nao seja necessario

    new_full_path_videoname = root_path + str(r"\video")
    new_full_path_videoname = "{0}\{1}".format(new_full_path_videoname, new_video_name)
    print("new full path videoname: ", new_full_path_videoname)
    
    try:
        response_s3, url = upload_file(new_full_path_videoname, "flagged-videos", "videos")
        print("pulando upload")
        #if (response_s3):
        #    print("video inserido no S3: ", response_s3)
    except Exception as error_up:
        print("upload failed", error_up)
        response_s3 = False

    if (response_s3):
        print("deletando video... ")
        command = "del {0}".format(new_full_path_videoname)
        os.system(command)

    return duracao_video, complete_datetime, nome_pdv, new_full_path_videoname, url


def check_videos_to_rename(videos_path, videos_extension):

    full_path = videos_path + str(r"\*.{0}".format(videos_extension))

    downloaded_videos_list = glob.glob(full_path, recursive=True)
    #downloaded_videos_list = glob.glob('*.mp4', recursive=True)
    #print("downloaded_videos_list: ", downloaded_videos_list)

    return downloaded_videos_list


def order_by_created_time(videos_list):

    # videos_list = lista com nomes antigos da intelbras a serem renomeados

    paths_list = [] # absolute path de cada video
    # paths_list = videos_list # caso abspath nao seja necessario
    ctimes_list = [] # instante em que o video foi criado

    for video in videos_list:
        paths_list.append(os.path.abspath(video)) # talvez nao seja necessario pegar o abspath, so o nome ja baste porque vem com "videos\" antes do nome
        ctimes_list.append(os.path.getctime(os.path.abspath(video)))

    zip_iterator = zip(paths_list, ctimes_list)
    dir_dict = dict(zip_iterator) # {"absolute path": instante de criacao, ...}

    # ordena os videos pelos instantes de criacao (values do dicionario)
    ord_dict = sorted(dir_dict.items(), key=lambda x: x[1]) # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    print("Ordered by ctime: ", ord_dict)

    return ord_dict


if __name__ == '__main__':

    pass
