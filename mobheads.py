###########################################
# Author: calebeden
# File: class_based_mobheads.py
# Created on Wed Jun 15 2022
###########################################

from os import mkdir, walk, chdir
from os.path import join
from shutil import copy, rmtree, copytree
from zipfile import ZipFile
import json
from PlayerHead import Mob


def setup_folders():
    try:
        rmtree('Mob Heads Addon')
    except:
        pass
    try:
        rmtree('Mob Heads Addon')
    except:
        pass


    

    mkdir('Mob Heads Addon')
    mkdir('Mob Heads Addon/resource_pack')
    mkdir('Mob Heads Addon/resource_pack/attachables')
    mkdir('Mob Heads Addon/resource_pack/texts')
    copytree('template/resource_pack/mob_head_textures', 'Mob Heads Addon/resource_pack/textures')
    mkdir('Mob Heads Addon/resource_pack/textures/items/mrc_heads')
    mkdir('Mob Heads Addon/resource_pack/textures/items/mrc_head_bundles')
    mkdir('Mob Heads Addon/resource_pack/textures/models')
    mkdir('Mob Heads Addon/resource_pack/textures/models/mrc_heads')
    mkdir('Mob Heads Addon/resource_pack/models')
    mkdir('Mob Heads Addon/resource_pack/models/entity')
    copy('template/resource_pack/models/entity/mrc_player_head.json',
         'Mob Heads Addon/resource_pack/models/entity/mrc_player_head.json')
    copytree('template/resource_pack/mob_head_render_controllers', 'Mob Heads Addon/resource_pack/render_controllers')
    copytree('template/resource_pack/mob_head_entity', 'Mob Heads Addon/resource_pack/entity')
    copy('template/resource_pack/mob_head_pack_icon.png',
         'Mob Heads Addon/resource_pack/pack_icon.png')

    mkdir('Mob Heads Addon/behavior_pack')
    copytree('template/behavior_pack/mob_head_items', 'Mob Heads Addon/behavior_pack/items')
    copytree('template/behavior_pack/mob_head_entities', 'Mob Heads Addon/behavior_pack/entities')
    copytree('template/behavior_pack/mob_head_animation_controllers', 'Mob Heads Addon/behavior_pack/animation_controllers')
    copytree('template/behavior_pack/mob_head_loot_tables', 'Mob Heads Addon/behavior_pack/loot_tables')
    copytree('template/behavior_pack/mob_head_recipes', 'Mob Heads Addon/behavior_pack/recipes')
    copy('template/behavior_pack/mob_head_pack_icon.png',
         'Mob Heads Addon/behavior_pack/pack_icon.png')


def generate_manifests():
    with open('version.json', 'r') as infile:
        version = json.load(infile)
    version_string = '.'.join(str(x) for x in version)

    with open('template/resource_pack/mob_head_manifest.json', 'r') as infile:
        resource_manifest = json.load(infile)
    resource_manifest['header']['description'] += version_string
    resource_manifest['header']['version'] = version
    resource_manifest['modules'][0]['description'] += version_string
    resource_manifest['dependencies'][0]['version'] = version
    with open('Mob Heads Addon/resource_pack/manifest.json', 'w') as outfile:
        json.dump(resource_manifest, outfile)

    with open('template/behavior_pack/mob_head_manifest.json', 'r') as infile:
        behavior_manifest = json.load(infile)
    behavior_manifest['header']['description'] += version_string
    behavior_manifest['header']['version'] = version
    behavior_manifest['modules'][0]['description'] += version_string
    behavior_manifest['dependencies'][0]['version'] = version
    with open('Mob Heads Addon/behavior_pack/manifest.json', 'w') as outfile:
        json.dump(behavior_manifest, outfile)


def package_addon():
    with open('Mob Heads Addon/resource_pack/textures/item_texture.json', 'r') as infile:
        item_texture_json = json.load(infile)
    item_texture_json['texture_data']['mrc:jeb_essence'] = {'textures': 'textures/items/jeb_essence'}
    item_texture_json['texture_data']['mrc:toast_essence'] = {'textures': 'textures/items/toast_essence'}
    with open('Mob Heads Addon/resource_pack/textures/item_texture.json', 'w') as outfile:
        json.dump(item_texture_json, outfile)
    with open('Mob Heads Addon/resource_pack/texts/en_US.lang', 'a') as outfile:
            outfile.write('item.mrc:jeb_essence=Essence of jeb_\n')
            outfile.write('item.mrc:toast_essence=Essence of Toast\n')

    chdir('Mob Heads Addon')
    with ZipFile('Mob Heads.mcaddon', 'w') as archive:
        for subdir, dirs, files in walk('behavior_pack'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
        for subdir, dirs, files in walk('resource_pack'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)

    # chdir('behavior_pack')
    # with ZipFile('Mob Heads Behavior.mcpack', 'w') as archive:
    #     for subdir, dirs, files in walk('./'):
    #         for file in files:
    #             if not file.endswith('.mcpack'):
    #                 filepath = join(subdir, file)
    #                 archive.write(filepath)
    # chdir('../')
    # move('behavior_pack/Mob Heads Behavior.mcpack', 'Mob Heads Behavior.mcpack')

    # chdir('resource_pack')
    # with ZipFile('Mob Heads Resource.mcpack', 'w') as archive:
    #     for subdir, dirs, files in walk('./'):
    #         for file in files:
    #             if not file.endswith('.mcpack'):
    #                 filepath = join(subdir, file)
    #                 archive.write(filepath)
    # chdir('../')
    # move('resource_pack/Mob Heads Resource.mcpack', 'Mob Heads Resource.mcpack')
    chdir('../')


def main():
    setup_folders()
    generate_manifests()

    item_texture_json = {"resource_pack_name": "playerheads",
                         "texture_name": "atlas.items", "texture_data": {}}

    for subdir, dirs, files in walk('template/skins/mobs'):
        for filename in files:
            Mob(filename, 'Mob Heads Addon').add_to_pack(item_texture_json)

    with open('Mob Heads Addon/resource_pack/textures/item_texture.json', 'w') as outfile:
        json.dump(item_texture_json, outfile)

    package_addon()

    print("\
\nDone!")

    return


if __name__ == "__main__":
    main()
