###########################################
# Author: calebeden
# File: class_based_microblocks.py
# Created on Wed Jun 15 2022
###########################################

from os import mkdir, walk, sep, rename, chdir
from os.path import join
from shutil import copy, rmtree
from PIL import Image, ImageOps
from zipfile import ZipFile
import json


class PlayerHead:
    def __init__(self, filename, language_template):
        self._filename = filename
        self._item_name = filename[:-4].lower()
        self.__language_template = language_template

    @property
    def filename(self):
        return self._filename

    @property
    def name(self):
        return self._item_name

    def generate_attachable(self):
        with open('template/resource_pack/attachables/template.json', 'r') as infile:
            item_json = json.load(infile)
        item_json['minecraft:attachable']['description']['identifier'] = "playerhead:" + self._item_name
        item_json['minecraft:attachable']['description']['textures']['default'] = 'textures/models/heads/' + self._item_name
        with open('in_progress/resource_pack/attachables/' + self._item_name + '.json', 'w') as outfile:
            json.dump(item_json, outfile)

        with open('template/resource_pack/attachables/render/template.player.json', 'r') as infile:
            armor_json = json.load(infile)
        armor_json['minecraft:attachable']['description']['identifier'] = "playerhead:" + \
            self._item_name + ".player"
        armor_json['minecraft:attachable']['description']['item'] = {
            "playerhead:" + self._item_name: "query.owner_identifier == 'minecraft:player'"}
        armor_json['minecraft:attachable']['description']['textures']['default'] = 'textures/models/heads/' + self._item_name
        with open('in_progress/resource_pack/attachables/render/' + self._item_name + '.player.json', 'w') as outfile:
            json.dump(armor_json, outfile)

    def generate_item_texture(self, item_texture_json):
        image = Image.open(
            'in_progress/resource_pack/textures/models/heads/' + self._filename)
        base_layer = image.crop((8, 8, 16, 16))
        outer_layer = image.crop((40, 8, 48, 16))
        composite = Image.alpha_composite(base_layer, outer_layer)
        item_texture = ImageOps.expand(composite, 4)
        item_texture.save(
            'in_progress/resource_pack/textures/items/' + self._filename)

        item_texture_json['texture_data']['playerhead:' +
                                          self._item_name] = {'textures': 'textures/items/' + self._filename}

    def generate_behavior(self):
        with open('template/behavior_pack/items/template.json', 'r') as infile:
            item_behavior = json.load(infile)
        item_behavior['minecraft:item']['description']['identifier'] = 'playerhead:' + self._item_name
        item_behavior['minecraft:item']['components']['minecraft:icon']['texture'] = 'playerhead:' + self._item_name
        item_behavior['minecraft:item']['components']['minecraft:display_name']['value'] = self._item_name
        with open('in_progress/behavior_pack/items/' + self._item_name + '.json', 'w') as outfile:
            json.dump(item_behavior, outfile)

    def generate_text(self):
        head_text = self.__language_template.replace(
            'lower', self._item_name).replace('template', self.human_readable)
        with open('in_progress/resource_pack/texts/en_US.lang', 'a') as outfile:
            outfile.write(head_text)

    def add_to_pack(self, item_texture_json):
        self.generate_attachable()
        self.generate_text()
        self.copy_texture()
        self.generate_item_texture(item_texture_json)
        self.generate_behavior()
        print(self.human_readable)


class Microblock(PlayerHead):
    def __init__(self, filename):
        super().__init__(filename, "item.playerhead:lower.name=Micro-template\n")

    @property
    def human_readable(self):
        # TNT is an exception because it is all caps
        if self._item_name == 'tnt':
            return 'TNT'
        # Jack o'Lantern is an exception because it has a lowercase at the start of the word
        if self._item_name == 'jack_olantern':
            return "Jack o'Lantern"
        return self._item_name.replace('_', ' ').title().replace(' Of ', ' of ').replace(' And ', ' and ')

    def copy_texture(self):
        copy('skins/microblocks/' + self._filename,
             'in_progress/resource_pack/textures/models/heads/' + self._filename)


class Person(PlayerHead):
    def __init__(self, filename):
        self.__name = filename[:-4]
        super().__init__(filename, "item.playerhead:lower.name=template's Head")

    @property
    def human_readable(self):
        return self.__name

    def copy_texture(self):
        copy('skins/people/' + self._filename,
             'in_progress/resource_pack/textures/models/heads/' + self._filename)


class Custom(PlayerHead):
    def __init__(self, filename):
        super().__init__(filename, "item.playerhead:lower.name=template's Head")

    @property
    def human_readable(self):
        return self._item_name.replace('_', ' ').title().replace(' Of ', ' of ').replace(' And ', ' and ')

    def copy_texture(self):
        copy('skins/custom/' + self._filename,
             'in_progress/resource_pack/textures/models/heads/' + self._filename)


def setup_folders():
    try:
        rmtree('in_progress')
    except:
        pass
    try:
        rmtree('Microblocks Addon')
    except:
        pass

    mkdir('in_progress')
    mkdir('in_progress/resource_pack')
    mkdir('in_progress/resource_pack/attachables')
    mkdir('in_progress/resource_pack/attachables/render')
    mkdir('in_progress/resource_pack/texts')
    mkdir('in_progress/resource_pack/textures')
    mkdir('in_progress/resource_pack/textures/items')
    mkdir('in_progress/resource_pack/textures/models')
    mkdir('in_progress/resource_pack/textures/models/heads')
    copy('template/resource_pack/manifest.json',
         'in_progress/resource_pack/manifest.json')
    copy('template/resource_pack/pack_icon.png',
         'in_progress/resource_pack/pack_icon.png')

    mkdir('in_progress/behavior_pack')
    mkdir('in_progress/behavior_pack/items')
    mkdir('in_progress/behavior_pack/loot_tables')
    mkdir('in_progress/behavior_pack/loot_tables/entities')
    copy('template/behavior_pack/manifest.json',
         'in_progress/behavior_pack/manifest.json')
    copy('template/behavior_pack/pack_icon.png',
         'in_progress/behavior_pack/pack_icon.png')


def package_addon():
    rename('in_progress', 'Microblocks Addon')
    chdir('Microblocks Addon')
    rename('behavior_pack', 'microblocks_b')
    with ZipFile('microblocks_b.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('microblocks_b'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
    rename('resource_pack', 'microblocks_r')
    with ZipFile('microblocks_r.mcpack', 'w') as archive:
        for subdir, dirs, files in walk('microblocks_r'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
    with ZipFile('microblocks.mcaddon', 'w') as archive:
        for subdir, dirs, files in walk('microblocks_b'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)
        for subdir, dirs, files in walk('microblocks_r'):
            for file in files:
                filepath = join(subdir, file)
                archive.write(filepath)


def main():
    chdir('C:/Users/ceden/Documents/Software Development/Python/Overhang Tweaks/Player-Heads-Packs/Block-Based/microblocks')
    setup_folders()

    item_texture_json = {"resource_pack_name": "playerheads",
                         "texture_name": "atlas.items", "texture_data": {}}

    for subdir, dirs, files in walk('skins/people'):
        for filename in files:
            Person(filename).add_to_pack(item_texture_json)
    for subdir, dirs, files in walk('skins/microblocks'):
        for filename in files:
            Microblock(filename).add_to_pack(item_texture_json)
    for subdir, dirs, files in walk('skins/custom'):
        for filename in files:
            Custom(filename).add_to_pack(item_texture_json)

    with open('in_progress/resource_pack/textures/item_texture.json', 'w') as outfile:
        json.dump(item_texture_json, outfile)

    package_addon()

    print("\
\nThe resource and behavior packs have been created. Now, you can add them to\n\
wandering trader trade table.")

    return


if __name__ == "__main__":
    main()
