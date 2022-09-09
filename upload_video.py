import boto3
from botocore.exceptions import ClientError
from pprint import pprint
import glob
#import pandas as pd
import logging
import os
import sys
import threading


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


def upload_file(file_name, bucket, folder, object_name=None):
    ''' Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to # "flagged-videos"
        :param folder: folder in bucket to upload to # "videos"
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False '''
    
    s3_client = boto3.client('s3')

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    #print("file name: ", file_name)

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, folder + '/' + file_name, Callback=ProgressPercentage(file_name)) # talvez a funcao nao retorne este "response" e nao haja o que printar
        print("uploaded tried")
    except ClientError as e:
        logging.error(e)
        return False, None
        
    # tratar o file name, pois o nome do arquivo vem com contrabarras no lugar de barras
    file_name.replace("\\", "/")
    object_url = "https://" + bucket + ".s3.amazonaws.com/" + "folder" + "/" + file_name

    return True, object_url

if __name__ == "__main__":

    pass