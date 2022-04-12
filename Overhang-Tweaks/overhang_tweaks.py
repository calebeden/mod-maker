'''
Created on Apr 24, 2020

@author: calebeden
'''

from os import mkdir, rename, walk, path, remove
from os.path import basename, join, isdir
from shutil import copy, rmtree, copytree
from PIL import Image
from zipfile import ZipFile
import json
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import Tk, mainloop, Menu, Frame
from caleb.caleb import inp_int

def pack_setup(preferences_json, preferences_location):
    #remove the previously created pack, if it exists
    try:
        rmtree('completed_packs/' + preferences_json['name'] + '/Overhang Tweaks ' + preferences_json['name'].title() + ' ' + '.'.join([str(preferences_json['version'][0]), str(preferences_json['version'][1]), str(preferences_json['version'][2])]))
    except:
        pass
    try:
        remove('completed_packs/' + preferences_json['name'] + '/overhangtweaks_' + preferences_json['name'] + '_' + '.'.join([str(preferences_json['version'][0]), str(preferences_json['version'][1]), str(preferences_json['version'][2])]) + '.mcpack')
    except:
        pass
    try:
        rmtree('Overhang Tweaks')
    except:
        pass
    try:
        rmtree('in_progress')
    except:
        pass
    
    #create a new work in progress pack with folders that can be filled later in the process
    mkdir('in_progress')
    mkdir('in_progress/subpacks')
    
    #modify/personalize manifest
    with open('template/manifest.json','r') as template_manifest:
        manifest = json.load(template_manifest)
        with open('preferences/version.json', 'r') as version:
            pack_version = json.load(version)['version']
        #insert the right pack version
        manifest['header']['description'] = preferences_json['name'].title() + "'s Tweaks v " + '.'.join([str(pack_version[0]), str(pack_version[1]), str(pack_version[2])])
        manifest['header']['version'] = pack_version
        manifest['modules'][0]['description'] = preferences_json['name'].title() + "'s Tweaks v " + '.'.join([str(pack_version[0]), str(pack_version[1]), str(pack_version[2])])
        manifest['modules'][0]['version'] = pack_version
        #insert the right subpacks
        for profile in preferences_json['profiles']:
            manifest['subpacks'].append({"folder_name": profile['nickname'].lower(), "name": profile['nickname'].title(), "memory_tier": profile['rank']})
        with open('in_progress/manifest.json', 'w') as outfile:
            json.dump(manifest, outfile)
    
    #copy the pack icon
    copy('template/pack_icon.png', 'in_progress/pack_icon.png')
    
    #we will copy the preferences file just in case we want it for future reference - it won't affect the pack itself
    copy(preferences_location, 'in_progress/preferences.json')

def subpack_setup(preferences_json): #creates the necessary folders and text documents
    #folders to fill with the new copied files
    mkdir(current_subpack + '/texts')
    mkdir(current_subpack + '/models')
    mkdir(current_subpack + '/models/entity')
    mkdir(current_subpack + '/sounds')
    mkdir(current_subpack + '/textures')
    mkdir(current_subpack + '/textures/entity')
    mkdir(current_subpack + '/textures/blocks')
    mkdir(current_subpack + '/textures/ui')
    mkdir(current_subpack + '/textures/gui')
    mkdir(current_subpack + '/textures/items')
    mkdir(current_subpack + '/textures/models')
    mkdir(current_subpack + '/textures/models/armor')
    mkdir(current_subpack + '/textures/environment')
    mkdir(current_subpack + '/textures/particle')
    mkdir(current_subpack + '/textures/misc')
    mkdir(current_subpack + '/textures/colormap')
    
    #change the sleeping message
    with open(current_subpack + '/texts/en_US.lang','a') as outfile:
        outfile.write('resourcePack.subpackResolution=Texture Pack Profile: %s\n')
        outfile.write(open('template/texts/tips.txt').read() + '\n\n')
        outfile.write('chat.type.sleeping=%s §ewent to bed. Sweet Dreams\n')
        outfile.write("howtoplay.beds.text.3=If you are playing Multiplayer, §meveryone in the world must be in a Bed at the same time to pass the night.§r But that doesn't matter because Overhang has one player sleeping enabled!\n\n")
        
    #create sound definitions in case the quieter and less intrusive options are selected
    with open('template/sounds/sound_definitions.json', 'r') as infile:
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(json.load(infile), outfile)
    
    #create blocks.json in case texture names are chnages
    with open('template/blocks.json', 'r') as infile:
        with open(current_subpack + '/blocks.json', 'w') as outfile:
            json.dump(json.load(infile), outfile)
    
    #create terrain_texture.json in case texture names are changed
    with open('template/textures/terrain_texture.json', 'r') as infile:
        with open(current_subpack + '/textures/terrain_texture.json', 'w') as outfile:
            json.dump(json.load(infile), outfile)

def panorama(panorama):
    if panorama == 'overhang':
        for image in range (0,6):
            copy('template/textures/ui/overhang_panorama/panorama_' + str(image) + '.png', current_subpack + '/textures/ui/panorama_' + str(image) + '.png')

def poppied_golem():
    copy('template/textures/entity/iron_golem.png', current_subpack + '/textures/entity/iron_golem.png')

def pebbleless_dirt():
    copy('template/textures/blocks/pebbleless_dirt.png', current_subpack + '/textures/blocks/dirt.png')
def grass(grass, pebbleless_dirt, alpha_foliage):
    if grass == 'normal':
        if pebbleless_dirt:
            copy('template/textures/blocks/terrain_normal/pebbleless/grass_side.tga',current_subpack + '/textures/blocks/grass_side.tga')
            copy('template/textures/blocks/terrain_normal/pebbleless/grass_side_carried.tga',current_subpack + '/textures/blocks/grass_side_carried.tga')
        else:
            pass
            #no need to override global resources
    elif grass == 'lower':
        if pebbleless_dirt:
            copy('template/textures/blocks/terrain_lower/pebbleless/grass_side.tga',current_subpack + '/textures/blocks/grass_side.tga')
            copy('template/textures/blocks/terrain_lower/pebbleless/grass_side_carried.tga',current_subpack + '/textures/blocks/grass_side_carried.tga')
        else:
            copy('template/textures/blocks/terrain_lower/pebbled/grass_side.tga',current_subpack + '/textures/blocks/grass_side.tga')
            copy('template/textures/blocks/terrain_lower/pebbled/grass_side_carried.tga',current_subpack + '/textures/blocks/grass_side_carried.tga')
    elif grass == 'side':
        copy('template/textures/blocks/terrain_side/grass_side.tga',current_subpack + '/textures/blocks/grass_side.tga')
        copy('template/textures/blocks/terrain_side/grass_side_carried.tga',current_subpack + '/textures/blocks/grass_side_carried.tga')
    if alpha_foliage:
        copy('template/textures/blocks/alpha_foliage/grass_carried.png',current_subpack + '/textures/blocks/grass_carried.png')
def mycelium(mycelium, pebbleless_dirt):
    if mycelium == 'normal':
        if pebbleless_dirt:
            copy('template/textures/blocks/terrain_normal/pebbleless/mycelium_side.png',current_subpack + '/textures/blocks/mycelium_side.png')
        else:
            pass
            #no need to override global resources
    elif mycelium == 'lower':
        #the pebbles all get covered by the lowered mycelium so we don't need to check
        copy('template/textures/blocks/terrain_lower/pebbleless/mycelium_side.png',current_subpack + '/textures/blocks/mycelium_side.png')
    elif mycelium == 'side':
        copy('template/textures/blocks/terrain_side/mycelium_side.png',current_subpack + '/textures/blocks/mycelium_side.png')
def path(path, pebbleless_dirt):
    if path == 'normal':
        if pebbleless_dirt:
            copy('template/textures/blocks/terrain_normal/pebbleless/grass_path_side.png',current_subpack + '/textures/blocks/grass_path_side.png')
        else:
            pass
            #no need to override global resources
    elif path == 'lower':
        if pebbleless_dirt:
            copy('template/textures/blocks/terrain_lower/pebbleless/grass_path_side.png',current_subpack + '/textures/blocks/grass_path_side.png')
        else:
            copy('template/textures/blocks/terrain_lower/pebbled/grass_path_side.png',current_subpack + '/textures/blocks/grass_path_side.png')
    elif path == 'side':
        copy('template/textures/blocks/terrain_side/grass_path_side.png',current_subpack + '/textures/blocks/grass_path_side.png')
def podzol(podzol, pebbleless_dirt):
    if podzol == 'normal':
        if pebbleless_dirt:
            copy('template/textures/blocks/terrain_normal/pebbleless/dirt_podzol_side.png',current_subpack + '/textures/blocks/dirt_podzol_side.png')
        else:
            pass
            #no need to override global resources
    elif podzol == 'lower':
        if pebbleless_dirt:
            copy('template/textures/blocks/terrain_lower/pebbleless/dirt_podzol_side.png',current_subpack + '/textures/blocks/dirt_podzol_side.png')
        else:
            copy('template/textures/blocks/terrain_lower/pebbled/dirt_podzol_side.png',current_subpack + '/textures/blocks/dirt_podzol_side.png')
    elif podzol == 'side':
        copy('template/textures/blocks/terrain_side/dirt_podzol_side.png',current_subpack + '/textures/blocks/dirt_podzol_side.png')
def snow(snow, pebbleless_dirt, whiter_snow):
    if whiter_snow:
        copy('template/textures/blocks/terrain_side/whiter_snow.png',current_subpack + '/textures/blocks/snow.png')
        copy('template/textures/items/snowball.png',current_subpack + '/textures/items/snowball.png')
        copy('template/textures/entity/snow_golem.png',current_subpack + '/textures/entity/snow_golem.png')
        if snow == 'normal':
            if pebbleless_dirt:
                copy('template/textures/blocks/terrain_normal/pebbleless/whiter_grass_side_snowed.png',current_subpack + '/textures/blocks/grass_side_snowed.png')
            else:
                pass
                #no need to override global resources
        elif snow == 'lower':
            if pebbleless_dirt:
                copy('template/textures/blocks/terrain_lower/pebbleless/whiter_grass_side_snowed.png',current_subpack + '/textures/blocks/grass_side_snowed.png')
            else:
                copy('template/textures/blocks/terrain_lower/pebbled/whiter_grass_side_snowed.png',current_subpack + '/textures/blocks/grass_side_snowed.png')
        elif snow == 'side':
            copy('template/textures/blocks/terrain_side/whiter_snow.png',current_subpack + '/textures/blocks/grass_side_snowed.png')
    else:
        if snow == 'normal':
            if pebbleless_dirt:
                copy('template/textures/blocks/terrain_normal/pebbleless/grass_side_snowed.png',current_subpack + '/textures/blocks/grass_side_snowed.png')
            else:
                pass
                #no need to override global resources
        elif snow == 'lower':
            if pebbleless_dirt:
                copy('template/textures/blocks/terrain_lower/pebbleless/grass_side_snowed.png',current_subpack + '/textures/blocks/grass_side_snowed.png')
            else:
                copy('template/textures/blocks/terrain_lower/pebbled/grass_side_snowed.png',current_subpack + '/textures/blocks/grass_side_snowed.png')
        elif snow == 'side':
            copy('template/textures/blocks/terrain_side/snow.png',current_subpack + '/textures/blocks/grass_side_snowed.png')

def pebbleless_coarse_dirt():
    copy('template/textures/blocks/coarse_dirt.png',current_subpack + '/textures/blocks/coarse_dirt.png')
   
def visible_wither_hearts():
    copy('template/textures/ui/wither_heart_flash_half.png',current_subpack + '/textures/ui/wither_heart_flash_half.png')
    copy('template/textures/ui/wither_heart_flash.png',current_subpack + '/textures/ui/wither_heart_flash.png')
    copy('template/textures/ui/wither_heart_half.png',current_subpack + '/textures/ui/wither_heart_half.png')
    copy('template/textures/ui/wither_heart.png',current_subpack + '/textures/ui/wither_heart.png')

def hardened_clay():
    with open(current_subpack + '/texts/en_US.lang','a') as outfile:
        outfile.write('howtoplay.blocks.text.7=Hardened Clay - This is found naturally in Mesa biomes or can be crafted and dyed from Clay that is found underwater. Hardened Clay can be made into Glazed Terracotta by smelting it in a Furnace.\n')
        outfile.write('itemGroup.name.stainedClay=Stained Clays\n')
        outfile.write('tile.hardened_clay.name=Hardened Clay\n')
        outfile.write('tile.stained_hardened_clay.black.name=Black Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.blue.name=Blue Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.brown.name=Brown Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.cyan.name=Cyan Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.gray.name=Gray Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.green.name=Green Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.lightBlue.name=Light Blue Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.lime.name=Lime Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.magenta.name=Magenta Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.name=Hardened Clay\n')
        outfile.write('tile.stained_hardened_clay.orange.name=Orange Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.pink.name=Pink Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.purple.name=Purple Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.red.name=Red Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.silver.name=Light Gray Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.white.name=White Stained Clay\n')
        outfile.write('tile.stained_hardened_clay.yellow.name=Yellow Stained Clay\n\n')

def clean_leather_armor():
    copy('template/textures/models/armor/leather_1.tga',current_subpack + '/textures/models/armor/leather_1.tga')
    copy('template/textures/models/armor/leather_2.tga',current_subpack + '/textures/models/armor/leather_2.tga')
    copy('template/textures/items/leather_boots.tga',current_subpack + '/textures/items/leather_boots.tga')
    copy('template/textures/items/leather_helmet.tga',current_subpack + '/textures/items/leather_helmet.tga')
    copy('template/textures/items/leather_leggings.tga',current_subpack + '/textures/items/leather_leggings.tga')

def circle_sun_moon():
    copy('template/textures/environment/moon_phases.png',current_subpack + '/textures/environment/moon_phases.png')
    copy('template/textures/environment/sun.png',current_subpack + '/textures/environment/sun.png')

def newshape_iron_nugget():
    copy('template/textures/items/iron_nugget.png',current_subpack + '/textures/items/iron_nugget.png')

def ores(universal_ores, ore_border, brighter_nether, old_netherrack):
    if ore_border:
        if universal_ores:
            for ore in ['coal', 'diamond', 'emerald', 'gold', 'iron', 'lapis', 'redstone']:
                copy('template/textures/blocks/ores/universal_ore_borders/' + ore + '_ore.png',current_subpack + '/textures/blocks/' + ore + '_ore.png')
            if old_netherrack and not brighter_nether:
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/old_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/old_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
            elif old_netherrack and brighter_nether:
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/bright_ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/bright_ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/old_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/bright_old_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
            elif brighter_nether:
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/bright_ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/bright_ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/bright_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/bright_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
            else:
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal_ore_borders/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
        else:
            for ore in ['coal', 'diamond', 'emerald', 'gold', 'iron', 'lapis', 'redstone']:
                copy('template/textures/blocks/ores/ore_borders/' + ore + '_ore.png',current_subpack + '/textures/blocks/' + ore + '_ore.png')
            if old_netherrack and not brighter_nether:
                copy('template/textures/blocks/ores/nether_ores/ore_borders/ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/old_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/old_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
            elif old_netherrack and brighter_nether:
                copy('template/textures/blocks/ores/nether_ores/ore_borders/ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/old_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/old_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
            elif brighter_nether:
                copy('template/textures/blocks/ores/nether_ores/ore_borders/ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/bright_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/bright_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
            else:
                copy('template/textures/blocks/ores/nether_ores/ore_borders/ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/ore_borders/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
    else:
        if universal_ores:
            copy('template/textures/blocks/ores/universal/emerald_ore.png',current_subpack + '/textures/blocks/emerald_ore.png')
            copy('template/textures/blocks/ores/universal/lapis_ore.png',current_subpack + '/textures/blocks/lapis_ore.png')
            if old_netherrack and not brighter_nether:
                copy('template/textures/blocks/ores/nether_ores/universal/ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/universal/ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/universal/old_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal/old_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
            elif old_netherrack and brighter_nether:
                copy('template/textures/blocks/ores/nether_ores/universal/bright_ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/universal/bright_ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/universal/old_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal/bright_old_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
            elif brighter_nether:
                copy('template/textures/blocks/ores/nether_ores/universal/bright_ancient_debris_side.png',current_subpack + '/textures/blocks/ancient_debris_side.png')
                copy('template/textures/blocks/ores/nether_ores/universal/bright_ancient_debris_top.png',current_subpack + '/textures/blocks/ancient_debris_top.png')
                copy('template/textures/blocks/ores/nether_ores/universal/bright_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal/bright_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
                copy('template/textures/blocks/ores/nether_ores/universal/gilded_blackstone.png',current_subpack + '/textures/blocks/gilded_blackstone.png')
            else:
                pass
        else:
            if old_netherrack:
                copy('template/textures/blocks/ores/nether_ores/old_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/old_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
            elif brighter_nether:
                copy('template/textures/blocks/ores/nether_ores/bright_nether_gold_ore.png',current_subpack + '/textures/blocks/nether_gold_ore.png')
                copy('template/textures/blocks/ores/nether_ores/bright_quartz_ore.png',current_subpack + '/textures/blocks/quartz_ore.png')
            else:
                pass
                #no need to override global resources

def poppy(poppy):
    if poppy == 'rose':
        copy('template/textures/blocks/flower_rose.png',current_subpack + '/textures/blocks/flower_rose.png')
        with open(current_subpack + '/texts/en_US.lang', 'a') as outfile:
            outfile.write('howtoplay.dyes.text.2=Some dye materials are harder to find than others. While most Dyes can be crafted from flowers like Red Dye from a Rose, some Dyes are found or created in more obscure ways such as: \n')
            outfile.write('tile.red_flower.poppy.name=Rose\n\n')
    elif poppy == 'cyan':
        copy('template/textures/blocks/flower_rose_blue.png',current_subpack + '/textures/blocks/flower_rose.png')
        with open(current_subpack + '/texts/en_US.lang', 'a') as outfile:
            outfile.write('howtoplay.dyes.text.2=Some dye materials are harder to find than others. While most Dyes can be crafted from flowers like Red Dye from a Cyan Rose (weird), some Dyes are found or created in more obscure ways such as: \n')
            outfile.write('tile.red_flower.poppy.name=Cyan Rose\n\n')

def smooth_oak():
    copy('template/textures/blocks/log_oak.png',current_subpack + '/textures/blocks/log_oak.png')

def smooth_stones():
    copy('template/textures/blocks/stone_diorite.png',current_subpack + '/textures/blocks/stone_diorite.png')
    copy('template/textures/blocks/stone_granite.png',current_subpack + '/textures/blocks/stone_granite.png')
    copy('template/textures/blocks/stone_granite_smooth.png',current_subpack + '/textures/blocks/stone_granite_smooth.png')

def nether(brighter_nether, black_nether_brick, crimson_nylium, warped_nylium, old_netherrack):
    if brighter_nether:
        if not old_netherrack:
            copy('template/textures/blocks/nether/bright_netherrack.png',current_subpack + '/textures/blocks/netherrack.png')
        copy('template/textures/blocks/nether/bright_soul_sand.png',current_subpack + '/textures/blocks/soul_sand.png')
        copy('template/textures/blocks/nether/bright_soul_soil.png',current_subpack + '/textures/blocks/soul_soil.png')
        if not black_nether_brick:
            copy('template/textures/blocks/nether/bright_nether_brick.png',current_subpack + '/textures/blocks/nether_brick.png')
            copy('template/textures/blocks/nether/bright_chiseled_nether_bricks.png', current_subpack + '/textures/blocks/chiseled_nether_bricks.png')
            copy('template/textures/blocks/nether/bright_cracked_nether_bricks.png', current_subpack + '/textures/blocks/cracked_nether_bricks.png')
    if black_nether_brick:
        copy('template/textures/blocks/nether/black_nether_brick.png',current_subpack + '/textures/blocks/nether_brick.png')
        copy('template/textures/blocks/nether/black_chiseled_nether_bricks.png', current_subpack + '/textures/blocks/chiseled_nether_bricks.png')
        copy('template/textures/blocks/nether/black_cracked_nether_bricks.png', current_subpack + '/textures/blocks/cracked_nether_bricks.png')
        copy('template/textures/items/netherbrick.png',current_subpack + '/textures/items/netherbrick.png')
    if old_netherrack:
        copy('template/textures/blocks/nether/old_netherrack.png',current_subpack + '/textures/blocks/netherrack.png')
    
    if crimson_nylium == 'normal':
        if old_netherrack:
            copy('template/textures/blocks/nether/nylium/normal/old_crimson_nylium_side.png',current_subpack + '/textures/blocks/crimson_nylium_side.png')
        elif brighter_nether:
            copy('template/textures/blocks/nether/nylium/normal/brighter_crimson_nylium_side.png',current_subpack + '/textures/blocks/crimson_nylium_side.png')
        else:
            pass
            #no need to override global resources
    elif crimson_nylium == 'lower':
        if old_netherrack:
            copy('template/textures/blocks/nether/nylium/lower/old_crimson_nylium_side.png',current_subpack + '/textures/blocks/crimson_nylium_side.png')
        elif brighter_nether:
            copy('template/textures/blocks/nether/nylium/lower/brighter_crimson_nylium_side.png',current_subpack + '/textures/blocks/crimson_nylium_side.png')
        else:
            copy('template/textures/blocks/nether/nylium/lower/crimson_nylium_side.png',current_subpack + '/textures/blocks/crimson_nylium_side.png')
    elif crimson_nylium == 'side':
        copy('template/textures/blocks/nether/nylium/side/crimson_nylium_side.png',current_subpack + '/textures/blocks/crimson_nylium_side.png')
    if warped_nylium == 'normal':
        if old_netherrack:
            copy('template/textures/blocks/nether/nylium/normal/old_warped_nylium_side.png',current_subpack + '/textures/blocks/warped_nylium_side.png')
        elif brighter_nether:
            copy('template/textures/blocks/nether/nylium/normal/brighter_warped_nylium_side.png',current_subpack + '/textures/blocks/warped_nylium_side.png')
        else:
            pass
            #no need to override global resources
    elif warped_nylium == 'lower':
        if old_netherrack:
            copy('template/textures/blocks/nether/nylium/lower/old_warped_nylium_side.png',current_subpack + '/textures/blocks/warped_nylium_side.png')
        elif brighter_nether:
            copy('template/textures/blocks/nether/nylium/lower/brighter_warped_nylium_side.png',current_subpack + '/textures/blocks/warped_nylium_side.png')
        else:
            copy('template/textures/blocks/nether/nylium/lower/warped_nylium_side.png',current_subpack + '/textures/blocks/warped_nylium_side.png')
    elif warped_nylium == 'side':
        copy('template/textures/blocks/nether/nylium/side/warped_nylium_side.png',current_subpack + '/textures/blocks/warped_nylium_side.png')

def cherry_picking():
    copy('template/textures/blocks/cake_top.png',current_subpack + '/textures/blocks/cake_top.png')
    copy('template/textures/items/cake.png',current_subpack + '/textures/items/cake.png')
    
def different_stems():
    print('Different melon and pumpkin stems are not currently available')
    
def unbundled_hay():
    copy('template/textures/blocks/hay_block_side.png',current_subpack + '/textures/blocks/hay_block_side.png')

def honey(honey):
    if honey == 'solid':
        copy('template/textures/blocks/honey/solid_honey_bottom.png',current_subpack + '/textures/blocks/honey_bottom.png')
        copy('template/textures/blocks/honey/solid_honey_side.png',current_subpack + '/textures/blocks/honey_side.png')
        copy('template/textures/blocks/honey/solid_honey_top.png',current_subpack + '/textures/blocks/honey_top.png')
    elif honey == 'transparent':
        copy('template/textures/blocks/honey/transparent_honey_bottom.png',current_subpack + '/textures/blocks/honey_bottom.png')
        copy('template/textures/blocks/honey/transparent_honey_side.png',current_subpack + '/textures/blocks/honey_side.png')
        copy('template/textures/blocks/honey/transparent_honey_top.png',current_subpack + '/textures/blocks/honey_top.png')

def soft_wool():
    for color in ['black', 'blue', 'brown', 'cyan', 'gray', 'green', 'light_blue', 'lime', 'magenta', 'orange', 'pink', 'purple', 'red', 'silver', 'white', 'yellow']:
            copy('template/textures/blocks/soft_wool/' + color + '_wool.png', current_subpack + '/textures/blocks/wool_colored_' + color + '.png')

def alternative_particles():
    copy('template/textures/particle/particles.png',current_subpack + '/textures/particle/particles.png')
    
def less_purple_purpur():
    copy('template/textures/blocks/less_purple_purpur/purpur_block.png',current_subpack + '/textures/blocks/purpur_block.png')
    copy('template/textures/blocks/less_purple_purpur/purpur_pillar_top.png',current_subpack + '/textures/blocks/purpur_pillar_top.png')
    copy('template/textures/blocks/less_purple_purpur/purpur_pillar.png',current_subpack + '/textures/blocks/purpur_pillar.png')

def unique_dyes():
    copy('template/textures/items/unique_dyes/gray_dye.png',current_subpack + '/textures/items/dye_powder_gray.png')
    copy('template/textures/items/unique_dyes/lime_dye.png',current_subpack + '/textures/items/dye_powder_lime.png')
    copy('template/textures/items/unique_dyes/magenta_dye.png',current_subpack + '/textures/items/dye_powder_magenta.png')
    copy('template/textures/items/unique_dyes/pink_dye.png',current_subpack + '/textures/items/dye_powder_pink.png')
    copy('template/textures/items/unique_dyes/purple_dye.png',current_subpack + '/textures/items/dye_powder_purple.png')

def better_bedrock():
    copy('template/textures/blocks/bedrock.png',current_subpack + '/textures/blocks/bedrock.png')

def redstone_dust(clean_redstone, redstone_power):
    if redstone_power:
        print('Redstone power levels not currently available')
    if clean_redstone:
        copy('template/textures/blocks/clean_redstone/redstone_dust_cross.png',current_subpack + '/textures/blocks/redstone_dust_cross.png')
        copy('template/textures/blocks/clean_redstone/redstone_dust_line.png',current_subpack + '/textures/blocks/redstone_dust_line.png')

def mine_animation(mine_animation):
    if mine_animation == 'bar':
        for stage in range (0,10):
            copy('template/textures/environment/mine_progress_bar/destroy_stage_' + str(stage) + '.png',current_subpack + '/textures/environment/destroy_stage_' + str(stage) + '.png')
    elif mine_animation == 'alternate':
        for stage in range (0,10):
            copy('template/textures/environment/alternate_block_destruction/destroy_stage_' + str(stage) + '.png',current_subpack + '/textures/environment/destroy_stage_' + str(stage) + '.png')

def visible_tripwire():
    copy('template/textures/blocks/trip_wire.png',current_subpack + '/textures/blocks/trip_wire.png')

def unobtrusive_scaffolding():
    copy('template/textures/blocks/unobtrusive_scaffolding/scaffolding_top.png',current_subpack + '/textures/blocks/scaffolding_top.png')
    
def lower_fire():
    copy('template/textures/blocks/lower_fire/fire_0_placeholder.png',current_subpack + '/textures/blocks/fire_0_placeholder.png')
    copy('template/textures/blocks/lower_fire/fire_0.png',current_subpack + '/textures/blocks/fire_0.png')
    copy('template/textures/blocks/lower_fire/fire_1_placeholder.png',current_subpack + '/textures/blocks/fire_1_placeholder.png')
    copy('template/textures/blocks/lower_fire/fire_1.png',current_subpack + '/textures/blocks/fire_1.png')

def water(clear_water, old_water):
    if clear_water:
        copy('template/textures/blocks/clearer_water/cauldron_water.png',current_subpack + '/textures/blocks/cauldron_water.png')
        copy('template/textures/blocks/clearer_water/water_still_grey.png',current_subpack + '/textures/blocks/water_still_grey.png')
        copy('template/textures/blocks/clearer_water/water_flow_grey.png',current_subpack + '/textures/blocks/water_flow_grey.png')
        if old_water:
            copy('template/no_biome_clear_water.json',current_subpack + '/biomes_client.json')
        else:
            copy('template/clear_water.json',current_subpack + '/biomes_client.json')
            copy('template/no_biome_clear_water.json',current_subpack + '/biomes_client.json')
    elif old_water:
        copy('template/no_biome.json',current_subpack + '/biomes_client.json')

def shorter_grass():
    copy('template/textures/blocks/short_grass/tallgrass.tga',current_subpack + '/textures/blocks/tallgrass.tga')
def shorter_tallgrass():
    copy('template/textures/blocks/short_grass/double_plant_grass_top.tga',current_subpack + '/textures/blocks/double_plant_grass_top.tga')
    copy('template/textures/blocks/short_grass/double_plant_grass_bottom.tga',current_subpack + '/textures/blocks/double_plant_grass_bottom.tga')
    copy('template/textures/blocks/short_grass/tallgrass_carried.tga',current_subpack + '/textures/blocks/tallgrass_carried.tga')

def kelp(kelp):
    #normal permanent permanentall or grown
    if kelp == 'permanent' or kelp == 'permanentall':
        copy('template/textures/blocks/kelp_flowers/kelp_top_bulb.tga',current_subpack + '/textures/blocks/kelp_top_bulb.tga')
        copy('template/textures/blocks/kelp_flowers/kelp_top.tga',current_subpack + '/textures/blocks/kelp_top.tga')
    if kelp == 'permanentall':
        copy('template/textures/blocks/kelp_flowers/kelp_a.tga',current_subpack + '/textures/blocks/kelp_a.tga')
        copy('template/textures/blocks/kelp_flowers/kelp_b.tga',current_subpack + '/textures/blocks/kelp_b.tga')
        copy('template/textures/blocks/kelp_flowers/kelp_c.tga',current_subpack + '/textures/blocks/kelp_c.tga')
        copy('template/textures/blocks/kelp_flowers/kelp_d.tga',current_subpack + '/textures/blocks/kelp_d.tga')
    if kelp == 'grown':
        copy('template/textures/blocks/kelp_flowers/kelp_top_bulb.tga',current_subpack + '/textures/blocks/kelp_top_bulb.tga')
        copy('template/textures/blocks/kelp_flowers/kelp_top.tga',current_subpack + '/textures/blocks/kelp_top.tga')

def observers(better_observer, observer_fix):
    if better_observer:
        #terrain texture, don't need blocks.json because the original vanilla one was made with 6 side support already
        with open('template/textures/better_observers.json', 'r') as observers:
            better_observers = json.load(observers)
            with open(current_subpack + '/textures/terrain_texture.json', 'r') as infile:
                terrain_json = json.load(infile)
                for key in better_observers['texture_data'].keys():
                    terrain_json['texture_data'][key] = better_observers['texture_data'][key]
            with open(current_subpack + '/textures/terrain_texture.json', 'w') as outfile:
                json.dump(terrain_json, outfile)
        
        for file in ['observer_back', 'observer_back_on', 'observer_front_powered', 'observer_side_powered', 'observer_side',]:
            copy('template/textures/blocks/observers/' + file + '.png', current_subpack + '/textures/blocks/' + file + '.png')
        if not observer_fix:
            copy('template/textures/blocks/observers/observer_top.png',current_subpack + '/textures/blocks/observer_top.png')
            copy('template/textures/blocks/observers/observer_top_powered.png',current_subpack + '/textures/blocks/observer_top_powered.png')
        else:
            copy('template/textures/blocks/observers/observer_top_better_fixed.png',current_subpack + '/textures/blocks/observer_top.png')
            copy('template/textures/blocks/observers/observer_top_powered_better_fixed.png',current_subpack + '/textures/blocks/observer_top_powered.png')
    elif observer_fix:
        copy('template/textures/blocks/observers/observer_top_fixed.png',current_subpack + '/textures/blocks/observer_top.png')
    
def directional_hoppers():
    print('Directional hoppers not currently available')
    #terrain texture
    with open('template/textures/directional_hoppers.json', 'r') as hoppers:
        directional_hoppers = json.load(hoppers)
        with open(current_subpack + '/textures/terrain_texture.json', 'r') as infile:
            terrain_json = json.load(infile)
            for key in directional_hoppers['texture_data'].keys():
                terrain_json['texture_data'][key] = directional_hoppers['texture_data'][key]
        with open(current_subpack + '/textures/terrain_texture.json', 'w') as outfile:
            json.dump(terrain_json, outfile)
    #blocks.json
    with open('template/directional_hoppers.json', 'r') as hoppers:
        directional_hoppers = json.load(hoppers)
        with open(current_subpack + '/blocks.json', 'r') as infile:
            blocks_json = json.load(infile)
            for key in directional_hoppers.keys():
                blocks_json[key] = directional_hoppers[key]
        with open(current_subpack + '/blocks.json', 'w') as outfile:
            json.dump(blocks_json, outfile)
    #for file in ['hopper_outside', 'hopper_back', 'hopper_inside', 'hopper_outside_flipped']:
    #    copy('template/textures/blocks/directional_hoppers/' + file + '.png', current_subpack + '/textures/blocks/' + file + '.png')
    for file in ['hopper_inside', 'hopper_s_', 'hopper_s', 'hopper_sd_', 'hopper_sd', 'hopper_sl_', 'hopper_sl', 'hopper_sr_', 'hopper_sr', 
'hopper_su_', 'hopper_su', 'hopper_t_', 'hopper_t', 'hopper_td_', 'hopper_td', 'hopper_tl_', 'hopper_tl', 'hopper_tr_', 'hopper_tr',
'hopper_tu_', 'hopper_tu']:
        copy('template/textures/blocks/directional_hoppers/' + file + '.png',current_subpack + '/textures/blocks/' + file + '.png')
    

def unobtrusive_weather():
    with open('template/sounds/quieter_rain.json', 'r') as rain:
        quiet_rain = json.load(rain)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_rain.keys():
                sound_json['sound_definitions'][key] = quiet_rain[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)

def quieter_droppers():
    print('Quieter droppers not currently available')
    #but if it was available, here's the code to do so
    '''with open('template/sounds/quieter_droppers.json', 'r') as droppers:
        quiet_droppers = json.load(droppers)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_droppers.keys():
                sound_json['sound_definitions'][key] = quiet_droppers[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)'''
def quieter_ghasts():
    with open('template/sounds/quieter_ghasts.json', 'r') as ghasts:
        quiet_ghasts = json.load(ghasts)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_ghasts.keys():
                sound_json['sound_definitions'][key] = quiet_ghasts[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)
def quieter_minecarts():
    with open('template/sounds/quieter_minecarts.json', 'r') as minecarts:
        quiet_minecarts = json.load(minecarts)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_minecarts.keys():
                sound_json['sound_definitions'][key] = quiet_minecarts[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)
def quieter_villagers():
    with open('template/sounds/quieter_villagers.json', 'r') as villagers:
        quiet_villagers = json.load(villagers)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_villagers.keys():
                sound_json['sound_definitions'][key] = quiet_villagers[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)
def quieter_fire():
    with open('template/sounds/quieter_fire.json', 'r') as fire:
        quiet_fire = json.load(fire)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_fire.keys():
                sound_json['sound_definitions'][key] = quiet_fire[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)
def quieter_portals():
    with open('template/sounds/quieter_portals.json', 'r') as portals:
        quiet_portals = json.load(portals)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_portals.keys():
                sound_json['sound_definitions'][key] = quiet_portals[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)
def quieter_water():
    with open('template/sounds/quieter_water.json', 'r') as water:
        quiet_water = json.load(water)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_water.keys():
                sound_json['sound_definitions'][key] = quiet_water[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)
def quieter_endermen():
    with open('template/sounds/quieter_endermen.json', 'r') as endermen:
        quiet_endermen = json.load(endermen)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_endermen.keys():
                sound_json['sound_definitions'][key] = quiet_endermen[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)
def quieter_pistons():
    with open('template/sounds/quieter_pistons.json', 'r') as pistons:
        quiet_pistons = json.load(pistons)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_pistons.keys():
                sound_json['sound_definitions'][key] = quiet_pistons[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)
def quieter_cows():
    with open('template/sounds/quieter_cows.json', 'r') as cows:
        quiet_cows = json.load(cows)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_cows.keys():
                sound_json['sound_definitions'][key] = quiet_cows[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)
def quieter_shulker_boxes():
    with open('template/sounds/quieter_shulker_boxes.json', 'r') as shulker_boxes:
        quiet_shulker_boxes = json.load(shulker_boxes)
        with open(current_subpack + '/sounds/sound_definitions.json', 'r') as infile:
            sound_json = json.load(infile)
            for key in quiet_shulker_boxes.keys():
                sound_json['sound_definitions'][key] = quiet_shulker_boxes[key]
        with open(current_subpack + '/sounds/sound_definitions.json', 'w') as outfile:
            json.dump(sound_json, outfile)

def glass(glass, stained_glass):
    if glass == 'borderless':
        copy('template/textures/blocks/borderless_glass/glass.png',current_subpack + '/textures/blocks/glass.png')
    elif glass == 'clean':
        copy('template/textures/blocks/clean_glass/glass.png',current_subpack + '/textures/blocks/glass.png')
    if stained_glass == 'borderless':
        for color in ['black', 'blue', 'brown', 'cyan', 'gray', 'green', 'light_blue', 'lime', 'magenta', 'orange', 'pink', 'purple', 'red', 'silver', 'white', 'yellow']:
            copy('template/textures/blocks/borderless_glass/' + color + '_stained_glass.png', current_subpack + '/textures/blocks/glass_' + color + '.png')
    elif stained_glass == 'clean':
        for color in ['black', 'blue', 'brown', 'cyan', 'gray', 'green', 'light_blue', 'lime', 'magenta', 'orange', 'pink', 'purple', 'red', 'silver', 'white', 'yellow']:
            copy('template/textures/blocks/clean_glass/' + color + '_stained_glass.png', current_subpack + '/textures/blocks/glass_' + color + '.png')

def pumpkin_overlay(pumpkin_overlay):
    if pumpkin_overlay == 'transparent':
        copy('template/textures/misc/pumpkinblur_transparent.png',current_subpack + '/textures/misc/pumpkinblur.png')
    elif pumpkin_overlay == 'remove':
        copy('template/textures/misc/pumpkinblur_remove.png',current_subpack + '/textures/misc/pumpkinblur.png')

def lower_shield():
    copy('template/models/entity/shield.geo.json', current_subpack + '/models/entity/shield.geo.json')

def clean_ice():
    for file in ['blue_ice', 'frosted_ice_0', 'frosted_ice_1', 'frosted_ice_2', 'frosted_ice_3', 'ice', 'packed_ice']:
        copy('template/textures/blocks/clean_ice/' + file + '.png',current_subpack + '/textures/blocks/' + file + '.png')

def alternate_enchant_glint():
    copy('template/textures/misc/enchanted_item_glint.png',current_subpack + '/textures/misc/enchanted_item_glint.png')

def icons(visible_wither_hearts, crosshair, rainbow_xp):
    '''if rainbow_xp:
        image1 = Image.open('template/textures/gui/icons_no_crosshair.png')
        image2 = Image.open('template/textures/gui/icons/rainbow_xp.png')
        image3 = Image.alpha_composite(image1, image2)
        image4 = Image.open('template/textures/gui/icons/' + crosshair + '_crosshair.png')
        image5 = Image.alpha_composite(image3, image4)
        if visible_wither_hearts:
            image6 = Image.open('template/textures/gui/icons/wither_hearts.png')
            final_image = Image.alpha_composite(image5, image6)
        else:
            final_image = image5
    else:
        image1 = Image.open('template/textures/gui/icons_no_crosshair.png')
        image2 = Image.open('template/textures/gui/icons/' + crosshair + '_crosshair.png')
        image3 = Image.alpha_composite(image1, image2)
        if visible_wither_hearts:
            image4 = Image.open('template/textures/gui/icons/wither_hearts.png')
            final_image = Image.alpha_composite(image3, image4)
        else:
            final_image = image_3
    final_image.save(current_subpack + '/textures/gui/icons.png')'''
    print('Rainbow xp temporarily diabled')
    image1 = Image.open('template/textures/gui/icons_no_crosshair.png')
    image2 = Image.open('template/textures/gui/icons/' + crosshair + '_crosshair.png')
    image3 = Image.alpha_composite(image1, image2)
    if visible_wither_hearts:
        image4 = Image.open('template/textures/gui/icons/wither_hearts.png')
        final_image = Image.alpha_composite(image3, image4)
    else:
        final_image = image3
    final_image.save(current_subpack + '/textures/gui/icons.png')

def alpha_foliage():
    copy('template/textures/blocks/alpha_foliage/acacia_leaves.png',current_subpack + '/textures/blocks/leaves_acacia_carried.png')
    copy('template/textures/blocks/alpha_foliage/acacia_leaves.png',current_subpack + '/textures/blocks/leaves_acacia.png')
    copy('template/textures/blocks/alpha_foliage/birch_leaves.png',current_subpack + '/textures/blocks/leaves_birch_carried.png')
    copy('template/textures/blocks/alpha_foliage/birch_leaves.png',current_subpack + '/textures/blocks/leaves_birch.png')
    copy('template/textures/blocks/alpha_foliage/dark_oak_leaves.png',current_subpack + '/textures/blocks/leaves_dark_oak_carried.png')
    copy('template/textures/blocks/alpha_foliage/dark_oak_leaves.png',current_subpack + '/textures/blocks/leaves_dark_oak.png')
    copy('template/textures/blocks/alpha_foliage/fern_carried.tga',current_subpack + '/textures/blocks/fern_carried.tga')
    copy('template/textures/blocks/alpha_foliage/fern.tga',current_subpack + '/textures/blocks/fern.tga')
    copy('template/textures/blocks/alpha_foliage/jungle_leaves.png',current_subpack + '/textures/blocks/leaves_jungle_carried.png')
    copy('template/textures/blocks/alpha_foliage/jungle_leaves.png',current_subpack + '/textures/blocks/leaves_jungle.png')
    copy('template/textures/blocks/alpha_foliage/double_plant_fern_top.tga',current_subpack + '/textures/blocks/double_plant_fern_top.tga')
    copy('template/textures/blocks/alpha_foliage/double_plant_fern_bottom.tga',current_subpack + '/textures/blocks/double_plant_fern_bottom.tga')
    copy('template/textures/blocks/alpha_foliage/double_plant_fern_carried.png',current_subpack + '/textures/blocks/double_plant_fern_carried.png')
    copy('template/textures/blocks/alpha_foliage/leaves_acacia_opaque.png',current_subpack + '/textures/blocks/leaves_acacia_opaque.png')
    copy('template/textures/blocks/alpha_foliage/leaves_big_oak_opaque.png',current_subpack + '/textures/blocks/leaves_big_oak_opaque.png')
    copy('template/textures/blocks/alpha_foliage/leaves_birch_opaque.png',current_subpack + '/textures/blocks/leaves_birch_opaque.png')
    copy('template/textures/blocks/alpha_foliage/leaves_jungle_opaque.png',current_subpack + '/textures/blocks/leaves_jungle_opaque.png')
    copy('template/textures/blocks/alpha_foliage/leaves_oak_opaque.png',current_subpack + '/textures/blocks/leaves_oak_opaque.png')
    copy('template/textures/blocks/alpha_foliage/leaves_spruce_opaque.png',current_subpack + '/textures/blocks/leaves_spruce_opaque.png')
    copy('template/textures/blocks/alpha_foliage/oak_leaves.png',current_subpack + '/textures/blocks/leaves_oak_carried.png')
    copy('template/textures/blocks/alpha_foliage/oak_leaves.png',current_subpack + '/textures/blocks/leaves_oak.png')
    copy('template/textures/blocks/alpha_foliage/oak_sapling.png',current_subpack + '/textures/blocks/sapling_oak.png')
    copy('template/textures/blocks/alpha_foliage/spruce_leaves.png',current_subpack + '/textures/blocks/leaves_spruce_carried.png')
    copy('template/textures/blocks/alpha_foliage/spruce_leaves.png',current_subpack + '/textures/blocks/leaves_spruce.png')
    copy('template/textures/blocks/alpha_foliage/sugar_cane.png',current_subpack + '/textures/blocks/reeds.png')
    copy('template/textures/blocks/alpha_foliage/double_plant_grass_top.tga',current_subpack + '/textures/blocks/double_plant_grass_top.tga')
    copy('template/textures/blocks/alpha_foliage/double_plant_grass_bottom.tga',current_subpack + '/textures/blocks/double_plant_grass_bottom.tga')
    copy('template/textures/blocks/alpha_foliage/double_plant_grass_carried.png',current_subpack + '/textures/blocks/double_plant_grass_carried.png')
    copy('template/textures/blocks/alpha_foliage/waterlily.png',current_subpack + '/textures/blocks/waterlily.png')
    copy('template/textures/blocks/alpha_foliage/tallgrass_carried.tga',current_subpack + '/textures/blocks/tallgrass_carried.tga')
    copy('template/textures/blocks/alpha_foliage/tallgrass.png',current_subpack + '/textures/blocks/tallgrass.png')
    copy('template/textures/blocks/alpha_foliage/vine.png',current_subpack + '/textures/blocks/vine.png')
    copy('template/textures/blocks/alpha_foliage/vine.png',current_subpack + '/textures/blocks/vine_carried.png')
    
    copy('template/textures/colormap/foliage.png',current_subpack + '/textures/colormap/foliage.png')
    copy('template/textures/colormap/grass.png',current_subpack + '/textures/colormap/grass.png')

def old_cobblestone():
    copy('template/textures/blocks/old_stuff/cobblestone.png',current_subpack + '/textures/blocks/cobblestone.png')
    copy('template/textures/blocks/old_stuff/mossy_cobblestone.png',current_subpack + '/textures/blocks/cobblestone_mossy.png')
def old_gravel():
    copy('template/textures/blocks/old_stuff/gravel.png',current_subpack + '/textures/blocks/gravel.png')
def old_lava():
    #print('Old lava is not currently available')
    copy('template/textures/blocks/old_stuff/lava_flow.png',current_subpack + '/textures/blocks/lava_flow.png')
    copy('template/textures/blocks/old_stuff/lava_still.png',current_subpack + '/textures/blocks/lava_still.png')
def old_metals(old_metal):
    if old_metal == 'java':
        for material in ['diamond', 'gold', 'iron']:
            for side in ['', '_side', '_bottom']:
                copy('template/textures/blocks/old_stuff/' + material + '_block' + side + '.png', current_subpack + '/textures/blocks/' + material + '_block' + side + '.png')
        #terrain texture
        with open('template/textures/old_metal_blocks.json', 'r') as metal_blocks:
            old_metal_blocks = json.load(metal_blocks)
            with open(current_subpack + '/textures/terrain_texture.json', 'r') as infile:
                terrain_json = json.load(infile)
                for key in old_metal_blocks['texture_data'].keys():
                    terrain_json['texture_data'][key] = old_metal_blocks['texture_data'][key]
            with open(current_subpack + '/textures/terrain_texture.json', 'w') as outfile:
                json.dump(terrain_json, outfile)
        #blocks.json                
        with open('template/old_metal_blocks.json', 'r') as metal_blocks:
            old_metal_blocks = json.load(metal_blocks)
            with open(current_subpack + '/blocks.json', 'r') as infile:
                blocks_json = json.load(infile)
                for key in old_metal_blocks.keys():
                    blocks_json[key] = old_metal_blocks[key]
            with open(current_subpack + '/blocks.json', 'w') as outfile:
                json.dump(blocks_json, outfile)
    elif old_metal == 'pocket':
        copy('template/textures/blocks/old_stuff/' + material + '_block.png', current_subpack + '/textures/blocks/' + material + '_block.png')
def old_lapis():
    copy('template/textures/blocks/old_stuff/lapis_block.png',current_subpack + '/textures/blocks/lapis_block.png')
def old_sponge():
    copy('template/textures/blocks/old_stuff/sponge.png',current_subpack + '/textures/blocks/sponge.png')
    copy('template/textures/blocks/old_stuff/wet_sponge.png',current_subpack + '/textures/blocks/sponge_wet.png')
def old_damage():
    copytree('template/sounds/damage',current_subpack + '/sounds/damage')
def old_wool():
    for color in ['black', 'blue', 'brown', 'cyan', 'gray', 'green', 'light_blue', 'lime', 'magenta', 'orange', 'pink', 'purple', 'red', 'silver', 'white', 'yellow']:
            copy('template/textures/blocks/old_stuff/' + color + '_wool.png', current_subpack + '/textures/blocks/wool_colored_' + color + '.png')
def old_shulkers():
    mkdir(current_subpack + '/textures/entity/shulker')
    for color in ['black', 'blue', 'brown', 'cyan', 'gray', 'green', 'light_blue', 'lime', 'magenta', 'orange', 'pink', 'red', 'silver', 'white', 'yellow']:
            copy('template/textures/entity/shulker/shulker_' + color + '.png', current_subpack + '/textures/entity/shulker/shulker_' + color + '.png')

def xisuma_paintings():
    mkdir(current_subpack + '/textures/painting')
    copy('template/textures/painting/kz.png',current_subpack + '/textures/painting/kz.png')
def xisuma_turtles():
    copy('template/textures/entity/sea_turtle.png',current_subpack + '/textures/entity/sea_turtle.png')
def xisuma_squids():
    copy('template/textures/entity/squid.png',current_subpack + '/textures/entity/squid.png')
def wandering_xisuma():
    copy('template/textures/entity/wandering_trader.png',current_subpack + '/textures/entity/wandering_trader.png')
    copy('template/textures/entity/llama/decor/trader_llama.png',current_subpack + '/textures/entity/llama/decor/trader_llama.png')

def bee_wither():
    mkdir(current_subpack + '/textures/entity/wither_boss')
    copy('template/textures/entity/wither_boss/wither_invulnerable.png',current_subpack + '/textures/entity/wither_boss/wither_invulnerable.png')
    copy('template/textures/entity/wither_boss/wither.png',current_subpack + '/textures/entity/wither_boss/wither.png')
    with open(current_subpack + '/texts/en_US.lang','a') as outfile:
        outfile.write('achievement.killWither.desc=Kill the Bee Wither\n')
        outfile.write('achievement.spawnWither.desc=Spawn the Bee Wither\n')
        outfile.write('entity.wither.name=Bee Wither\n')
        outfile.write('entity.wither_skull.name=Bee Wither Skull\n')
        outfile.write('entity.wither_skull_dangerous.name=Bee Wither Skull\n')
        outfile.write('howtoplay.beacons.text.2=They are crafted with Glass, Obsidian, and Nether Stars (which is obtained by defeating the Bee Wither).\n')
        outfile.write('tips.game.53=The Beacon is a powerful item that can only be crafted with a nether star from the Bee Wither!\n\n')

def beeralis():
    mkdir(current_subpack + '/textures/entity/bee')
    for state in ['_angry_nectar', '_angry', '_nectar', '']:
        copy('template/textures/entity/bee/bee' + state + '.png',current_subpack + '/textures/entity/bee/bee' + state + '.png')
    with open(current_subpack + '/texts/en_US.lang','a') as outfile:
        outfile.write('entity.bee.name=Beeralis\n')
        outfile.write('item.spawn_egg.entity.bee.name=Spawn Beeralis\n')
        outfile.write('tile.beehive.name=Beeralis Hive\n')
        outfile.write('tile.bee_nest.name=Beeralis Nest\n\n')
        print('Bee achievements not currently available')

def ilmango_apples():
    copy('template/textures/items/golden_apple.png',current_subpack + '/textures/items/apple_golden.png')

def bacon_beacon():
    copy('template/textures/entity/beacon_beam.png',current_subpack + '/textures/entity/beacon_beam.png')

def concorp_wings():
    copy('template/textures/items/elytra.png',current_subpack + '/textures/items/elytra.png')
    copy('template/textures/items/broken_elytra.png',current_subpack + '/textures/items/broken_elytra.png')
    copy('template/textures/models/armor/elytra.png',current_subpack + '/textures/models/armor/elytra.png')

def slime(slime_color, sticky_piston_sides, slime):
    if slime_color != 'normal':
        mkdir(current_subpack + '/textures/entity/slime')
        copy('template/textures/slime_variants/' + slime_color + '/block/slime_block_' + slime + '.png', current_subpack + '/textures/blocks/slime.png')
        copy('template/textures/slime_variants/' + slime_color + '/block/piston_top_sticky.png', current_subpack + '/textures/blocks/piston_top_sticky.png')
        copy('template/textures/slime_variants/' + slime_color + '/entity/slime/slime.png', current_subpack + '/textures/entity/slime/slime.png')
        copy('template/textures/slime_variants/' + slime_color + '/item/slime_ball.png', current_subpack + '/textures/items/slimeball.png')
    if sticky_piston_sides:
        mkdir(current_subpack + '/textures/entity/pistonarm')
        #terrain texture
        with open('template/textures/sticky_piston_sides.json', 'r') as sticky:
            sticky_sides = json.load(sticky)
            with open(current_subpack + '/textures/terrain_texture.json', 'r') as infile:
                terrain_json = json.load(infile)
                for key in sticky_sides['texture_data'].keys():
                    terrain_json['texture_data'][key] = sticky_sides['texture_data'][key]
            with open(current_subpack + '/textures/terrain_texture.json', 'w') as outfile:
                json.dump(terrain_json, outfile)
        #blocks.json
        with open('template/sticky_piston_sides.json', 'r') as sticky:
            sticky_sides = json.load(sticky)
            with open(current_subpack + '/blocks.json', 'r') as infile:
                blocks_json = json.load(infile)
                for key in sticky_sides.keys():
                    blocks_json[key] = sticky_sides[key]
            with open(current_subpack + '/blocks.json', 'w') as outfile:
                json.dump(blocks_json, outfile)
        copy('template/textures/slime_variants/' + slime_color + '/entity/pistonarm/pistonArmSticky_sides.png',current_subpack + '/textures/entity/pistonarm/pistonArmSticky.png')
        copy('template/textures/slime_variants/' + slime_color + '/block/piston_side_sticky.png', current_subpack + '/textures/blocks/piston_side_sticky.png')
    elif slime_color != 'normal':
        mkdir(current_subpack + '/textures/entity/pistonarm')
        copy('template/textures/slime_variants/' + slime_color + '/entity/pistonarm/pistonArmSticky.png',current_subpack + '/textures/entity/pistonarm/pistonArmSticky.png')

def rails(rail_shape):
    if rail_shape == 'skinny':
        for file in ['rail_normal_turned', 'rail_activator_powered', 'rail_activator', 'rail_detector_powered', 'rail_detector', 'rail_golden_powered', 'rail_golden', 'rail_normal_turned', 'rail_normal']:
            copy('template/textures/blocks/rails/skinny_rails/' + file + '.png', current_subpack + '/textures/blocks/' + file + '.png')
        copy('template/textures/entity/skinny_minecart.png',current_subpack + '/textures/entity/minecart.png')
    elif rail_shape == 'monorail':
        for file in ['rail_normal_turned', 'rail_activator_powered', 'rail_activator', 'rail_detector_powered', 'rail_detector', 'rail_golden_powered', 'rail_golden', 'rail_normal_turned', 'rail_normal']:
            copy('template/textures/blocks/rails/monorail/' + file + '.png', current_subpack + '/textures/blocks/' + file + '.png')
        copy('template/textures/entity/monorail_minecart.png',current_subpack + '/textures/entity/minecart.png')

def transparent_portals():
    copy('template/textures/blocks/transparent_portals/portal_placeholder.png',current_subpack + '/textures/blocks/portal_placeholder.png')
    copy('template/textures/blocks/transparent_portals/portal.png',current_subpack + '/textures/blocks/portal.png')

def endless_end_rods():
    print('Endless end rods not currently available')
    #copy('template/textures/blocks/end_rod.png',current_subpack + '/textures/blocks/end_rod.png')

def visual_honey_stages():
    print('Visual honey stages not currently available')

def classic_netherite():
    for armor in ['helmet','chestplate','leggings','boots']:
        copy('template/textures/items/netherite/netherite_' + armor + '.png',current_subpack + '/textures/items/netherite_' + armor + '.png')
    copy('template/textures/models/armor/netherite_1.png',current_subpack + '/textures/models/armor/netherite_1.png')
    copy('template/textures/models/armor/netherite_2.png',current_subpack + '/textures/models/armor/netherite_2.png')

def no_cave_sounds():
    copytree('template/sounds/cave',current_subpack + '/sounds/cave')

def zombie_pigman():
    mkdir(current_subpack + '/entity')
    copy('template/entity/zombie_pigman.entity.json',current_subpack + '/entity/zombie_pigman.entity.json')
    with open(current_subpack + '/texts/en_US.lang', 'a') as outfile:
        outfile.write('entity.zombie_pigman.name=Zombie Pigman\n')
        outfile.write('item.spawn_egg.entity.zombie_pigman.name=Spawn Zombie Pigman\n\n')

def noteblock_banners():
    print('Noteblock banners not currently available')

def fully_grown_crops():
    print('Grown crop markers not currently available')

def hunger_preview():
    print('Hunger preview not currently available')

def gui(gui):
    if gui == 'dark':
        mkdir(current_subpack + '/textures/gui/newgui')
        mkdir(current_subpack + '/textures/gui/newgui/buttons')
        mkdir(current_subpack + '/textures/gui/newgui/buttons/border')
        mkdir(current_subpack + '/textures/gui/newgui/buttons/borderless')
        mkdir(current_subpack + '/textures/gui/newgui/mob_effects')
        mkdir(current_subpack + '/textures/gui/newgui/play_screen')
        mkdir(current_subpack + '/textures/gui/achievements')
        for subdir, dirs, files in walk('template/darkmode/textures/ui'):
            for filename in files:
                template_filepath = subdir + '/' + filename
                #print(template_filepath)
                new_filepath = template_filepath.replace('template/darkmode',current_subpack)
                #print(new_filepath)
                copy(template_filepath, new_filepath)
        copy('template/darkmode/textures/gui/achievements/fillalpha.png',current_subpack + '/textures/gui/achievements/fillalpha.png')
        for subdir, dirs, files in walk('template/darkmode/textures/gui/newgui'):
            for filename in files:
                template_filepath = subdir + '/' + filename
                #print(template_filepath)
                new_filepath = template_filepath.replace('template/darkmode',current_subpack)
                #print(new_filepath)
                copy(template_filepath, new_filepath)
        

def zip_folder(preferences_json):
    #since we are done working, we can rename the folder so that it shows the proper name when extracted as well as the original will be where it needs to go
    if not isdir('completed_packs/' + preferences_json['name']):
        mkdir('completed_packs/' + preferences_json['name'])
    rename('in_progress','Overhang Tweaks')
    with ZipFile('completed_packs/' + preferences_json['name'] + '/overhangtweaks_' + preferences_json['name'] + '_' + '.'.join([str(preferences_json['version'][0]), str(preferences_json['version'][1]), str(preferences_json['version'][2])]) + '.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('Overhang Tweaks'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
    rename('Overhang Tweaks','completed_packs/' + preferences_json['name'] + '/Overhang Tweaks ' + preferences_json['name'].title() + ' ' + '.'.join([str(preferences_json['version'][0]), str(preferences_json['version'][1]), str(preferences_json['version'][2])]))
    #rename('Overhang Tweaks', 'completed_packs/' + preferences_json['name'] + '/overhangtweaks_' + preferences_json['name'] + '_' + str(edition) + '.mcpack')


if __name__ == '__main__':
    main_window = Tk()
    main_window.withdraw()
    preferences_location = askopenfilename(initialdir = "/Users/calebeden/Documents/Eclipse/Overhang Tweaks/Overhang Tweaks/preferences",title = "Select Preferences Json")
    preferences_json = json.load(open(preferences_location,'r'))
    
    #first we make sure the preferences file has the correct version. If not, we ask the user to fix it and exit the program
    if preferences_json['version'] != json.load(open('preferences/version.json', 'r'))['version']:
        print('Incorrect version number. Please fix and start over!')
        exit()
    
    pack_setup(preferences_json, preferences_location)
    
    for profile in preferences_json['profiles']:
        #print(profile)
        global current_subpack
        current_subpack = 'in_progress/subpacks/' + profile['nickname'].lower()
        #print(current_subpack)
        mkdir(current_subpack)
        subpack_setup(preferences_json)
        
        if profile['poppied_golem']:
            poppied_golem()
        
        if profile['pebbleless_dirt']:
            pebbleless_dirt()
        grass(profile['grass'], profile['pebbleless_dirt'], profile['alpha_foliage'])
        mycelium(profile['mycelium'], profile['pebbleless_dirt'])
        path(profile['path'], profile['pebbleless_dirt'])
        podzol(profile['podzol'], profile['pebbleless_dirt'])
        snow(profile['snow'], profile['pebbleless_dirt'], profile['whiter_snow'])
        
        if profile['pebbleless_coarse_dirt']:
            pebbleless_coarse_dirt()
        
        if profile['visible_wither_hearts']:
            visible_wither_hearts()
        
        if profile['hardened_clay']:
            hardened_clay()
        
        if profile['clean_leather_armor']:
            clean_leather_armor()
        
        if profile['circle_sun_moon']:
            circle_sun_moon()
        
        if profile['newshape_iron_nugget']:
            newshape_iron_nugget()
        
        ores(profile['universal_ores'], profile['ore_border'], profile['brighter_nether'], profile['old_netherrack'])
        
        poppy(profile['poppy'])
        
        if profile['smooth_oak']:
            smooth_oak()
        
        if profile['smooth_stones']:
            smooth_stones()
        
        nether(profile['brighter_nether'], profile['black_nether_brick'], profile['crimson_nylium'], profile['warped_nylium'], profile['old_netherrack'])
        
        if profile['cherry_picking']:
            cherry_picking()
        
        if profile['different_stem']:
            different_stems()
        
        if profile['unbundled_hay']:
            unbundled_hay()
           
        honey(profile['honey'])
        
        if profile['wool'] == 'soft':
            soft_wool()
            
        if profile['alternative_particle']:
            alternative_particles()
            
        if profile['less_purple_purpur']:
            less_purple_purpur()
        
        if profile['unique_dye']:
            unique_dyes()
        
        if profile['better_bedrock']:
            better_bedrock()
        
        redstone_dust(profile['clean_redstone'], profile['redstone_power'])
        
        mine_animation(profile['mine_animation'])
        
        if profile['visible_tripwire']:
            visible_tripwire()
        
        if profile['unobtrusive_scaffolding']:
            unobtrusive_scaffolding()
        
        if profile['lower_fire']:
            lower_fire()
        
        water(profile['clearer_water'], profile['old_water'])
        
        if profile['shorter_grass'] and not profile['alpha_foliage']:
            shorter_grass()
        if profile['shorter_tallgrass'] and not profile['alpha_foliage']:
            shorter_tallgrass()
        
        kelp(profile['kelp'])
        
        observers(profile['better_observer'],['observer_fix'])
            
        if profile['directional_hopper']:
            directional_hoppers()
        
        if profile['unobtrusive_weather']:
            unobtrusive_weather()
        
        if profile['quieter_dropper']:
            quieter_droppers()
        if profile['quieter_ghast']:
            quieter_ghasts()
        if profile['quieter_minecart']:
            quieter_minecarts()
        if profile['quieter_villager']:
            quieter_villagers()
        if profile['quieter_fire']:
            quieter_fire()
        if profile['quieter_portal']:
            quieter_portals()
        if profile['quieter_water']:
            quieter_water()
        if profile['quieter_endermen']:
            quieter_endermen()
        if profile['quieter_piston']:
            quieter_pistons()
        if profile['quieter_cow']:
            quieter_cows()
        if profile['quieter_shulker_box']:
            quieter_shulker_boxes()
        
        glass(profile['glass'], profile['stained_glass'])
        
        pumpkin_overlay(profile['pumpkin_overlay'])
        
        if profile['clean_ice']:
            clean_ice()
        
        if profile['lower_shield']:
            lower_shield()
        
        if profile['alternate_enchant_glint']:
            alternate_enchant_glint()
        
        icons(profile['visible_wither_hearts'], profile['crosshair'], profile['rainbow_xp'])
        
        if profile['alpha_foliage']:
            alpha_foliage()
        
        if profile['old_cobblestone']:
            old_cobblestone()
        if profile['old_gravel']:
            old_gravel()
        if profile['old_lava']:
            old_lava()
        old_metals(profile['old_metal'])
        if profile['old_lapis']:
            old_lapis()
        if profile['old_sponge']:
            old_sponge()
        if profile['old_damage']:
            old_damage()
        if profile['wool'] == 'old':
            old_wool()
        if profile['old_shulker']:
            old_shulkers()
        
        if profile['xisuma_painting']:
            xisuma_paintings()
        if profile['xisuma_turtle']:
            xisuma_turtles()
        if profile['xisuma_squid']:
            xisuma_squids()
        
        if profile['bee_wither']:
            bee_wither()
        
        if profile['beeralis']:
            beeralis()
        
        if profile['ilmango_apple']:
            ilmango_apples()
        
        if profile['bacon_beacon']:
            bacon_beacon()
        
        if profile['concorp_wing']:
            concorp_wings()
        
        slime(profile['slime_color'], profile['sticky_piston_sides'], profile['slime'])
        
        panorama(profile['panorama'])
        
        rails(profile['rail_shape'])
        
        if profile['transparent_portal']:
            transparent_portals()
        
        if profile['endless_end_rod']:
            endless_end_rods()
        
        if profile['honey_stages']:
            visual_honey_stages()
        
        if profile['classic_netherite']:
            classic_netherite()
        
        if profile['no_cave_sounds']:
            no_cave_sounds()
        
        if profile['old_zombie_pigman']:
            zombie_pigman()
        
        if profile['noteblock_banners']:
            noteblock_banners()
        
        if profile['fully_grown_crops']:
            fully_grown_crops()
        
        if profile['hunger_preview']:
            hunger_preview()
        
        gui(profile['gui'])
    
    zip_folder(preferences_json)
    