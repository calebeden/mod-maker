'''
Created on May 1, 2020

@author: calebeden
'''

from os import mkdir, walk, sep, rename, chdir
from os.path import join
from shutil import copy, rmtree
from PIL import Image, ImageOps
from zipfile import ZipFile
import json

global heads, people, microblocks, mobs, template_entity_json, person_text, person_egg_text,\
 microblock_text, microblock_egg_text, mob_text, mob_egg_text, item_texture_json_start,\
 item_texture_json_template, item_texture_json_end, item_texture_json_list, entity_behavior, loot_table,\
 customs, custom_test, custom_egg_test
 
heads = []
mobs = []
mob_text = "entity.playerhead:lower.name=template Head"
mob_egg_text = "item.spawn_egg.entity.playerhead:lower.name=template Head"
item_texture = {"resource_pack_name": "playerheads", "texture_name": "atlas.items", "texture_data": {}}
template_loot_table = {"pools": [{"rolls":1, "entries":[{"type": "item", "name":"minecraft:spawn_egg", "weight":1,\
    "functions":[{"function":"minecraft:set_actor_id"}]}]}]}

if __name__ == '__main__':
    #try to remove the previous pack
    try:
        rmtree('in_progress')
    except:
        pass
    try:
        rmtree('Mob Heads Addon')
    except:
        pass
    
    #create or copy the necessary folders and files
    mkdir('in_progress')
    mkdir('in_progress/resource_pack')
    mkdir('in_progress/resource_pack/entity')
    mkdir('in_progress/resource_pack/entity/playerheads')
    mkdir('in_progress/resource_pack/models')
    mkdir('in_progress/resource_pack/models/entity')
    copy('template/resource_pack/models/entity/playerhead.json','in_progress/resource_pack/models/entity/playerhead.json')
    mkdir('in_progress/resource_pack/texts')
    mkdir('in_progress/resource_pack/textures')
    mkdir('in_progress/resource_pack/textures/items')
    mkdir('in_progress/resource_pack/textures/items/playerheads')
    mkdir('in_progress/resource_pack/textures/entity')
    mkdir('in_progress/resource_pack/textures/entity/playerheads')
    copy('template/resource_pack/manifest.json', 'in_progress/resource_pack/manifest.json')
    copy('template/resource_pack/pack_icon.png', 'in_progress/resource_pack/pack_icon.png')
    
    mkdir('in_progress/behavior_pack')
    mkdir('in_progress/behavior_pack/entities')
    mkdir('in_progress/behavior_pack/entities/playerheads')
    mkdir('in_progress/behavior_pack/loot_tables')
    mkdir('in_progress/behavior_pack/loot_tables/entities')
    mkdir('in_progress/behavior_pack/loot_tables/entities/playerheads')
    copy('template/behavior_pack/manifest.json', 'in_progress/behavior_pack/manifest.json')
    copy('template/behavior_pack/pack_icon.png', 'in_progress/behavior_pack/pack_icon.png')
    
    #Get a list of all the person, microblock, mob, and custom skins; one list for each category as well as the overall heads list
    for subdir, dirs, files in walk('skins/mobs'):
        for filename in files:
            filepath = subdir + sep + filename
            if filename[-4:] == '.png':
                head = filename[:-4]
                #print(head)
                heads.append(head)
                mobs.append(head)
            
    #loop through all listed heads
    for head in heads:
        print(head.title().replace('_',' '))
        #first create textures through resource pack
        #create .entity.json file
        with open('template/resource_pack/entity/playerheads/template.entity.json','r') as infile:
            with open('in_progress/resource_pack/entity/playerheads/' + head + '.entity.json', 'w') as outfile:
                entity_json = json.load(infile)
                entity_json['minecraft:client_entity']['description']['identifier'] = "playerhead:" + head
                entity_json['minecraft:client_entity']['description']['textures'] = {'default': 'textures/entity/playerheads/' + head}
                entity_json['minecraft:client_entity']['description']['spawn_egg']['texture'] = 'spawn_' + head
                json.dump(entity_json, outfile)
        #add to language file while locating the texture to copy
        with open('in_progress/resource_pack/texts/en_US.lang', 'a') as outfile:
            if head in mobs:
                #jeb_ sheep is an exception because it has an underscore
                if head == 'jeb_sheep':
                    copy('skins/mobs/jeb_sheep.png','in_progress/resource_pack/textures/entity/playerheads/jeb_sheep.png')
                    outfile.write(mob_text.replace('lower','jeb_sheep').replace('template', 'jeb_ Sheep') + '\n')
                    outfile.write(mob_egg_text.replace('lower','jeb_sheep').replace('template', 'jeb_ Sheep') + '\n\n')
                else:
                    copy('skins/mobs/' + head + '.png','in_progress/resource_pack/textures/entity/playerheads/' + head + '.png')
                    outfile.write(mob_text.replace('template', head.title().replace('_',' ')).replace('lower', head.lower()).replace('Of', 'of').replace('And', 'and') + '\n')
                    outfile.write(mob_egg_text.replace('template', head.title().replace('_',' ')).replace('lower', head.lower()).replace('Of', 'of').replace('And', 'and') + '\n\n')
        #create spawn egg texture
        image = Image.open('in_progress/resource_pack/textures/entity/playerheads/' + head + '.png')
        base_layer = image.crop((8, 8, 16, 16))
        outer_layer = image.crop((40, 8, 48, 16))
        composite = Image.alpha_composite(base_layer, outer_layer)
        egg_texture = ImageOps.expand(composite, 4)
        egg_texture.save('in_progress/resource_pack/textures/items/playerheads/' + head + '.png')
        #add spawn egg texture to item_texture.json list
        item_texture['texture_data']['spawn_' + head] = {'textures': 'textures/items/playerheads/' + head + '.png'}
        
        #then add basic functionality through the bahavior pack
        with open('template/behavior_pack/entities/playerheads/template.json','r') as infile:
            with open('in_progress/behavior_pack/entities/playerheads/' + head + '.json', 'w') as outfile:
                entity_behavior = json.load(infile)
                entity_behavior['minecraft:entity']['description']['identifier'] = 'playerhead:' + head
                entity_behavior['minecraft:entity']['components']['minecraft:identifier'] = 'playerhead:' + head
                entity_behavior['minecraft:entity']['components']['minecraft:loot']['table'] = 'loot_tables/entities/playerheads/' + head + '.json'
                json.dump(entity_behavior, outfile)
        #and add the loot table
        with open('template/behavior_pack/loot_tables/entities/playerheads/template.json','r') as infile:
            with open('in_progress/behavior_pack/loot_tables/entities/playerheads/' + head + '.json', 'w') as outfile:
                loot_table = json.load(infile)
                loot_table['pools'][0]['entries'][0]['functions'][0]['id'] = 'playerhead:' + head
                json.dump(loot_table, outfile)
    #now that we have iterated through every head, they are all stored in item_texture, which we can now save as a json file
    with open('in_progress/resource_pack/textures/item_texture.json', 'w') as outfile:
        json.dump(item_texture, outfile)
    
    
    #since we are done working, we can rename the folder so that it shows the proper name when extracted as well as the original will be where it needs to go
    rename('in_progress','Mob Heads Addon')
    chdir('Mob Heads Addon')
    rename('behavior_pack','mobheads_b')
    '''with ZipFile('mobheads_b.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('mobheads_b'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)'''
    rename('resource_pack','mobheads_r')
    with ZipFile('mobheads_r.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('mobheads_r'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
    '''with ZipFile('playerheads.mcaddon', 'w') as archive:
        for subdir, dirs, files in walk('playerheads_b'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
        for subdir, dirs, files in walk('playerheads_r'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)'''
    
    print("\
\nThe resource and behavior packs have been created. Now, you can add them to\n\
the mob, wandering trader, and chest loot tables.")

    print("\n\n\
Plan for forward compatibility:\n\
1. When either player heads or custom block models are released, change the loot tables so that they\n\
provide the new item. Add a crafting recipe for people to manually convert to the new format.\n\
2. Create a function or command that people can run which would setblock at the entities and then kill\n\
the entities and their drops (or just remove the drops if I take this option).\n\
3. If I publish this outside just the friend group, DO NOT drop support for the entities in ANY future\n\
version, just in case someone doesn\'t update the pack.\
")



