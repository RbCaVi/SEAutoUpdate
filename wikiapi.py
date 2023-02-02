import json,requests,os

import util
if util.qpy:
  requests.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

csrftoken=None

session=requests.Session()

apiendpoint="https://spaceexploration.miraheze.org/w/api.php"
headers={'User-Agent':"SEAutoUpdate/1.0 (robert@robertvail.info)"}

username="RbCaVi@SEAutoUpdate"
password="lrqc55rc1r6dqtgl3h9b1hq8u8ccbldv"

def getpages(pages):
  query={
    "formatversion":"2",
    "format":"json",
    "action":"query",
    "prop":"revisions",
    "rvprop":'|'.join([
      "content",
      #"ids",
      "timestamp"
    ]),
    "rvslots":"main",
    "curtimestamp":"true",
    "titles":"|".join(pages)
  }
  response=session.get(url=apiendpoint,params=query,headers=headers)
  data=response.json()
  return data

def login(name,pw):
  query={
       "formatversion":"2",
       "format":"json",
       "action":"query",
       "meta":"tokens",
       "type":"login"
  }
  response=session.get(url=apiendpoint,params=query,headers=headers)
  data=response.json()
  token=data['query']['tokens']['logintoken']
  query={
       "formatversion":"2",
       "format":"json",
       "action":"login",
       "lgname":name,
       "lgpassword":pw,
       "lgtoken":token,
  }
  response=session.post(url=apiendpoint,data=query,headers=headers)
  print("Logged in as "+name)
  #util.pj(response.json())

def getcsrftoken():
    global csrftoken
    if csrftoken is None:
        query={
           "formatversion":"2",
           "format":"json",
           "action":"query",
           "meta":"tokens"
        }
        response=session.get(url=apiendpoint,params=query,headers=headers)
        data=response.json()
        csrftoken=data['query']['tokens']['csrftoken']
    return csrftoken

def gettimestamp():
    query={
       "formatversion":"2",
       "format":"json",
       "action":"query",
       "curtimestamp":"true"
    }
    response=session.get(url=apiendpoint,params=query,headers=headers)
    data=response.json()
    return data["curtimestamp"]

def edit(title,content,start,base='now',summary='Automatically edited by SEAutoUpdate',minor=False,createonly=True):
  token=getcsrftoken()
  query={
       "formatversion":"2",
       "format":"json",
       "action":"edit",
       "title":title,
       "text":content,
       "summary":summary,
       "basetimestamp":base,
       "starttimestamp":start,
       "token":token,
       "bot":"true",
  }
  if not minor:
    query['notminor']='true'
  if createonly:
    query['createonly']='true'
  
  response=session.post(url=apiendpoint,data=query,headers=headers)
  data=response.json()
  return data

def read_chunks(file,size=1024):
    while True:
        data=file.read(size)
        if not data:
            break
        yield data

def upload(filename,uploadname,comment='Uploaded by SEAutoUpdate',chunksize=16384):
    """Send multiple post requests to upload a file in chunks using `stash` mode.
    Stash mode is used to build a file up in pieces and then commit it at the end
    """
    
    file=open(filename,'rb')
    size=os.stat(filename).st_size
    
    token=getcsrftoken()

    chunks = read_chunks(file,chunksize)
    chunk = next(chunks)

    # Parameters for the first chunk
    params = {
        "action": "upload",
        "stash": 1,
        "filename": uploadname,
        "filesize": size,
        "offset": 0,
        "format": "json",
        "token": token,
        "ignorewarnings": 1
    }
    index = 0
    filedata = {'chunk':('{}.jpg'.format(index), chunk, 'multipart/form-data')}
    index += 1
    response = session.post(apiendpoint, files=filedata, data=params)
    data = response.json()
    util.pj(data)

    # Pass the filekey parameter for second and further chunks
    for chunk in chunks:
        params = {
            "action": "upload",
            "stash": 1,
            "offset": data["upload"]["offset"],
            "filename": uploadname,
            "filesize": size,
            "filekey": data["upload"]["filekey"],
            "format": "json",
            "token": token,
            "ignorewarnings": 1
        }
        filedata = {'chunk':('{}.jpg'.format(index), chunk, 'multipart/form-data')}
        index += 1
        response = session.post(apiendpoint, files=filedata, data=params)
        data = response.json()
        util.pj(data)

    # Final upload using the filekey to commit the upload out of the stash area
    params = {
        "action": "upload",
        "filename": uploadname,
        "filekey": data["upload"]["filekey"],
        "format": "json",
        "comment": comment,
        "token": token,
        "ignorewarnings":1
    }
    response = session.post(apiendpoint, data=params)
    data = response.json()
    util.pj(data)

#pj(getpages(['umbrella']))

login(username,password)

#file="/storage/emulated/0/Download/usb.jpg"

#upload(file,'usb-data-card.jpg')

gettimestamp()