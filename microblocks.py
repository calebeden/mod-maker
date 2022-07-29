###########################################
# Author: calebeden
# File: class_based_microblocks.py
# Created on Wed Jun 15 2022
###########################################

from os import mkdir, walk, chdir
from os.path import join
from shutil import copy, rmtree
from zipfile import ZipFile
import json
from PlayerHead import Microblock, Person, Custom
from math import ceil


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
    mkdir('Microblocks Addon/resource_pack/textures/items/mrc_head_bundles')
    mkdir('Microblocks Addon/resource_pack/textures/models')
    mkdir('Microblocks Addon/resource_pack/textures/models/mrc_heads')
    mkdir('Microblocks Addon/resource_pack/models')
    mkdir('Microblocks Addon/resource_pack/models/entity')
    copy('template/resource_pack/models/entity/mrc_player_head.json',
         'Microblocks Addon/resource_pack/models/entity/mrc_player_head.json')
    copy('template/resource_pack/microblock_pack_icon.png',
         'Microblocks Addon/resource_pack/pack_icon.png')

    mkdir('Microblocks Addon/behavior_pack')
    mkdir('Microblocks Addon/behavior_pack/items')
    mkdir('Microblocks Addon/behavior_pack/trading')
    mkdir('Microblocks Addon/behavior_pack/trading/economy_trades')
    mkdir('Microblocks Addon/behavior_pack/recipes')
    copy('template/behavior_pack/microblock_pack_icon.png',
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
    resource_manifest['dependencies'][0]['version'] = version
    with open('Microblocks Addon/resource_pack/manifest.json', 'w') as outfile:
        json.dump(resource_manifest, outfile)

    with open('template/behavior_pack/microblock_manifest.json', 'r') as infile:
        behavior_manifest = json.load(infile)
    behavior_manifest['header']['description'] += version_string
    behavior_manifest['header']['version'] = version
    behavior_manifest['modules'][0]['description'] += version_string
    behavior_manifest['dependencies'][0]['version'] = version
    with open('Microblocks Addon/behavior_pack/manifest.json', 'w') as outfile:
        json.dump(behavior_manifest, outfile)


def generate_trades():
    with open('template/behavior_pack/trading/economy_trades/wandering_trader_trades.json', 'r') as infile:
        wandering_trades = json.load(infile)

    player_trades = {"num_to_select": 1, "trades": []}

    for subdir, dirs, files in walk('template/skins/people'):
        for filename in files:
            item_name = filename[:-4].lower()
            trade = {"max_uses": 3, "wants": [{"item": "minecraft:diamond"}], "gives": [
                {"item": f"mrc:{item_name}_head"}]}

            player_trades['trades'].append(trade)
    wandering_trades['tiers'][0]['groups'].insert(0, player_trades)

    with open('template/behavior_pack/trading/trade_pairs.json', 'r') as infile:
        trade_pairs = json.load(infile)
    print(f"\nThere are {len(trade_pairs)} survival microblocks. The wandering trader will sell {ceil(len(trade_pairs)/10)} at a time.\n")
    microblock_trades = {"num_to_select": ceil(len(trade_pairs)/10), "trades": []}

    for pair in trade_pairs:
        trade = {"max_uses": 1, "wants": [
            {"item": "minecraft:emerald"}], "gives": []}
        trade['wants'].append({"item": pair['block']})
        if 'data' in pair.keys():
            trade['wants'][1]['item'] += f":{pair['data']}"
        trade['gives'] = [
            {"item": f"{pair['microblock']}_head_bundle"}]

        microblock_trades['trades'].append(trade)
    wandering_trades['tiers'][0]['groups'].insert(1, microblock_trades)

    with open('Microblocks Addon/behavior_pack/trading/economy_trades/wandering_trader_trades.json', 'w') as outfile:
        json.dump(wandering_trades, outfile)

    # print(wandering_trades)


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

    generate_trades()

    package_addon()

    print("Done!")

    return


if __name__ == "__main__":
    main()
