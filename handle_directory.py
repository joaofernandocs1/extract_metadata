import os
import glob
import subprocess


def get_created_paths(mibo_path):

    # mibo_path:      /mnt/sdcard/MiboCam
    # mibo_sess_path: /mnt/sdcard/MiboCam/123456789
    # mibo_tmp_path:  /mnt/sdcard/MiboCam/123456789/videoDownloadTmp
    # mibo_vid_path:  /mnt/sdcard/MiboCam/123456789/video


    out = subprocess.check_output("adb shell ls {}".format(mibo_path), shell=True, text=True)
    out = out.split('\n')

    sess_path = mibo_path + "/" + str(out[0]) # session path
    print("mibo_sess_path: ", sess_path)

    tmp_path = sess_path + "/videoDownloadTmp" # session tmp path
    print("mibo_tmp_path: ", tmp_path)
    
    vid_path = sess_path + "/video" # session videos path
    print("mibo_vid_path: ", vid_path)

    return sess_path, tmp_path, vid_path


def clean_all_dirs(mibo_sess_path, mibo_vid_path, mibo_tmp_path, path_to, videos_ext, thumbs_ext):

    # limpa diretorio /video local
    complete_path = path_to + str(r"\video")
    print("complete path: ", complete_path)

    videos_files_list = glob.glob("{0}/*.{1}".format(complete_path, videos_ext), recursive=True)
    thumbs_files_list = glob.glob("{0}/*.{1}".format(complete_path, thumbs_ext), recursive=True)
    print("old videos files list to remove: ", videos_files_list)
    print("old thumbs files list to remove: ", thumbs_files_list)

    if (len(videos_files_list) > 0):
        for video in videos_files_list:

            del_command = "del {0}".format(video)
            print(del_command)
            os.system(del_command)

    if (len(thumbs_files_list) > 0):
        for thumb in thumbs_files_list:

            del_command = "del {0}".format(thumb)
            print(del_command)
            os.system(del_command)

    # limpa o diretorio mibo_vid_path do emulador 
    try:
        command = "adb shell rm {0}/*".format(mibo_vid_path)
        print(command)
        #os.system(command)
        out_vid = subprocess.check_output(command, shell=True, text=True)
        #print("out_tmp: ", out_vid) # comando adb shell rm nao tem saida
        print("mibo_vid_path cleaned")

    except subprocess.CalledProcessError as error_open_vids:
        print("Error removing mibo_vid_path content: ", error_open_vids.output)
        # pode estar vazio ou pode nao ter sido criado ainda (CORRIGIR)
        print("mibo_vid_path already empty")
        # command = "adb shell mkdir {0}".format(mibo_tmp_path)
        # print(command)
        # os.system(command)
    except Exception as error_vids:
        print("Unknown error: ", error_vids)

    # listar os diretos em mibo_sess_path
    out = subprocess.check_output("adb shell ls {}".format(mibo_sess_path), shell=True, text=True)
    out = out.split('\n')
    #out.pop()

    # checar se diretorio mibo_tmp_path ja foi criado
    for dir in out:
        if (dir == "videoDownloadTmp"):
            tmp_path = True
            break
        else:
            tmp_path = False

    # se nao foi criado, cria
    if (not tmp_path):
        print("mibo_tmp_path not created. Creating... ")
        command = "adb shell mkdir {0}".format(mibo_tmp_path)
        print(command)
        os.system(command)
    # se ja foi criado, apenas limpa
    elif(tmp_path):
        print("mibo_tmp_path already exists")

        try:
            command = "adb shell rm {0}/*".format(mibo_tmp_path)
            print(command)
            #os.system(command)
            out_tmp = subprocess.check_output(command, shell=True, text=True)
            print("out_tmp: ", out_tmp) # comando adb shell rm nao tem saida

        except subprocess.CalledProcessError as error_open_tmp:
            print("Error removing mibo_tmp_path content: ", error_open_tmp.output)
            # pode estar vazio ou pode nao ter sido criado ainda (CORRIGIR)
            print("mibo_tmp_path already empty")
            # command = "adb shell mkdir {0}".format(mibo_tmp_path)
            # print(command)
            # os.system(command)
        except Exception as error_tmp:
            print("Unknown error: ", error_tmp)
 
    return True


def check_downloaded(mibo_vid_path, mibo_tmp_path):

    count_vid = 0
    count_thb = 0
    count_tmp_vid = 0
    count_tmp_thb = 0
    downloaded = False

    # adb shell ls /mnt/sdcard/MiboCam/10020171/video
    #os.chdir(str(r"C:\Users\João Fernando\Documents\Roda\git_acoes_suspeitas\acoes_suspeitas\v_acoes_susp\manage_videos\video"))
    #cwd = os.getcwd() 
    #print("Current local working directory is:", cwd)
    # lista conteudo do diretorio de videos baixados no dispositivo Android
    out = subprocess.check_output("adb shell ls {}".format(mibo_vid_path), shell=True, text=True)
    out = out.split('\n')
    out.pop()
    #print(out)

    # 2a estrategia: lista diretorio de videos baixados e checar se diretorio de videos sendo baixados esta vazio

    for file in out:
        if (file.endswith(".mp4")):
            count_vid += 1
        elif(file.endswith(".jpg")):
            count_thb += 1

    # lista conteudo do diretorio de videos sendo baixados (diretorio de arquivos de video temporarios) no dispositivo Android
    try:
        out_tmp = subprocess.check_output("adb shell ls {}".format(mibo_tmp_path), shell=True, text=True)
        out_tmp = out_tmp.split('\n')
        out_tmp.pop()
        #print(out_tmp)

    except subprocess.CalledProcessError as error_open_tmp:
        print("Error opening video tmp: ", error_open_tmp.output)
        print("video tmp path doesnt exist. Will create...")
        command = "adb shell mkdir {0}".format(mibo_tmp_path)
        print(command)
        os.system(command)
        out_tmp = []

    for file in out_tmp:
        if (file.endswith(".mp4")):
            count_tmp_vid += 1
        elif(file.endswith(".jpg")):
            count_tmp_thb += 1

    # print("count_vid: ", count_vid, "count_thb: ", count_thb, "count_tmp_vid: ", count_tmp_vid, "count_tmp_thb: ", count_tmp_thb)

    if (count_vid == 1 and count_thb == 1 and count_tmp_vid == 0 and count_tmp_thb == 0): # corresponde ao diretorio de temporario vazio e o diretorio /video preenchido
        message = "Download concluido"
        #print(message)
        downloaded = True
    else:
        message = "Download nao concluido"
        #print(message)
        downloaded = False

    # 1a estrategia: contar arquivos no diretorio de videos baixados

    # apenas um arquivo, a thumb
    #if (len(out) == 1):
    #    print("thumb downloaded")
    #    message = "NOT OK"
    #    downloaded = False
    # 2 arquivos ou numero de arquivos multiplo de 2
    #elif (len(out) == 0):
    #    print("empty directory")
    #    message = "NOT OK"
    #    downloaded = False
    # ja tem um numero par de videos e de thumbs e outro video esta sendo baixado
    #elif (len(out) == 2):
    #    print("download finished")
    #    message = "OK"
    #    downloaded = True

    return message, downloaded


def pull_and_remove_from_emulator(path_from, path_to): # 515

    # PARAMS: 
    #
    # path_from: "/mnt/sdcard/MiboCam/4149925/video/" (EXAMPLE)
    #            path completo da pasta do emulador para baixar videos
    #
    # path_to:   "C:\Users\joaofernando\Documents\Roda\git_acoes_suspeitas\acoes_suspeitas\v_acoes_susp\manage_videos" (EXAMPLE)
    #            path local para colocar os vídeos baixados

    pull_command = "adb pull {0} {1}".format(path_from, path_to)
    print(pull_command)
    os.system(pull_command)

    complete_path = path_to + str(r"\video")

    videos_to_delete = glob.glob("{0}/*.mp4".format(complete_path), recursive=True)
    print("videos to delete: ", videos_to_delete)
    thumbs_to_delete = glob.glob("{0}/*.jpg".format(complete_path), recursive=True)
    print("thumbs to delete: ", thumbs_to_delete)

    # deleta os videos do diretorio do android(emulador ou mobile)
    for video in videos_to_delete:
        adb_del_vid_command = "adb shell rm {0}/{1}".format(path_from, os.path.basename(video))
        #adb_del_vid_command = "adb shell rm -f {0}{1}".format(path_from, video)
        print("adb del videos: ", adb_del_vid_command)
        os.system(adb_del_vid_command)

    # deleta as thumbs do diretorio do android(emulador ou mobile)
    for thumb in thumbs_to_delete:
        adb_del_thb_command = "adb shell rm {0}/{1}".format(path_from, os.path.basename(thumb))
        #adb_del_thb_command = "adb shell rm -f {0}{1}".format(path_from, video)
        print("adb del thumbs: ", adb_del_thb_command)
        os.system(adb_del_thb_command)
    

def filtrate_directory(ext_to_keep, ext_to_remove, path):

	# ext_to_keep = "mp4" (EXAMPLE)
	# ext_to_remove = "jpg" (EXAMPLE)

    # path = "C:\Users\joaofernando\Documents\Roda\git_acoes_suspeitas\acoes_suspeitas\v_acoes_susp\manage_videos"

    complete_path = path + str(r"\video")
    print("complete path: ", complete_path)

    videos_files_list = glob.glob("{0}/*.{1}".format(complete_path, ext_to_keep), recursive=True)
    thumbs_files_list = glob.glob("{0}/*.{1}".format(complete_path, ext_to_remove), recursive=True)
    print("videos files list: ", videos_files_list)
    print("thumbs files list: ", thumbs_files_list)

    for thumb in thumbs_files_list:

        del_command = "del {0}".format(thumb)
        print(del_command)
        os.system(del_command)

    # lista tudo que ha no diretorio
    #dir_list = glob.glob(complete_path + "/*", recursive=True)
    #print("dir list: ", dir_list)

    return videos_files_list


def remove_session_path(sess_path_to_remove, mibo_path):

    command = "adb shell rm {0}/*".format(sess_path_to_remove)
    print(command)
    os.system(command)

    out = subprocess.check_output("adb shell ls {}".format(mibo_path), shell=True, text=True)

    if (len(out) == 0):
        removed = True
    elif (len(out) != 0):
        removed = False

    return removed


if __name__ == "__main__":

    pass