import data
import fix
import locale
import util
import wikiapi
import process

process.init()

import sys

datacards=[x for x in data.data['recipe'] if 'data' in x]

#util.pj(datacards)

#print(len(datacards))

#util.pj([x for x in data.data['recipe'] if 'science-pack' in x])
#util.pj([x for x in data.data['recipe'] if 'simulation' in x])
#util.pj([x for x in data.data['recipe'] if 'insight' in x])
#util.pj([x for x in data.data['recipe'] if 'catalogue' in x])
#sys.exit()
#util.pj(data.data['recipe'][datacards[0]])
#util.pj(data.data['recipe']['se-formatting-1'])
#util.pj(processrecipe(datacards[0]))
