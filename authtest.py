from evernote.api.client import EvernoteClient

dev_token = 'S=s1:U=8d631:E=14a2adb30d1:C=142d32a04d4:P=1cd:A=en-devtoken:V=2:H=0dcc95fb7ef5991a98ec6c76605d53dd'
client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
user = userStore.getUser()
print user.username