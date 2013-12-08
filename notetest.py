import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
#from evernote.eadm.type.ttypes import Types
#import evernote.edam.userstore.constants as UserStoreConstants
#from evernote.edam.error.ttypes import EDAMUserException
#from evernote.edam.error.ttypes import EDAMSystemException
#from evernote.edam.error.ttypes import EDAMNotFoundException
#from evernote.edam.error.ttypes import EDAMErrorCode

dev_token = 'S=s1:U=8d631:E=14a2adb30d1:C=142d32a04d4:P=1cd:A=en-devtoken:V=2:H=0dcc95fb7ef5991a98ec6c76605d53dd'
client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
user = userStore.getUser()
#print user.username

noteStore = client.get_note_store()
notebooks = noteStore.listNotebooks()
for n in notebooks:
	print n.name
	
	
note = Types.Note()
note.title = 'A test note'
note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>this is the test note</en-note>'
note = noteStore.createNote(note)