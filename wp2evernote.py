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
	
	# set the date
	note.date = post['date']
	
	# set the title
	note.title = post['title']
	
	# create attachments from WP urls (images, etc.)
	# update body URL's to match attachment targets
	# set the body
	note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
	note.content += post['text']
	
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
	
# debug
print posts[10]

# generate notes
notes = []
for post in posts:
	notes.append(create_note(post))
	
# debug
print notes[10]




