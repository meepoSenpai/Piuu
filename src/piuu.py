#! /bin/python3

'''
This is just a small python module I made to upload
an image to imgur, which then copies the image link
directly into the systems clipboard
'''

import csv
import argparse
from getpass import getuser
from subprocess import call

import notify2
import pyperclip
from imgurpython import ImgurClient

CLIENT = ImgurClient('5df57a2eb3ac87a', '')
SAVEFILE = "/home/{0}/.images.csv".format(getuser())
notify2.init("Piuu")

def upload_image(client, image_path, argdict={}):
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
    if argdict != {}:
        for key in iter(argdict):
            config[key] = argdict[key]
    notify2.Notification("Uploading...").show()
    image = client.upload_from_path(image_path, config=config, anon=True)
    return image

def write_hash(image):
    '''
    This function writes the delete-hash to a file, so the user can check his uploaded images
    or delete the image afterwards
    '''
    # to_save = "Image-URL: {0}, Delete-Hash: {1}".format(image['link'], image['deletehash'])
    to_save = [image['link'], image['deletehash']]
    with open(SAVEFILE, "a") as output:
        writer = csv.writer(output)
        writer.writerow(to_save)

def list_all_uploads():
    '''
    This function should list all previously uploaded files, that are stored in
    the /home/user/.images.txt
    '''
    links = obtain_list_and_keys()
    for key, link_hash in enumerate(links):
        print("{0}. The deletehash for {1} is {2}.".format(key, link_hash[0], link_hash[1]))

def obtain_list_and_keys():
    '''
    Returns a list of delete hashes and a dictionary of
    links in relation to the deletehash
    '''
    with open(SAVEFILE, "r") as uploads:
        all_lines = list(csv.reader(uploads))
    link_list = [(x[0], x[1]) for x in all_lines]
    return link_list

def delete_by_index(index):
    '''
    This method will delete an image on basis of an index
    taken from all listed uploads
    '''
    #sorted_keys, link_dict = obtain_list_and_keys()
    link_list = obtain_list_and_keys()
    try:
        delhash = link_list[index][1]
        with open(SAVEFILE, 'r') as uploads:
            all_uploads = list(csv.reader(uploads))
        to_write = [x for x in all_uploads if not delhash == x[1]]
        with open(SAVEFILE, 'w') as uploads:
            csv.writer(uploads).writerows(to_write)
        CLIENT.delete_image(delhash)
    except IndexError:
        print("Invalid index given")

def initiate_upload(image_path, argdict={}):
    '''
    This initiates the upload after it was determined which flag was set
    with the launch of the utility.
    '''
    upload = upload_image(CLIENT, image_path, argdict)
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
    IMAGE_TAGS = PARSER.add_argument_group()
    IMAGE_TAGS.add_argument('-n', '--name', type=str,
                            help='Add a name to the Image')
    IMAGE_TAGS.add_argument('-D', '--description', type=str,
                            help='Add a description')
    IMAGE_TAGS.add_argument('-t', '--title', type=str,
                            help='Add an image Title')
    IMG_GROUP.add_argument('-g', '--graphical-ui', action='store_true',
                           help='Open the GUI')
    ARGS = PARSER.parse_args()
    ARGDICT = {}
    if ARGS.name or ARGS.description or ARGS.title:
        if ARGS.name:
            ARGDICT['name'] = ARGS.name
        if ARGS.description:
            ARGDICT['description'] = ARGS.description
        if ARGS.title:
            ARGDICT['title'] = ARGS.title
    if ARGS.list:
        list_all_uploads()
    elif ARGS.screenshot:
        call(["scrot", "/tmp/piuu.png"])
        initiate_upload("/tmp/piuu.png", ARGDICT)
    elif ARGS.selection:
        call(["scrot", "-s", "/tmp/piuu.png"])
        initiate_upload("/tmp/piuu.png")
    elif ARGS.filename:
        initiate_upload(ARGS.filename)
    elif ARGS.delete:
        list_all_uploads()
        delete_by_index(int(input("What image do you want to delete? ")))
