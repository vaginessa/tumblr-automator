# tumblr-automator

> Upload images to your tumblr via email

## Overview

[Tumblr] (http://www.tumblr.com) is a convenient way to manage a photo blog.
If you have a lot of pictures to be uploaded at one time, however, there is no
easy way to do it. This quick-and-dirty script uploads pictures to your blog,
one at at a time, for one picture per post. This makes it easy to do bulk
uploads while maintaining a one-pic-per-post style on your blog.

They will [appear like this] (http://wherehewasdrinking.tumblr.com/). The text
I go through and add by hand.

## Usage

Clone the repo. Put the pictures you want uploaded in the `pics/` directory.
Start the python repl and use it like so:

```python
import tumblr_automator

personal_email = 'personal.email@yourdomain.com'
tumblr_email = 'upload.email@tumblr.com'
automator = tumblr_automator.TumblrAutomator(
    fro=personal_email,
    to=tumblr_email
)
automator.nextWave()
```

`personal_email` is the email you want the pictures to originate from. I use my
gmail.

`tumblr_email` is the upload email of your tumblr blog. Look in your blog's
dashboard to find it.

If you want a different folder than `pics`, you can pass it into the
`TumblrAutomator` by specifying a value for the `directory` argument.

## SMTP Server

Note that this requires an smtp server to be running on your machine and
reachable as `localhost`. If you're using a unix system you might be able to
get away with this just by doing `sudo postfix start` in a shell before running
the script.

> If your ISP blocks traffic on port 25, you might have trouble getting
this to work.

Once the server is up, you can run
`date | mail -s test personal.email@yourdomain.com` to see if your mail is
getting through.

If you're having trouble, try looking at the log to see what is going on.
If your activity is being blocked, you might end up with a `no route to host`
message. To tail the log (at least for postfix and at least on a Mac), you can
try:

```shell
tail -f /var/log/mail.log
```

This will let you watch the log as messages come in. Don't forget that you can
use `ctrl+c` to quit.

If you're not having any luck (and you're on a unix system), try running:

```shell
telnet smtp.gmail.com 25
```

> To get out of the telnet protocol, you'll have to use the escape sequence
and then hit q. In my case, this looks like: `ctrl+]`, `q`.

This should try to connect to one of google's smtp servers. If you can't get on
this, it is likely that you are being rejected because google doesn't trust
your IP address.

I get around this by getting postfix running on my machine and then running
the script on a university network.

Another option might be to edit the script to authenticate using a secure
connection and your google sign in. Take a look at the [Resources section]
(#resources) for an example.

You can also configure it by using a
postfix relay through a trusted smtp server, but you're on your own for that.


## Caveats

A few things limit this script.

First, the last time I checked there was a limit of 50 email uploads per day.
Any more than that and they just get swallowed up.

Second, the posts don't always appear in the same order you send them. Whether
it's on tumblr's end or just one random email bouncing around the network a
while longer, you might need to look out for this. I wrote the script for a
blog where I want the posts to appear in a particular order. This means I'll
often end up catching a post in the wrong order, deleting the subsequent posts,
and restarting at the point where things went wrong. Ameliorating this problem
is why I added a wait to the script, but this still didn't completely fix it.


## Resources

* A good starting point for getting postfix set up on a mac:
[http://benjaminrojas.net/configuring-postfix-to-send-mail-from-mac-os-x-mountain-lion/] (http://benjaminrojas.net/configuring-postfix-to-send-mail-from-mac-os-x-mountain-lion/)
* An example of using the Python smtp library. This can be useful for debugging
when you're trying to see if your server is set up correctly and you can
send mail. Note that this uses gmail's server. [http://www.mkyong.com/python/how-do-send-email-in-python-via-smtplib/]
(http://www.mkyong.com/python/how-do-send-email-in-python-via-smtplib/)
