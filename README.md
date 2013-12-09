A simple script to import Wordpress posts into Evernote, designed to produce posts for [Postach.io](http://postach.io).

Be warned, this script is very primative at this stage.  Someday it will do a better job, unless someone else writes something better, then I'll probably just use that instead ;)

###Useage:###

     wp2evernote <token> <wordpress export.xml> <starting post> <ending post>

*  token: your developer token
*  wordpress export.xml: the file you exported from Wordpress
*  starting post: optional, the first post to process
*  ending post: optional, the last post to process

After starting the script you'll be prompted to select the notebook you'd like the posts uploaded to.  Select a notebook by typing in the number to the left of the name and press "enter".  

Next you'll see a list of each post and it's upload status.  Uploads will fail for all sorts of mysterious reasons, this is why the optional start and end ranges are provided to allow you to selectively publish posts that have failed but you've attempted to modify to get them to work.

It's important to note that if you run the script more than once, and you don't specify a range of failed posts, the script will happily post duplicate notes!

The script also converts WP categories to tags, and also appends the "published" tag used by Postach.io to turn the new notes into posts immediately (at some point I'll make this optional, probably).

Reference:

*  http://luisrei.com/post/17376030577/out-of-wordpress-com-and-into-evernote-com
*  http://virantha.com/2013/11/04/creating-new-notes-and-attaching-files-using-evernotes-python-api/
*  http://dev.evernote.com/doc/articles/enml.php
*  http://dev.evernote.com/doc/start/python.php
