import os
import util
import copy
import data

if util.devel:
  locales=[os.path.join(util.fdir,'locale.txt')]
else:
  # TODO: handle zipped mods
  mods=filter(lambda x:x.is_dir(),os.scandir(os.path.join(util.fdir,'mods')))
  locales=[]
  for mod in mods:
    if os.path.exists(os.path.join(mod.path,'locale','en')):
      locales+=[x.path for x in os.scandir(os.path.join(mod.path,'locale','en'))]
  # get the core and base locales as well
  locales+=[x.path for x in os.scandir(os.path.join(util.fdir,'data','core','locale','en'))]
  locales+=[x.path for x in os.scandir(os.path.join(util.fdir,'data','base','locale','en'))]
  locales=[x for x in locales if x.endswith('.cfg')] # not sure if this is needed

locale={}
for file in locales:
  with open(file) as f:
    fdata=f.read()

  category=None # i don't know how to handle locale entries without a category
  for line in fdata.split('\n'):
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
  # TODO: handle localizing lists
  return locale.get(s)

def recipelocale(recipe,data=data.data):
  # get the locale for a recipe
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

def itemlocale(item,data=data.data):
  # get the locale for an item or fluid
  if item=='time':
    return 'Time','Time'
  for itype in util.itemtypes:
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
  return fluidlocale(item,data)

def fluidlocale(fluid,data=data.data):
  # get the locale for a fluid
  fluid=data['fluid'][fluid]
  if 'localized_description' not in fluid:
    desc=localize('fluid-description.'+fluid['name'])
  else:
    desc=localize(fluid['localized_description'])
  if 'localized_name' not in fluid:
    name=localize('fluid-name.'+fluid['name'])
  else:
    name=localize(fluid['localized_name'])
  return name,desc

def techlocale(tech,data):
    # get the locale for a technology
    name=tech
    tech=data['technology'][tech]
    try:
        int(name.split('-',maxsplit=1)[1])
        name=name.split('-',maxsplit=1)[0]
    except:
        pass
    if 'localized_description' not in tech:
        desc=localize('technology-description.'+name)
    else:
        desc=localize(tech['localized_description'])
    if 'localized_name' not in tech:
        name=localize('technology-name.'+name)
    else:
        name=localize(tech['localized_name'])
    return name,desc


del f,fdata,line,locales
