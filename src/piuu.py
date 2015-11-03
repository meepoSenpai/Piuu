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
    notify2.Notification("Uploading...").show()
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
    sorted_keys, link_dict = obtain_list_and_keys()
    for key_index in range(len(sorted_keys)):
        key = sorted_keys[key_index]
        print("{2}. The delete hash to {0} is {1}".format(key, link_dict[key], key_index + 1))

def obtain_list_and_keys():
    '''
    Returns a list of delete hashes and a dictionary of
    links in relation to the deletehash
    '''
    with open(SAVEFILE, "r") as uploads:
        all_links = uploads.read()
    all_links = all_links.replace("Image-URL: ", "")\
                         .replace(" Delete-Hash: ", "")\
                         .split("\n")[:-1]
    link_dict = {}
    for item in all_links:
        split_item = item.split(",")
        link_dict[split_item[0]] = split_item[1]
    sorted_keys = sorted(list(link_dict.keys()))
    return sorted_keys, link_dict

def delete_by_index(index):
    '''
    This method will delete an image on basis of an index
    taken from all listed uploads
    '''
    sorted_keys, link_dict = obtain_list_and_keys()
    try:
        delhash = link_dict[sorted_keys[index - 1]]
        with open(SAVEFILE, 'r') as uploads:
            all_uploads = uploads.read().replace('\n', '\n~')\
                                        .split('~')[:-1]
        to_write = [x for x in all_uploads if not x.endswith(delhash + '\n')]
        with open(SAVEFILE, 'w') as uploads:
            uploads.writelines(to_write)
        CLIENT.delete_image(delhash)
    except IndexError:
        print("Invalid index given")

def initiate_upload(image_path):
    '''
    This initiates the upload after it was determined which flag was set
    with the launch of the utility.
    '''
    upload = upload_image(CLIENT, image_path)
    pyperclip.copy(upload['link'])
    write_hash(upload)
    notify2.Notification("Upload completed!").show()
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
    IMG_GROUP.add_argument('-d', '--delete', action="store_true",
                           help="Delete image from imgur")
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
    elif ARGS.delete:
        list_all_uploads()
        delete_by_index(int(input("What image do you want to delete? ")))
