#! /bin/python3

'''
This is just a small python module I made to upload
an image to imgur, which then copies the image link
directly into the systems clipboard
'''

from imgurpython import ImgurClient
from sys import argv, exit
from getpass import getuser
from subprocess import call
import pyperclip

CLIENT = ImgurClient('5df57a2eb3ac87a', '')
SAVEFILE = "/home/{0}/.images.txt".format(getuser())
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

def write_hash(image):
    '''
    This function writes the delete-hash to a file, so the user can check his uploaded images
    or delete the image afterwards
    '''
    to_save = "Image-URL: {0}, Delete-Hash: {1}".format(image['link'], image['deletehash'])
    with open(SAVEFILE, "a") as output:
        print(to_save, file=output)

if __name__ == '__main__':
    if argv[1] == '-s':
        IMAGE_PATH = "/tmp/piuu.png"
        if len(argv) == 2:
            call(["scrot", "/tmp/piuu.png"])
        elif argv[2] == "--selection":
            call(["scrot", "-s", "/tmp/piuu.png"])
        else:
            print("Faulty arguments given")
            exit()

    UPLOAD = upload_image(CLIENT)
    pyperclip.copy(UPLOAD['link'])
    write_hash(UPLOAD)
