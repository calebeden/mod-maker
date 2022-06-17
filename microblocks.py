###########################################
# Author: calebeden
# File: class_based_microblocks.py
# Created on Wed Jun 15 2022
###########################################

from os import mkdir, walk, chdir
from os.path import join
from shutil import copy, rmtree, move
from zipfile import ZipFile
import json
from PlayerHead import Microblock, Person, Custom


def setup_folders():
    try:
        rmtree('Microblocks Addon')
    except:
        pass

    mkdir('Microblocks Addon')
    mkdir('Microblocks Addon/resource_pack')
    mkdir('Microblocks Addon/resource_pack/attachables')
    mkdir('Microblocks Addon/resource_pack/texts')
    mkdir('Microblocks Addon/resource_pack/textures')
    mkdir('Microblocks Addon/resource_pack/textures/items')
    mkdir('Microblocks Addon/resource_pack/textures/items/mrc_heads')
    mkdir('Microblocks Addon/resource_pack/textures/models')
    mkdir('Microblocks Addon/resource_pack/textures/models/mrc_heads')
    mkdir('Microblocks Addon/resource_pack/models')
    mkdir('Microblocks Addon/resource_pack/models/entity')
    copy('template/resource_pack/models/entity/mrc_player_head.json',
         'Microblocks Addon/resource_pack/models/entity/mrc_player_head.json')
    copy('template/resource_pack/pack_icon.png',
         'Microblocks Addon/resource_pack/pack_icon.png')

    mkdir('Microblocks Addon/behavior_pack')
    mkdir('Microblocks Addon/behavior_pack/items')
    mkdir('Microblocks Addon/behavior_pack/loot_tables')
    mkdir('Microblocks Addon/behavior_pack/loot_tables/entities')
    copy('template/behavior_pack/pack_icon.png',
         'Microblocks Addon/behavior_pack/pack_icon.png')


def generate_manifests():
    with open('version.json', 'r') as infile:
        version = json.load(infile)
    version_string = '.'.join(str(x) for x in version)

    with open('template/resource_pack/microblock_manifest.json', 'r') as infile:
        resource_manifest = json.load(infile)
    resource_manifest['header']['description'] += version_string
    resource_manifest['header']['version'] = version
    resource_manifest['modules'][0]['description'] += version_string
    resource_manifest['modules'][0]['version'] = version
    resource_manifest['dependencies'][0]['version'] = version
    with open('Microblocks Addon/resource_pack/manifest.json', 'w') as outfile:
        json.dump(resource_manifest, outfile)

    with open('template/behavior_pack/microblock_manifest.json', 'r') as infile:
        behavior_manifest = json.load(infile)
    behavior_manifest['header']['description'] += version_string
    behavior_manifest['header']['version'] = version
    behavior_manifest['modules'][0]['description'] += version_string
    behavior_manifest['modules'][0]['version'] = version
    behavior_manifest['dependencies'][0]['version'] = version
    with open('Microblocks Addon/behavior_pack/manifest.json', 'w') as outfile:
        json.dump(behavior_manifest, outfile)


def package_addon():
    chdir('Microblocks Addon')
    with ZipFile('Microblocks.mcaddon', 'w') as archive:
        for subdir, dirs, files in walk('behavior_pack'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
        for subdir, dirs, files in walk('resource_pack'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)

    chdir('behavior_pack')
    with ZipFile('Microblocks Behavior.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('./'):
            for file in files:
                if not file.endswith('.mcpack'):
                    filepath = join(subdir, file)
                    archive.write(filepath)
    chdir('../')
    move('behavior_pack/Microblocks Behavior.mcpack', 'Microblocks Behavior.mcpack')

    chdir('resource_pack')
    with ZipFile('Microblocks Resource.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('./'):
            for file in files:
                if not file.endswith('.mcpack'):
                    filepath = join(subdir, file)
                    archive.write(filepath)
    chdir('../')
    move('resource_pack/Microblocks Resource.mcpack', 'Microblocks Resource.mcpack')
    chdir('../')
    


def main():
    setup_folders()
    generate_manifests()

    item_texture_json = {"resource_pack_name": "playerheads",
                         "texture_name": "atlas.items", "texture_data": {}}

    for subdir, dirs, files in walk('template/skins/people'):
        for filename in files:
            Person(filename, 'Microblocks Addon').add_to_pack(
                item_texture_json)
    for subdir, dirs, files in walk('template/skins/microblocks'):
        for filename in files:
            Microblock(filename, 'Microblocks Addon').add_to_pack(
                item_texture_json)
    for subdir, dirs, files in walk('template/skins/custom'):
        for filename in files:
            Custom(filename, 'Microblocks Addon').add_to_pack(
                item_texture_json)

    with open('Microblocks Addon/resource_pack/textures/item_texture.json', 'w') as outfile:
        json.dump(item_texture_json, outfile)

    package_addon()

    print("\
\nThe resource and behavior packs have been created. Now, you can add them to\n\
wandering trader trade table.")

    return


if __name__ == "__main__":
    main()
