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
piuu.py [image]
```

The image link will also automatically be copied to your clipboard thanks to the 
pyperclip module.

###Features to come

So far uploads are always done anonymously, so I am planning on adding login-functionality
sometime soon, and the possibility to edit the image tags and album it is uploaded to.
