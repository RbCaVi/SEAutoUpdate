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

order=[
    'burner-assembling-machine',
    'assembling-machine-1',
    'assembling-machine-2',
    'assembling-machine-3',
    'se-space-assembling-machine',
    'se-space-manufactory',
    'se-space-supercomputer-1',
    'se-space-supercomputer-2',
    'se-space-supercomputer-3',
    'se-space-supercomputer-4',
    'se-nexus',
    'se-space-astrometrics-laboratory',
    'se-space-biochemical-laboratory',
    'se-space-electromagnetics-laboratory',
    'se-space-genetics-laboratory',
    'se-space-gravimetrics-laboratory',
    'se-space-laser-laboratory',
    'se-space-material-fabricator',
    'se-space-mechanical-laboratory',
    'se-space-radiation-laboratory',
    'se-space-thermodynamics-laboratory',
    'se-space-particle-accelerator',
    'se-space-particle-collider',
    'se-space-decontamination-facility',
    'se-space-radiator',
    'se-space-radiator-2',
    'se-space-hypercooler',
    'se-space-telescope',
]
[
    'character',
    'character-jetpack',
    
]

def reorder(l):
    newl=[]
    for i in l:
        if i not in order:
            with open('/storage/emulated/0/Documents/pydroid3/seauto/unordered.txt','a') as f:
                f.write(i)
                f.write('\n')
        i=i.replace('-grounded','')
        if 'telescope' in i:
            i='se-space-telescope'
        if 'character' in i:
            i='character'
        newl.append(i)
    l=newl
    return [i for _,i in sorted([((order+[i]).index(i),i) for i in l])]

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
    util.pj(tech)
    if info is None:
        info=copy.deepcopy(defaulttinfo)
    else:
        info=copy.deepcopy(info)
    n=data.pdata['technology'][tech]
    info['allows']=[*set(map(locale.techname,process.postreqs['normal'][tech]))]
    info['effects']=[*map(locale.recipename,process.unlocks['normal'][tech])]
    info['required-technologies']=[*map(locale.techname,process.prereqs['normal'][tech])]
    info['cost-multiplier']=n['normal']['count']
    if 'expensive' in info:
        info['expensive-cost-multiplier']=n['expensive']['count']
    info['cost']=' + '.join([
        	   locale.itemlocale(pack[0],data.data)[0]+','+numtostr(pack[1])
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
    info['consumers']=[*map(locale.recipename,process.uses['normal'].get(item,[]))]
    return info

def towikifluid(fluid,group,info=None):
    if info is None:
        info=copy.deepcopy(defaultrinfo)
    else:
        info=copy.deepcopy(info)
    proto=process.getitem(fluid)
    util.pj(proto)
    info['category']=group
    info['internal-name']=fluid
    return info

def towikirecipe(recipe,info=None,replace=None):
    if info is None:
        info=copy.deepcopy(defaultrinfo)
    else:
        info=copy.deepcopy(info)
    if type(recipe)==list or type(recipe)==tuple:
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
    info['producers']+=process.madein[n['category']]
    for x in util.difficulty:
        if x not in n:
            continue
        prefix=diff_prefixes[x]
        ings=' + '.join([
        	   locale.itemlocale(ing[0],data.data)[0]+','+numtostr(ing[1])
        	   for ing in
        	   [['time',n[x]['time'],'time']]+n[x]['ingredients']
        ])
        ress=' + '.join([
        	   locale.itemlocale(res[0],data.data)[0]+','+numtostr(res[1])
        	   for res in
        	   n[x]['results']
        ])
        recipestr=ings+' > '+ress
        info[prefix+'recipe'+postfix]=recipestr
    print(recipe)
    techs=process.unlockedby['normal'].get(recipe,[])
    info['required-technologies']=[*map(locale.techname,techs)]
    return info

def toinfobox(info):
    if 'producers' in info:
      print(info['producers'])
      info['producers']=' + '.join(map(locale.entityname,reorder(set(info['producers']))))
    s='{{Infobox SE'
    for key in info:
        s+='\n|'
        s+=key
        s+='='
        val=info[key]
        if type(val)==int:
            val=str(val)
        elif type(val)!=str:
            print(val)
            val=' + '.join(val)
        s+=val
    s+='\n}}'
    return s

#util.pj([x for x in data.data['recipe'].keys() if 'simu' in x])

#util.pj([*process.uses['expensive'].keys()])
#a=towikirecipe('se-simulation-ab')
#util.pj(a)
#util.pj(towikirecipe(['se-simulation-ab','se-simulation-abm'],a))