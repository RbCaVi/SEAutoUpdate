import os
import util
import copy

itemtypes=[
  'item',
  'ammo',
  'capsule',
  'gun',
  'item-with-entity-data',
  'item-with-label',
  'item-with-inventory',
  'blueprint-book',
  'item-with-tags',
  'selection-tool',
  'blueprint',
  'copy-paste-tool',
  'deconstruction-item',
  'upgrade-item',
  'module',
  'rail-planner',
  'spidertron-remote',
  'tool',
  'armor',
  'repair-tool'
]

mods=filter(lambda x:x.is_dir(),os.scandir(os.path.join(util.fdir,'mods')))
locales=[]
for mod in mods:
  if os.path.exists(os.path.join(mod.path,'locale','en')):
    locales+=[x.path for x in os.scandir(os.path.join(mod.path,'locale','en'))]
locales+=[x.path for x in os.scandir(os.path.join(util.fdir,'data','core','locale','en'))]
locales+=[x.path for x in os.scandir(os.path.join(util.fdir,'data','base','locale','en'))]
locales=[x for x in locales if x.endswith('.cfg')]
locale={}
for file in locales:
  with open(file) as f:
    data=f.read()
  
  category=None
  for line in data.split('\n'):
    if line.strip()=='' or line.startswith(';') or line.startswith('#'):
      continue
    if line.startswith('[') and line.endswith(']'):
      category=line[1:-1]
    else:
      key,value=line.split('=',maxsplit=1)
      if category is None:
        locale[key]=value
      else:
        locale[category+'.'+key]=value

def localize(s):
  return locale.get(s)

def recipelocale(recipe,data):
  recipe=data['recipe'][recipe]
  return recipelocaleraw(recipe)

def recipelocaleraw(recipe):
  if 'normal' in recipe:
    recipe=copy.deepcopy(recipe)
    recipe.update(recipe['normal'])
    del recipe['normal']
    return recipelocaleraw(recipe)
  if len(recipe['results'])==1:
    if 'main_product' in recipe and recipe['main_product']=='':
      if 'localized_description' not in recipe:
        desc=localize('recipe-description.'+recipe['name'])
      else:
        desc=localize(recipe['localized_description'])
      if 'localized_name' not in recipe:
        name=localize('recipe-name.'+recipe['name'])
      else:
        name=localize(recipe['localized_name'])
      return name,desc
    return itemlocale(recipe['results'][0]['name'],data)
  if 'main_product' in recipe:
    return itemlocale(recipe['main_product'],data)
  if 'localized_description' not in recipe:
    desc=localize('recipe-description.'+recipe['name'])
  else:
    desc=localize(recipe['localized_description'])
  if 'localized_name' not in recipe:
    name=localize('recipe-name.'+recipe['name'])
  else:
    name=localize(recipe['localized_name'])
  return name,desc

def itemlocale(item,data):
  for itype in itemtypes:
    if item in data[itype]:
      item=data[itype][item]
      if 'localized_description' not in item:
        desc=localize('item-description.'+item['name'])
      else:
        desc=localize(item['localized_description'])
      if 'localized_name' not in item:
        name=localize('item-name.'+item['name'])
      else:
        name=localize(item['localized_name'])
      return name,desc

def fluidlocale(fluid,data):
  fluid=data['fluid'][fluid]
  if 'localized_description' not in fluid:
    desc=localize('fluid-description.'+fluid['name'])
  else:
    desc=localize(fluid['localized_description'])
  if 'localized_name' not in item:
    name=localize('fluid-name.'+fluid['name'])
  else:
    name=localize(fluid['localized_name'])
  return name,desc
