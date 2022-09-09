#%%
import os 

# O EMULADOR PRECISA ESTAR ABERTO NO ANDROID STUDIO

def get_videos_from_emulator(path_from, path_to):

    command = "adb pull {0} {1}".format(path_from, path_to)
    print(command)
    os.system(command)

def copy_to_modules_path():

    # funcao para copiar da pasta "video/" criada ao fazer o adb pull para a pasta dos modulos

    return

if __name__ == '__main__':

    # exp.: /mnt/sdcard/MiboCam/4319089/video/
    # complete_path_from = input("path completo da pasta do emulador para baixar videos: ")
    complete_path_from = "/mnt/sdcard/MiboCam/4319089/video/"
    # exp.: C:\Users\Mateus\Videos\antifraude
    # complete_path_to = input("path local para colocar os vídeos baixados: ")
    complete_path_to = "C:\Users\Mateus\Videos\antifraude"

    get_videos_from_emulator(complete_path_from, complete_path_to)