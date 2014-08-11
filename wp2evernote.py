#!/usr/bin/python
# -*- coding: utf-8 -*-


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
from bs4 import BeautifulSoup


def get_post(node):
	post = dict()

        #check and add title name to post
        try:
	    post['title'] = node.getElementsByTagName('title')[0].firstChild.data
        except:
            post['title'] = 'no name'

	post['date'] = node.getElementsByTagName('pubDate')[0].firstChild.data
        post['status'] = node.getElementsByTagName('wp:status')[0].firstChild.data

        try:
		post['text'] = node.getElementsByTagName('content:encoded')[0].firstChild.data
        except:
		post['text'] = ''

	tags = []
	for subnode in node.getElementsByTagName('category'):
		tags.append(subnode.getAttribute('nicename'))

	post['tags'] = tags

        return post

def get_image(image_data):
#took from https://github.com/evernote/evernote-sdk-python/blob/master/sample/client/EDAMTest.py
        pass

def create_note(post):

	# create a new note
	note = Types.Note()
	note.notebookGuid = notebook_guid

	# set the date (converted from ex: Wed, 28 Aug 2013 15:08:10 +0000)
	pattern = '%a, %d %b %Y %H:%M:%S +0000'
	note.created = int(time.mktime(time.strptime(post['date'], pattern))) * 1000

	# set the title
	note.title = post['title'].encode('utf-8')

	# add tags
	tags = []
	for tag in post['tags']:
		tags.append(tag.encode('utf-8'))

        # check if a page, add relative tag
        #if post['type'] == 'page' :
        #    tags.append('page')

        # add the magic 'published' tag to make it a blog post IF it was already published
        if post['status'] == 'publish' :
            tags.append('published')

	note.tagNames = tags

	# TODO: create attachments from WP urls (images, etc.)
	# TODO: update body URL's to match attachment targets

	# clean-up the post's text
	scrubbed_content = post['text']

        # remove all prohibited attributes with bs4
        proibithed_attrs = ['id','class','onclick','ondbliclick','accesskey','data','dynsrc','tabindex']
        proibithed_elements = ['applet','base','basfont','bgsound','blink','body','button','dir','embed','fieldset','form','frame','frameset','head','html','iframe','ilayer','input','isindex','label','layer','legend','link','marquee','menu','meta','noframes','noscript','object','optgroup','option','param','plaintext','script','select','style','textarea','xml']
        soup = BeautifulSoup(scrubbed_content)

        for bad_attr in proibithed_attrs :
            for value in soup.findAll() :
                del(value[bad_attr])

        bad_elements = soup.findAll(proibithed_elements)
        [element.extract() for element in bad_elements]

        # get back to str
        scrubbed_content = str(soup)

	# convert newlines to breaks
	scrubbed_content = scrubbed_content.replace('\n', '<br/>')

	# close br's
	scrubbed_content = scrubbed_content.replace('<br>', '<br/>')

	# clos hr's
	scrubbed_content = scrubbed_content.replace('<hr>', '<hr/>')

        while scrubbed_content.find('[caption') > 0:

		start_idx = scrubbed_content.find('[caption')
		end_idx = scrubbed_content.find(']', start_idx)

		scrubbed_content = scrubbed_content[:start_idx] + scrubbed_content[end_idx + 1:]

	while scrubbed_content.find('[/caption]') > 0:
		start_idx = scrubbed_content.find('[/caption]')
		end_idx = start_idx + 10
		scrubbed_content = scrubbed_content[:start_idx] + scrubbed_content[end_idx:]

	# set the body
	note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
	note.content += '<en-note>'
	note.content += scrubbed_content
	note.content += '</en-note>'

	return note


def upload_note(note):
	client = EvernoteClient(token=auth_token, sandbox=False)
	noteStore = client.get_note_store()
	note = noteStore.createNote(note)


if len(sys.argv) >= 3:

	# get the auth token
	auth_token = sys.argv[1]

	# ask user to pick a notebook
	client = EvernoteClient(token=auth_token, sandbox=False)
	noteStore = client.get_note_store()
	notebooks = noteStore.listNotebooks()

	notebook_idx = 0
	print('Select a notebook to upload to:')
	for n in notebooks:
		print '%d - %s' % (notebook_idx, n.name)
		notebook_idx += 1

	selected_notebook = int(raw_input('>'))
	notebook_guid = notebooks[selected_notebook].guid

	# get the export file to process
	infile = sys.argv[2]

	# read posts from input file
	dom = minidom.parse(infile)

	# process posts & pages
	posts = []
        pages = []
	for node in dom.getElementsByTagName('item'):

            if node.getElementsByTagName('wp:post_type')[0].firstChild.data == 'post' :

                post = get_post(node)
		posts.append(post)

	    # TODO: implement pages import
            #elif node.getElementsByTagName('wp:post_type')[0].firstChild.data == 'page' :

                #page = get_page(node)
                #pages.append(page)



	print 'processing %d posts' % len(posts)

	# generate notes
	notes = []
	for post in posts:
		notes.append(create_note(post))


	# upload notes
	# resume if post # is specified
	starting_post = 0
	if len(sys.argv) > 3:
		starting_post = int(sys.argv[3])

	# stop early if specified
	ending_post = len(notes)
	if len(sys.argv) > 4:
		ending_post = int(sys.argv[4])

	if starting_post != 0:
		print 'starting at post %d' % starting_post

	# header
	print('post\tstatus')

	note_idx = 0
	upload_errors = 0
	for note in notes:

		if note_idx >= starting_post:
			sys.stdout.write('%d %s' % (note_idx, note.title))

			try:
				upload_note(note)
				sys.stdout.write('\tcomplete\n')

			except:
				sys.stdout.write('\tfailed\n')
				#print note
				print sys.exc_info()
				#print 'error uploading note %d' % note_idx
				upload_errors += 1
				#sys.exit(1)

		if note_idx == ending_post:
			break

		note_idx += 1

	total_uploaded = ((ending_post - starting_post) - upload_errors) + 1
	print '%d posts uploaded' % total_uploaded
	print '%d upload errors' % upload_errors

else:

	print 'usage: wp2evernote <token> <wordpress export.xml> <starting post> <ending post>\n'
