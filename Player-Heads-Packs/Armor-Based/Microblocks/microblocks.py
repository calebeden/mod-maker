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

global heads, people, microblocks, customs, farm_products, person_text, microblock_text, custom_text, item_texture_json

heads = []
people = []
microblocks = []
customs = []
farm_products = []
person_text = "item.playerhead:lower.name=template's Head"
microblock_text = "item.playerhead:lower.name=Micro-template"
custom_text = "item.playerhead:lower.name=template"
item_texture_json = {"resource_pack_name": "playerheads", "texture_name": "atlas.items", "texture_data": {}}

if __name__ == '__main__':
    #try to remove the previous pack
    try:
        rmtree('in_progress')
    except:
        pass
    try:
        rmtree('Microblocks Addon')
    except:
        pass

    #create or copy the necessary folders and files
    mkdir('in_progress')
    mkdir('in_progress/resource_pack')
    mkdir('in_progress/resource_pack/attachables')
    mkdir('in_progress/resource_pack/attachables/render')
    mkdir('in_progress/resource_pack/texts')
    mkdir('in_progress/resource_pack/textures')
    mkdir('in_progress/resource_pack/textures/items')
    mkdir('in_progress/resource_pack/textures/models')
    mkdir('in_progress/resource_pack/textures/models/heads')
    copy('template/resource_pack/manifest.json', 'in_progress/resource_pack/manifest.json')
    copy('template/resource_pack/pack_icon.png', 'in_progress/resource_pack/pack_icon.png')

    mkdir('in_progress/behavior_pack')
    mkdir('in_progress/behavior_pack/items')
    mkdir('in_progress/behavior_pack/loot_tables')
    mkdir('in_progress/behavior_pack/loot_tables/entities')
    copy('template/behavior_pack/manifest.json', 'in_progress/behavior_pack/manifest.json')
    copy('template/behavior_pack/pack_icon.png', 'in_progress/behavior_pack/pack_icon.png')

    #Get a list of all the person, microblock, mob, and custom skins; one list for each category as well as the overall heads list
    for subdir, dirs, files in walk('skins/people'):
        for filename in files:
            filepath = subdir + sep + filename
            if filename[-4:] == '.png':
                head = filename[:-4]
                #print(head)
                heads.append(head)
                people.append(head)
    for subdir, dirs, files in walk('skins/microblocks'):
        for filename in files:
            filepath = subdir + sep + filename
            if filename[-4:] == '.png':
                head = filename[:-4]
                #print(head)
                heads.append(head)
                microblocks.append(head)
    for subdir, dirs, files in walk('skins/custom'):
        for filename in files:
            filepath = subdir + sep + filename
            if filename[-4:] == '.png':
                head = filename[:-4]
                #print(head)
                heads.append(head)
                customs.append(head)
    for subdir, dirs, files in walk('skins/farm_products'):
        for filename in files:
            filepath = subdir + sep + filename
            if filename[-4:] == '.png':
                head = filename[:-4]
                #print(head)
                heads.append(head)
                farm_products.append(head)

    #loop through all listed heads
    for head in heads:
        print(head.title().replace('_',' '))
        #first create textures through resource pack
        #create json files to define materials
        with open('template/resource_pack/attachables/template.json','r') as infile:
            with open('in_progress/resource_pack/attachables/' + head + '.json', 'w') as outfile:
                item_json = json.load(infile)
                item_json['minecraft:attachable']['description']['identifier'] = "playerhead:" + head
                item_json['minecraft:attachable']['description']['textures']['default'] = 'textures/models/heads/' + head
                json.dump(item_json, outfile)
        with open('template/resource_pack/attachables/render/template.player.json','r') as infile:
            with open('in_progress/resource_pack/attachables/render/' + head + '.player.json', 'w') as outfile:
                armor_json = json.load(infile)
                armor_json['minecraft:attachable']['description']['identifier'] = "playerhead:" + head + ".player"
                armor_json['minecraft:attachable']['description']['item'] = {"playerhead:" + head: "query.owner_identifier == 'minecraft:player'"}
                armor_json['minecraft:attachable']['description']['textures']['default'] = 'textures/models/heads/' + head
                json.dump(armor_json, outfile)
        #add to language file while copying the texture
        with open('in_progress/resource_pack/texts/en_US.lang', 'a') as outfile:
            if head in people:
                copy('skins/people/' + head + '.png','in_progress/resource_pack/textures/models/heads/' + head + '.png')
                outfile.write(person_text.replace('template', head.title().replace('_',' ')).replace('lower', head.lower()).replace('Of ', 'of').replace('And ', 'and') + '\n')
            if head in microblocks:
                #TNT is an exception because it is all caps
                if head == 'tnt':
                    copy('skins/microblocks/tnt.png','in_progress/resource_pack/textures/models/heads/tnt.png')
                    outfile.write(microblock_text.replace('lower','tnt').replace('template', 'TNT') + '\n')
                #Jack o'Lantern is an exception because it has a capital in the middle of a word
                if head == 'jack_olantern':
                    copy('skins/microblocks/jack_olantern.png','in_progress/resource_pack/textures/models/heads/jack_olantern.png')
                    outfile.write(microblock_text.replace('lower','jack_olantern').replace('template', "Jack o'Lantern") + '\n')
                else:
                    copy('skins/microblocks/' + head + '.png','in_progress/resource_pack/textures/models/heads/' + head + '.png')
                    outfile.write(microblock_text.replace('template', head.title().replace('_',' ')).replace('lower', head.lower()).replace('Of', 'of').replace('And ', 'and ') + '\n')
            if head in customs:
                copy('skins/custom/' + head + '.png','in_progress/resource_pack/textures/models/heads/' + head + '.png')
                outfile.write(custom_text.replace('template', head.title().replace('_',' ')).replace('lower', head.lower()).replace('Of', 'of').replace('And', 'and') + '\n')
            if head in farm_products:
                copy('skins/farm_products/' + head + '.png','in_progress/resource_pack/textures/models/heads/' + head + '.png')
                outfile.write(custom_text.replace('template', head.title().replace('_',' ')).replace('lower', head.lower()).replace('Of', 'of').replace('And', 'and') + '\n')
        #create item texture
        image = Image.open('in_progress/resource_pack/textures/models/heads/' + head + '.png')
        base_layer = image.crop((8, 8, 16, 16))
        outer_layer = image.crop((40, 8, 48, 16))
        composite = Image.alpha_composite(base_layer, outer_layer)
        item_texture = ImageOps.expand(composite, 4)
        item_texture.save('in_progress/resource_pack/textures/items/' + head + '.png')
        #add item texture to item_texture.json list
        item_texture_json['texture_data']['playerhead:' + head] = {'textures': 'textures/items/' + head + '.png'}

        #then add basic functionality through the behavior pack
        with open('template/behavior_pack/items/template.json','r') as infile:
            with open('in_progress/behavior_pack/items/' + head + '.json', 'w') as outfile:
                item_behavior = json.load(infile)
                item_behavior['minecraft:item']['description']['identifier'] = 'playerhead:' + head
                item_behavior['minecraft:item']['components']['minecraft:icon']['texture'] = 'playerhead:' + head
                item_behavior['minecraft:item']['components']['minecraft:display_name']['value'] = head
                json.dump(item_behavior, outfile)
    #now that we have iterated through every head, they are all stored in item_texture, which we can now save as a json file
    with open('in_progress/resource_pack/textures/item_texture.json', 'w') as outfile:
        json.dump(item_texture_json, outfile)


    #since we are done working, we can rename the folder so that it shows the proper name when extracted as well as the original will be where it needs to go
    rename('in_progress','Microblocks Addon')
    chdir('Microblocks Addon') #change cwd
    rename('behavior_pack','microblocks_b')
    '''with ZipFile('microblocks_b.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('microblocks_b'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)'''
    rename('resource_pack','microblocks_r')
    with ZipFile('microblocks_r.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('microblocks_r'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
    '''with ZipFile('microblocks.mcaddon', 'w') as archive:
        for subdir, dirs, files in walk('microblocks_b'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
        for subdir, dirs, files in walk('microblocks_r'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)'''

    print("\
\nThe resource and behavior packs have been created. Now, you can add them to\n\
wandering trader trade table.")

    print("\n\n\
Plan for pack readiness:\n\
1. Bug test and fix all issues.\n\
2. See if custom blocks (models) are still considered experimental. If they are, go with\n\
the temporary armor stand-like idea. If not, then go ahead and prepare the custom blocks now.\n\
3. Send to friends to test. If everything goes good, add to the realm.\n\
(Alternatively wait for custom armor to exit experimental gameplay to ensure more stability)\
")
