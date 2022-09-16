import os
import glob


def filtrate_directory(ext_to_keep, ext_to_remove, path=None):

	# ext_to_keep = "mp4" (EXAMPLE)
	# ext_to_remove = "jpg" (EXAMPLE)

    # path = "C:\Users\joaofernando\Documents\Roda\git_acoes_suspeitas\acoes_suspeitas\v_acoes_susp\manage_videos"

    if path is None:
        path = ""

    videos_files_list = glob.glob("*.{}".format(ext_to_keep))
    thumbs_files_list = glob.glob("*.{}".format(ext_to_remove))
    #print("videos files list: ", videos_files_list)
    #print("thumbs files list: ", thumbs_files_list)

    for thumb in thumbs_files_list:

        del_command = "del {0}".format(thumb)
        print(del_command)
        os.system(del_command)

    return videos_files_list


if __name__ == "__main__":

    pass