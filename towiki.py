import process
import data
import util
import locales as locale

import copy

categories={
    'logistics':'Logistics',
    'production':'Production',
    'resources':'Resources',
    'intermediate-products':'Manufacturing',
    'combat':'Equipment and Combat',
    'science':'Science',
}

diff_prefixes={
	   'normal':'',
	   'expensive':'expensive-'
}

postfixes=['','2','3','4','5']

def numtostr(n):
    s=str(n)
    if s.startswith('0'):
        s=s[1:]
    return s

process.init()
data.init()

defaultrinfo={'producers':[]}
defaulttinfo={}

def towikitech(tech,info=None):
    if info is None:
        info=copy.deepcopy(defaulttinfo)
    else:
        info=copy.deepcopy(info)
    n=data.pdata['technology'][tech]
    info['allows']=process.postreqs['normal'][tech]
    info['effects']=process.unlocks['normal'][tech]
    info['required-technologies']=process.prereqs['normal'][tech]
    info['cost']=n['normal']['count']
    util.pj([
        	   (locale.itemlocale(pack[0],data.data),pack)
        	   for pack in
        	   n['normal']['packs']
        ])
    info['required-packs']=' + '.join([
        	   locale.itemlocale(pack[0],data.data)[0]+', '+numtostr(pack[1])
        	   for pack in
        	   n['normal']['packs']
        ])
    return info

def towikiitem(item,info=None):
    if info is None:
        info=copy.deepcopy(defaultrinfo)
    else:
        info=copy.deepcopy(info)
    proto=process.getitem(item)
    info['category']=categories[data.data['item-subgroup'][proto['subgroup']]['group']]
    info['internal-name']=item
    info['stack-size']=str(proto['stack_size'])
    return info

def towikirecipe(recipe,info=None,replace=None):
    if info is None:
        info=copy.deepcopy(defaultrinfo)
    else:
        info=copy.deepcopy(info)
    if type(recipe)==list:
        for x in recipe:
            info=towikirecipe(x,info,replace)
        return info
    if not replace:
        for i,postfix in enumerate(postfixes):
            props=['recipe','total-raw','expensive-recipe','expensive-total-raw']
            c=False
            for prop in props:
                if prop+postfix in info:
                    c=True
                    break
            if not c:
                break
    elif type(replace)==int:
        postfix=postfixes[replace]
    else:
        postfix=replace
    n=data.pdata['recipe'][recipe]
    info['producers']+=map(locale.itemlocale,process.madein[n['category']])
    for x in util.difficulty:
        if x not in n:
            continue
        prefix=diff_prefixes[x]
        ings=' + '.join([
        	   locale.itemlocale(ing[0],data.data)[0]+', '+numtostr(ing[1])
        	   for ing in
        	   [['time',n[x]['time'],'time']]+n[x]['ingredients']
        ])
        ress=' + '.join([
        	   locale.itemlocale(res[0],data.data)[0]+', '+numtostr(res[1])
        	   for res in
        	   n[x]['results']
        ])
        recipestr=ings+' > '+ress
        #util.pj(ings+' > '+ress)
        info[prefix+'recipe'+postfix]=recipestr
    techs=process.unlockedby.get(recipe,[])
    info['required-technologies']=' + '.join(techs)
    return info

def toinfobox(info):
    info['producers']=' + '.join(sorted(set(info['producers'])))
    s='{{Infobox SE'
    for key in info:
        s+='\n|'
        s+=key
        s+='='
        val=info[key]
        if type(val)!=str:
            val=' + '.join(val)
        s+=val
    s+='\n}}'
    return s

#util.pj([x for x in data.data['recipe'].keys() if 'simu' in x])

#util.pj([*process.uses['expensive'].keys()])
#a=towikirecipe('se-simulation-ab')
#util.pj(a)
#util.pj(towikirecipe(['se-simulation-ab','se-simulation-abm'],a))