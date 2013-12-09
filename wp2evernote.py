#!/bin/python

# wp2evernote.py
# import Wordpress posts into Evernote as notes

import string
import os
import sys
import getopt
from xml.dom import minidom
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import time


# get the export file to process
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


def create_note(post):

	# create a new note
	note = Types.Note()
	
	# set the date (converted from ex: Wed, 28 Aug 2013 15:08:10 +0000)
	pattern = '%a, %d %b %Y %H:%M:%S +0000'
	note.created = int(time.mktime(time.strptime(post['date'], pattern))) * 1000
	
	# set the title
	note.title = post['title']
	
	# add tags
	tags = []
	for tag in post['tags']:
		tags.append(tag)
		
	note.tagNames = tags
	
	# TODO: create attachments from WP urls (images, etc.)
	# TODO: update body URL's to match attachment targets
	
	# clean-up the post's text
	scrubbed_content = post['text'].encode('utf-8')
	
	# convert newlines to breaks
	scrubbed_content = scrubbed_content.replace('\n', '<br/>')
	
	# remove class directives (ie: class="size-medium wp-image-1756")
	while scrubbed_content.find('class=') > 0:
		
		start_idx = scrubbed_content.find('class=')
		print start_idx
		
		end_idx = scrubbed_content.find('"', start_idx + 7)
		print end_idx
		
		scrubbed_content = scrubbed_content[:start_idx] + scrubbed_content[end_idx + 2:]
		
	# remove captions
	while scrubbed_content.find('[caption') > 0:
	
		start_idx = scrubbed_content.find('[caption')
		end_idx = scrubbed_content.find(']', start_idx)
		
		scrubbed_content = scrubbed_content[:start_idx] + scrubbed_content[end_idx + 1:]
		
	while scrubbed_content.find('[/caption]') > 0:
		start_idx = scrubbed_content.find('[/caption]')
		end_idx = start_idx + 10
		scrubbed_content = scrubbed_content[:start_idx] + scrubbed_content[end_idx:]
		
	#scrubbed_content = scrubbed_content.replace('class=', 'ass=')
	
	# set the body
	note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
	note.content += '<en-note>'
	note.content += scrubbed_content #post['text'].replace('\n', '<br/>')
	note.content += '</en-note>'
	
	return note
	
	
def upload_note(note):
	dev_token = 'S=s1:U=8d631:E=14a2adb30d1:C=142d32a04d4:P=1cd:A=en-devtoken:V=2:H=0dcc95fb7ef5991a98ec6c76605d53dd'
	client = EvernoteClient(token=dev_token)
	noteStore = client.get_note_store()
	note = noteStore.createNote(note)
	
	
# read posts from input file
print 'reading %s' % infile
dom = minidom.parse(infile)

# process posts
posts = []
for node in dom.getElementsByTagName('item'):
	post = get_post(node)
	posts.append(post)
	
print 'processing %d posts' % len(posts)

# generate notes
notes = []
for post in posts:
	notes.append(create_note(post))
	
# debug
print notes[517]
#print notes[11]

# try uploading one
upload_note(notes[517])






