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
import sys

CLIENT = ImgurClient('5df57a2eb3ac87a', '')
SAVEFILE = "/home/{0}/.images.txt".format(getuser())
IMAGE_PATH = sys.argv[-1]
notify2.init("Piuu")
NOTIFICATOIN = notify2.Notification("The upload was completed!")

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

def initiate_upload():
    '''
    This initiates the upload after it was determined which flag was set
    with the launch of the utility.
    '''
    upload = upload_image(CLIENT)
    pyperclip.copy(upload['link'])
    write_hash(upload)
    NOTIFICATOIN.show()

if __name__ == '__main__':
    if sys.argv[1] == '-s':
        IMAGE_PATH = "/tmp/piuu.png"
        if len(sys.argv) == 2:
            call(["scrot", "/tmp/piuu.png"])
        elif sys.argv[2] == "--selection":
            call(["scrot", "-s", "/tmp/piuu.png"])
        else:
            print("Faulty arguments given")
            sys.exit()
        initiate_upload()
    elif sys.argv[1] == '-l':
        list_all_uploads()
    elif sys.argv[1] == '-f':
        initiate_upload()
    else:
        print("Invalid arguments, please consult someone who" +\
              " knows more than you do")
