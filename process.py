import data
import util

def getitemtype(item):
    for itype in ['fluid']+util.itemtypes:
        if item in data.data[itype]:
            return itype

def processrecipe(recipe):
    recipe=data.data['recipe'][recipe]
    new={}
    for x in ['normal','expensive']:
        if x not in recipe:
            continue
        new[x]={'ingredients':[],'results':[]}
        for ingredient in recipe[x]['ingredients']:
            new[x]['ingredients'].append((
                ingredient['name'],
                ingredient['amount'],
                getitemtype(ingredient['name'])
                #ingredient['type']
            ))
        for result in recipe[x]['results']:
            new[x]['results'].append((
                result['name'],
                result['amount'],
                getitemtype(result['name'])
                #result['type']
            ))
        new[x]['time']=recipe[x]['energy_required']
    new['name']=recipe['name']
    return new

def processtech(tech):
    tech=data.data['technology'][tech]
    new={}
    new['name']=tech['name']
    for x in util.difficulty:
        if x not in tech:
            continue
        new[x]={'packs':[]}
        for pack in tech[x]['unit']['ingredients']:
            new[x]['packs'].append((
                pack['name'],
                pack['amount']
            ))
        if 'count' in tech[x]['unit']:
            new[x]['count']=tech[x]['unit']['count']
        else:
            new[x]['count']=tech[x]['unit']['count_formula']
        new[x]['time']=tech[x]['unit']['time']
        new[x]['prerequisites']=tech[x].get('prerequisites',{})
        try:
            effects=tech[x].get('effects',{})
            if type(effects)==dict:
                effects=effects.values()
            new[x]['effects']=[e['recipe'] for e in effects if e['type']=='unlock-recipe']
        except Exception as e:
            print(tech)
            raise e
    return new

def init():
	global uses,produces
	global prereqs,postreqs,unlocks
	uses={x:{} for x in util.difficulty}
	produces={x:{} for x in util.difficulty}

	for recipe in [processrecipe(r) for r in data.data['recipe']]:
	    for x in util.difficulty:
	        if x not in recipe:
	            continue
	        for ing in recipe[x]['ingredients']:
	            if ing[0::2] not in uses[x]:
	                uses[x][ing[0::2]]=[]
	            uses[x][ing[0::2]].append(recipe['name'])
	        for res in recipe[x]['results']:
	            if res[0::2] not in produces[x]:
	                produces[x][res[0::2]]=[]
	            produces[x][res[0::2]].append(recipe['name'])

	prereqs={x:{} for x in util.difficulty}
	postreqs={x:{} for x in util.difficulty}
	unlocks={x:{} for x in util.difficulty}

	for tech in [processtech(t) for t in data.data['technology']]:
	    for x in util.difficulty:
	        if x not in tech:
	            continue
	        for prereq in tech[x]['prerequisites']:
	            if prereq[0::2] not in postreqs[x]:
	                postreqs[x][prereq]=[]
	            postreqs[x][prereq].append(tech['name'])
	            if tech['name'] not in prereqs[x]:
	                prereqs[x][tech['name']]=[]
	            prereqs[x][tech['name']].append(prereq)
	        for effect in tech[x]['effects']:
	            if tech['name'] not in unlocks[x]:
	                unlocks[x][tech['name']]=[]
	            unlocks[x][tech['name']].append(effect)