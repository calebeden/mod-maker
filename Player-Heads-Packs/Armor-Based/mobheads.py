###########################################
# Author: calebeden
# File: class_based_mobheads.py
# Created on Wed Jun 15 2022
###########################################

from os import mkdir, walk, rename, chdir
from os.path import join
from shutil import copy, rmtree
from zipfile import ZipFile
import json
from PlayerHead import Mob


def setup_folders():
    try:
        rmtree('in_progress')
    except:
        pass
    try:
        rmtree('Mob Heads Addon')
    except:
        pass

    mkdir('in_progress')
    mkdir('in_progress/resource_pack')
    mkdir('in_progress/resource_pack/attachables')
    mkdir('in_progress/resource_pack/attachables/render')
    mkdir('in_progress/resource_pack/texts')
    mkdir('in_progress/resource_pack/textures')
    mkdir('in_progress/resource_pack/textures/items')
    mkdir('in_progress/resource_pack/textures/items/mrc_heads')
    mkdir('in_progress/resource_pack/textures/models')
    mkdir('in_progress/resource_pack/textures/models/mrc_heads')
    mkdir('in_progress/resource_pack/models')
    mkdir('in_progress/resource_pack/models/entity')
    copy('../template/resource_pack/models/entity/mrc_player_head.json',
         'in_progress/resource_pack/models/entity/mrc_player_head.json')
    copy('../template/resource_pack/pack_icon.png',
         'in_progress/resource_pack/pack_icon.png')

    mkdir('in_progress/behavior_pack')
    mkdir('in_progress/behavior_pack/items')
    mkdir('in_progress/behavior_pack/loot_tables')
    mkdir('in_progress/behavior_pack/loot_tables/entities')
    copy('../template/behavior_pack/pack_icon.png',
         'in_progress/behavior_pack/pack_icon.png')


def generate_manifests():
    with open('../version.json', 'r') as infile:
        version = json.load(infile)
    with open('../template/resource_pack/mobheads_manifest.json', 'r') as infile:
        resource_manifest = json.load(infile)
    resource_manifest['header']['version'] = version
    resource_manifest['modules'][0]['version'] = version
    resource_manifest['dependencies'][0]['version'] = version
    with open('in_progress/resource_pack/manifest.json', 'w') as outfile:
        json.dump(resource_manifest, outfile)

    with open('../template/behavior_pack/mobheads_manifest.json', 'r') as infile:
        behavior_manifest = json.load(infile)
    behavior_manifest['header']['version'] = version
    behavior_manifest['modules'][0]['version'] = version
    behavior_manifest['dependencies'][0]['version'] = version
    with open('in_progress/behavior_pack/manifest.json', 'w') as outfile:
        json.dump(behavior_manifest, outfile)


def package_addon():
    rename('in_progress', 'Mob Heads Addon')
    chdir('Mob Heads Addon')
    rename('behavior_pack', 'mobheads_b')
    with ZipFile('mobheads_b.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('mobheads_b'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
    rename('resource_pack', 'mobheads_r')
    with ZipFile('mobheads_r.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('mobheads_r'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
    with ZipFile('mobheads.mcaddon', 'w') as archive:
        for subdir, dirs, files in walk('mobheads_b'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
        for subdir, dirs, files in walk('mobheads_r'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)


def main():
    chdir('C:/Users/ceden/Documents/Software Development/Python/Overhang Tweaks/Player-Heads-Packs/Armor-Based/mobheads')
    setup_folders()
    generate_manifests()

    item_texture_json = {"resource_pack_name": "playerheads",
                         "texture_name": "atlas.items", "texture_data": {}}

    for subdir, dirs, files in walk('skins/mobs'):
        for filename in files:
            Mob(filename).add_to_pack(item_texture_json)

    with open('in_progress/resource_pack/textures/item_texture.json', 'w') as outfile:
        json.dump(item_texture_json, outfile)

    package_addon()

    print("\
\nThe resource and behavior packs have been created. Now, you can add them to\n\
the mob loot tables.")

    return


if __name__ == "__main__":
    main()
