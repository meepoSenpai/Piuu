#! /bin/python3

'''
This is just a small python module I made to upload
an image to imgur, which then copies the image link
directly into the systems clipboard
'''

from imgurpython import ImgurClient
from getpass import getuser
from subprocess import call
import pyperclip
import notify2
import argparse

CLIENT = ImgurClient('5df57a2eb3ac87a', '')
SAVEFILE = "/home/{0}/.images.txt".format(getuser())
notify2.init("Piuu")
NOTIFICATOIN = notify2.Notification("The upload was completed!")

def upload_image(client, image_path, **kwargs):
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
    image = client.upload_from_path(image_path, config=config, anon=True)
    return image

def write_hash(image):
    '''
    This function writes the delete-hash to a file, so the user can check his uploaded images
    or delete the image afterwards
    '''
    to_save = "Image-URL: {0}, Delete-Hash: {1}".format(image['link'], image['deletehash'])
    with open(SAVEFILE, "a") as output:
        print(to_save, file=output)

def list_all_uploads():
    '''
    This function should list all previously uploaded files, that are stored in
    the /home/user/.images.txt
    '''
    with open(SAVEFILE, "r") as uploads:
        all_links = uploads.read()
    all_links = all_links.replace("Image-URL: ", "")\
                         .replace(" Delete-Hash: ", "")\
                         .split("\n")
    all_links.pop(-1)
    link_dict = {}
    for item in all_links:
        split_item = item.split(",")
        link_dict[split_item[0]] = split_item[1]
    sorted_keys = sorted(list(link_dict.keys()))
    for key_index in range(len(sorted_keys)):
        key = sorted_keys[key_index]
        print("{2}. The delete hash to {0} is {1}".format(key, link_dict[key], key_index))
    return sorted_keys, link_dict

def initiate_upload(image_path):
    '''
    This initiates the upload after it was determined which flag was set
    with the launch of the utility.
    '''
    upload = upload_image(CLIENT, image_path)
    pyperclip.copy(upload['link'])
    write_hash(upload)
    NOTIFICATOIN.show()
    return upload

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    IMG_GROUP = PARSER.add_mutually_exclusive_group()
    IMG_GROUP.add_argument('-s', '--screenshot', action="store_true",
                           help="Upload from screenshot")
    IMG_GROUP.add_argument('-sS', '--selection', action="store_true",
                           help="Lets you select a portion of the screen for upload")
    IMG_GROUP.add_argument('-f', '--filename', type=str,
                           help="Upload file from filename")
    IMG_GROUP.add_argument('-l', '--list', action="store_true",
                           help="List uploads")
    ARGS = PARSER.parse_args()
    if ARGS.list:
        list_all_uploads()
    elif ARGS.screenshot:
        call(["scrot", "/tmp/piuu.png"])
        initiate_upload("/tmp/piuu.png")
    elif ARGS.selection:
        call(["scrot", "-s", "/tmp/piuu.png"])
        initiate_upload("/tmp/piuu.png")
    elif ARGS.filename:
        initiate_upload(ARGS.filename)
