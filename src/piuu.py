'''
This is just a small python module I made to upload
an image to imgur, which then copies the image link
directly into the systems clipboard
'''

from imgurpython import ImgurClient
from sys import argv
import pyperclip

CLIENT = ImgurClient('5df57a2eb3ac87a', '')
IMAGE_PATH = argv[-1]

def upload_image(client, **kwargs):
    '''
    Uploads the image given in the Command line
    Arguments
    '''
    config = {
        'album' : None,
        'name' : None,
        'title' : None,
        'description' : None
    }
    if kwargs == {}:
        config = {
            'album' : None,
            'name' : 'RandImg',
            'title' : 'RandImg',
            'description' : 'RandImg'
        }
    print("Uploading....")
    image = client.upload_from_path(IMAGE_PATH, config=config, anon=True)
    return image

if __name__ == '__main__':
    UPLOAD = upload_image(CLIENT)
    pyperclip.copy(UPLOAD['link'])
    print(UPLOAD)

