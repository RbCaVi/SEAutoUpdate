import json,requests

import util
if util.qpy:
  requests.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

session=requests.Session()

apiendpoint="https://spaceexploration.miraheze.org/w/api.php"
headers={'User-Agent':"Robert/1.0 (robert@robertvail.info)"}

username="RbCaVi@SEAutoUpdate"
password="lrqc55rc1r6dqtgl3h9b1hq8u8ccbldv"

def pj(x):
  print(json.dumps(x,indent=2))

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
  pj(response.json())

def edit(title,content,start,base='now',summary='Automatically edited by SEAutoUpdate',minor=False,createonly=True):
  query={
       "formatversion":"2",
       "format":"json",
       "action":"query",
       "meta":"tokens"
  }
  response=session.get(url=apiendpoint,params=query,headers=headers)
  data=response.json()
  token=data['query']['tokens']['csrftoken']
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

#pj(getpages(['umbrella']))

login(username,password)


