#!/bin/python

# wp2evernote.py
# import Wordpress posts into Evernote as notes

import string
import os
import sys
import getopt
from xml.dom import minidom

infile = sys.argv[1]

def get_post(node):

	post = dict()
	post['title'] = node.getElementsByTagName('title')[0].firstChild.data
	post['date'] = node.getElementsByTagName('pubDate')[0].firstChild.data
	
	if node.getElementsByTagName('content:encoded')[0].firstChild != None:
		post['text'] = node.getElementsByTagName('content:encoded')[0].firstChild.data
	else:
		post['text'] = ''
		
	tags = []
	for subnode in node.getElementsByTagName('category'):
		tags.append(subnode.getAttribute('nicename'))
		
	post['tags'] = tags
	
	return post


#def create_note(date, title, body):
	# create a new note
	# set the date
	# set the title
	# create attachments from WP urls (images, etc.)
	# update body URL's to match attachment targets
	# set the body
	# upload to evernote
	
	
	
# get a list of wp posts
print 'reading %s' % infile
dom = minidom.parse(infile)
posts = []

for node in dom.getElementsByTagName('item'):
	post = get_post(node)
	posts.append(post)
	
# debug
print posts[0]