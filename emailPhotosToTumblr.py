# Posts a folder of pics to your tumblr, uploading them as single image posts.
import os
import time
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import copy

# for sorting
import re


EMAIL_FROM = "personal.email@gmail.com"
EMAIL_TO = "tumblr.email@tumblr.com"
DIR_PICS = "pics"


class TumblrPhotoUploader:
    """
    Use this class to upload pictures to your tumblr.

    It moves through a folder of pictures, uploading them to your tumblr as
    single photo posts.
    """

    # Set it up with the default addresses of my tumblr.
    # Start the cursor over list at 0, take 25 chunks
    # Reads in the file names and sorts them.
    def __init__(
        self,
        fro=EMAIL_FROM,
        to=EMAIL_TO,
        directory=DIR_PICS,
        cursor=0,
        chunk=25
    ):
        """
        Get the object up and running. Starts the cursor over the list,
        beginning at cursor and up until cursor + chunk. Sorts them nicely.

        Params:
            fro: default EMAIL_FROM. The email address you want to send from
            to: default EMAIL_TO. The email address you're sending to. This is
                your tumblr upload email. Find it on your tumblr blog.
            directory: default PICS. The directory where your pictures are
                stored. Relative to the directory containing this script.
            cursor: default 0. The starting point in the folder. Default value
                is 0. This is necessary because it often happens that tumblr
                loads things out of order and you have to delete the last 10,
                say, and then restart somewhere along the line. This variable
                lets you handle this more easily without just deleting the old
                ones in the directory.
            chunk: default 25. the number of pictures you upload at a time.
        """
        self.fro = fro
        self.to = to
        self.cwd = os.getcwd()
        self.filenames = os.listdir(self.cwd + '/' + directory)
        self.filenames = self.sort_nicely(self.filenames)
        self.cursor = cursor
        self.chunk = chunk
        self.delay = 30

    def sort_nicely(self, l):
        copied = copy.deepcopy(l)
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        copied.sort(key=alphanum_key)
        return copied

    def startServer(self, host='localhost'):
        print 'starting server'
        self.s = smtplib.SMTP(host)

    def nextWave(self):
        """
        Upload the next waves of photos, from cursor to cursor + chunk.
        """
        # the point to which you're read
        nextBite = self.cursor + self.chunk
        #start the server each time
        self.startServer()
        for file in self.filenames[self.cursor:nextBite]:
            time.sleep(self.delay)
            msg = MIMEMultipart()
            msg['Subject'] = file
            msg['From'] = self.fro
            msg['To'] = self.to
            fp = open(self.cwd + '/pics/' + file, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            img.add_header('Content-Disposition', 'attachment', filename=file)
            msg.attach(img)
            try:
                print 'sending: ' + file
                # print to get any errors.
                print self.s.sendmail(self.fro, self.to, msg.as_string())
            except:  # catch all exceptions
                print 'error, trying to restarting server'
                # wait 60 seconds to make sure all the previous sends
                # got there
                # in a test, python didn't actually get there, it took ages for the
                # 3 following the crash to work. not sure why.
                print 'sleeping 60 seconds to let tumblr catch up'
                time.sleep(60)
                self.startServer()
                print 'resending: ' + file
                print self.s.sendmail(self.fro, self.to, msg.as_string())
        self.cursor = self.cursor + self.chunk

    def rollback(self):
        """
        Call this after the previous wave has to be deleted. This is basically
        just to account for the fact that tumblr so often doesn't post the
        images in order as you send them. Rolls back to the cursor position
        minus the chunk size. Therefore you should only manually delete posts
        in groups of size chunk if you want to use this method.
        """
        self.cursor = self.cursor - self.chunk
