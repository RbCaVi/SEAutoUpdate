import copy

def move(d1,d2,i):
    # move the key i (if it exists) and its value from d1 to d2
    if i in d1:
        d2[i]=d1[i]
        del d1[i]

def fixrecipe(recipe,root=True):
    # normalize a recipe to the form:
    # no difficulty-specific properties in the top level
    # all in normal (and expensive if used)
    # all ingredients and results are in the full form
    recipe=copy.deepcopy(recipe) # don't modify the original recipe
    if 'normal' in recipe:
        recipe['normal']=fixrecipe(recipe['normal'],False)
        if 'expensive' not in recipe:
            return recipe
    if 'expensive' in recipe:
        recipe['expensive']=fixrecipe(recipe['expensive'],False)
        if 'normal' not in recipe or not recipe['normal']: # if normal is not defined, but expensive is, set normal to expensive
            recipe['normal']=recipe['expensive']
            del recipe['expensive']
        return recipe
    recipe['ingredients']=[*map(fixingredient,recipe['ingredients'])] # fix all the ingredients
    if 'result' in recipe and 'results' not in recipe: # move result to results
        if 'result_count' not in recipe:
            recipe['result_count']=1
        recipe['results']=[[recipe['result'],recipe['result_count']]]
    recipe['results']=[*map(fixresult,recipe['results'])] # fix the results
    recipe['energy_required']=recipe.get('energy_required',0.5)
    if not root:
        return recipe
    # move all the difficulty-specific settings to normal
    recipe['normal']={}
    move(recipe,recipe['normal'],'results')
    move(recipe,recipe['normal'],'result')
    move(recipe,recipe['normal'],'result_count')
    move(recipe,recipe['normal'],'ingredients')
    move(recipe,recipe['normal'],'energy_required')
    move(recipe,recipe['normal'],'emissions_multiplier')
    move(recipe,recipe['normal'],'requester_paste_multiplier')
    move(recipe,recipe['normal'],'overload_multiplier')
    move(recipe,recipe['normal'],'allow_inserter_overload')
    move(recipe,recipe['normal'],'enabled')
    move(recipe,recipe['normal'],'hidden')
    move(recipe,recipe['normal'],'hide_from_stats')
    move(recipe,recipe['normal'],'hide_from_player_crafting')
    move(recipe,recipe['normal'],'allow_decomposition')
    move(recipe,recipe['normal'],'allow_as_intermediate')
    move(recipe,recipe['normal'],'allow_intermediates')
    move(recipe,recipe['normal'],'always_show_made_in')
    move(recipe,recipe['normal'],'show_amount_in_title')
    move(recipe,recipe['normal'],'always_show_products')
    move(recipe,recipe['normal'],'unlock_results')
    move(recipe,recipe['normal'],'main_product')
    return recipe

def fixingredient(ingredient):
    # fix one ingredient to the table form
    if type(ingredient)==list:
        return {'type':'item','name':ingredient[0],'amount':ingredient[1]}
    return ingredient

def fixresult(result):
    # fix one result to the table form
    # the amount_min and amount_max are put into amount
    if type(result)==list:
        result={'type':'item','name':result[0],'amount':result[1]}
    if 'amount_min' in result and 'amount' not in result:
        if 'probability' not in result:
            result['probability']=1
        result['amount']=result['probability']*(0.5*(result['amount_min']+result['amount_max']))
    if 'type' not in result:
        result['type']='item'
    return result

def fixtech(tech,root=True):
    tech=copy.deepcopy(tech)
    if 'normal' in tech:
        tech['normal']=fixtech(tech['normal'],False)
        if 'expensive' not in tech:
            return tech
    if 'expensive' in tech:
        tech['expensive']=fixtech(tech['expensive'],False)
        if 'normal' not in tech or not tech['normal']:
            tech['normal']=tech['expensive']
            del tech['expensive']
        return tech
    if not root:
        return tech
    tech['unit']['ingredients']=[*map(fixingredient,tech['unit']['ingredients'])]
    tech['normal']={}
    move(tech,tech['normal'],'upgrade')
    move(tech,tech['normal'],'enabled')
    move(tech,tech['normal'],'hidden')
    move(tech,tech['normal'],'visible_when_disabled')
    move(tech,tech['normal'],'ignore_tech_cost_multiplier')
    move(tech,tech['normal'],'unit')
    move(tech,tech['normal'],'max_level')
    move(tech,tech['normal'],'prerequisites')
    move(tech,tech['normal'],'effects')
    return tech
