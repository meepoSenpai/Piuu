#Piuu - The Python Imgur Upload Utility

This is a small terminal application that lets you easily upload
images on [Imgur](http://imgur.com) because in my personal opinion
using the website is a huge pain.

The deletehash and the Image links of the images you've uploaded are
all stored in ~/.images.txt so you can delete the images any time you
want to (or check back for previous uploads)

###Installation

So far installation will only be possible by cloning the repo and either
adding the script to your $PATH or linking it somewhere where it is in your path.

You'll need to install the requirements from the requirements.txt.

###Usage

Simply run this in your terminal:
```
piuu.py -f [image]
```

The image link will also automatically be copied to your clipboard thanks to the 
pyperclip module.

```
piuu.py -s
```

If you pass the `-s` flag instead of an image-name you will automatically upload a screenshot.
The delete hash and image link will be stored in ~/.images.txt regularly and the link will be
stored in the system clipboard.

```
piuu.py -sS
```

The `-sS` flag allows you to only screencap a selection of your screen. Otherwise it works exactly
the same as `-s`

```
piuu.py -l
```

`-l` will list all uploads to date, including the deletehash of the image.

###Features to come

So far uploads are always done anonymously, so I am planning on adding login-functionality
sometime soon, and the possibility to edit the image tags and album it is uploaded to.
